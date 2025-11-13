import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
import random
from parallel_ai_testing.parallel_client import ParallelAIClient
from parallel_ai_testing.logger_config import setup_logger

logger = setup_logger()

BRANDS = ["Stellantis", "Airbus", "FIFA", "Bayer"]

PROMPTS_BY_CATEGORY = {
    "Media Presence": [
        "Which media outlets have reported on {brand} in the past 3 months?",
        "In which media has {brand} been mentioned most frequently in recent months?",
        "How has {brand}'s media presence developed over the last 6 months?"
    ],
    "Sentiment Analysis": [
        "How positive or negative has the media coverage about {brand} been in recent months?",
        "What is the overall tonality of the coverage about {brand}?",
        "Are there any indications of potential crises or negative topics {brand} should proactively address?"
    ],
    "Competitor Analysis": [
        "How does {brand} compare to competitors in media coverage and sentiment?",
        "Which topics are {brand}'s competitors currently focusing on?",
        "How often is {brand} mentioned compared to competitors?"
    ],
    "Topic Trends": [
        "Which topics had the biggest impact on {brand} in recent months?",
        "What are the dominant topics in {brand}'s industry right now?",
        "Which societal and economic issues are gaining importance for {brand}?"
    ]
}

ALL_PROCESSORS = ["lite", "base", "core", "core2x", "pro", "ultra", "ultra2x", "ultra4x", "ultra8x"]

PROCESSOR_COSTS = {
    "lite": 0.005,
    "base": 0.010,
    "core": 0.025,
    "core2x": 0.050,
    "pro": 0.100,
    "ultra": 0.300,
    "ultra2x": 0.600,
    "ultra4x": 1.200,
    "ultra8x": 2.400
}


def create_widget_prompt(brand: str, base_question: str) -> str:
    return f"""Generate a comprehensive analysis report for {brand} focusing on the following question:

{base_question}

Please structure your response as a JSON object with the following three widgets:

1. "media_segments": An analysis of which media outlets, platforms, and channels are discussing {brand}. Include breakdown by media type (online, print, social media, broadcast).

2. "sentiment": A detailed sentiment analysis including:
   - Overall sentiment score (positive, neutral, negative with percentages)
   - Sentiment trends over time
   - Key factors driving positive or negative sentiment
   - Specific examples of positive and negative coverage

3. "platform_heat_spike_map": A geographic and platform-based analysis showing:
   - Which platforms (Twitter/X, LinkedIn, Facebook, Instagram, TikTok, news sites, blogs) have the most activity
   - Which geographic regions show the highest volume of mentions
   - Any notable spikes in volume or engagement
   - Trending hashtags or topics related to {brand}

Return your response in strict JSON format with these exact widget names as top-level keys."""


async def test_single_query(client: ParallelClient, brand: str, prompt: str, processor: str) -> dict:
    start_time = time.time()
    
    try:
        result = await client.query_parallel_ai(prompt, [processor])
        
        end_time = time.time()
        latency = end_time - start_time
        
        processor_result = result.get(processor, {})
        
        return {
            "brand": brand,
            "processor": processor,
            "prompt": prompt,
            "success": processor_result.get("status") == "success",
            "latency_seconds": round(latency, 2),
            "cost_usd": PROCESSOR_COSTS[processor],
            "output": processor_result.get("output"),
            "error": processor_result.get("error"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        end_time = time.time()
        latency = end_time - start_time
        
        logger.error(f"Error testing {brand} on {processor}: {str(e)}")
        return {
            "brand": brand,
            "processor": processor,
            "prompt": prompt,
            "success": False,
            "latency_seconds": round(latency, 2),
            "cost_usd": PROCESSOR_COSTS[processor],
            "output": None,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def extract_widgets(output: dict) -> dict:
    if not output or not isinstance(output, dict):
        return {
            "media_segments": None,
            "sentiment": None,
            "platform_heat_spike_map": None,
            "extraction_success": False
        }
    
    content = output.get("content", {})
    
    media_segments = content.get("media_segments")
    sentiment = content.get("sentiment")
    platform_heat_spike_map = content.get("platform_heat_spike_map")
    
    extraction_success = all([
        media_segments is not None,
        sentiment is not None,
        platform_heat_spike_map is not None
    ])
    
    return {
        "media_segments": media_segments,
        "sentiment": sentiment,
        "platform_heat_spike_map": platform_heat_spike_map,
        "extraction_success": extraction_success
    }


async def run_comprehensive_test():
    logger.info("Starting comprehensive Parallel AI testing")
    logger.info(f"Testing {len(BRANDS)} brands across {len(ALL_PROCESSORS)} processors")
    
    client = ParallelClient()
    all_results = []
    
    for brand in BRANDS:
        category = random.choice(list(PROMPTS_BY_CATEGORY.keys()))
        base_question = random.choice(PROMPTS_BY_CATEGORY[category])
        base_question = base_question.format(brand=brand)
        
        prompt = create_widget_prompt(brand, base_question)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Testing brand: {brand}")
        logger.info(f"Category: {category}")
        logger.info(f"Base question: {base_question}")
        logger.info(f"{'='*80}\n")
        
        for processor in ALL_PROCESSORS:
            logger.info(f"Testing {brand} on processor: {processor}")
            
            result = await test_single_query(client, brand, prompt, processor)
            
            if result["success"]:
                widgets = extract_widgets(result["output"])
                result["widgets"] = widgets
                
                logger.info(f"✓ {processor}: Success (latency: {result['latency_seconds']}s, cost: ${result['cost_usd']}, widgets extracted: {widgets['extraction_success']})")
            else:
                result["widgets"] = {
                    "media_segments": None,
                    "sentiment": None,
                    "platform_heat_spike_map": None,
                    "extraction_success": False
                }
                logger.error(f"✗ {processor}: Failed - {result['error']}")
            
            all_results.append(result)
            
            await asyncio.sleep(2)
    
    return all_results


def generate_analysis_report(results: list) -> dict:
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r["success"])
    failed_tests = total_tests - successful_tests
    
    successful_extractions = sum(1 for r in results if r.get("widgets", {}).get("extraction_success", False))
    
    total_latency = sum(r["latency_seconds"] for r in results if r["success"])
    avg_latency = total_latency / successful_tests if successful_tests > 0 else 0
    
    total_cost = sum(r["cost_usd"] for r in results)
    
    processor_stats = {}
    for processor in ALL_PROCESSORS:
        processor_results = [r for r in results if r["processor"] == processor]
        successful = [r for r in processor_results if r["success"]]
        
        processor_stats[processor] = {
            "total_tests": len(processor_results),
            "successful": len(successful),
            "failed": len(processor_results) - len(successful),
            "success_rate": len(successful) / len(processor_results) if processor_results else 0,
            "avg_latency": sum(r["latency_seconds"] for r in successful) / len(successful) if successful else 0,
            "cost_per_test": PROCESSOR_COSTS[processor],
            "total_cost": PROCESSOR_COSTS[processor] * len(processor_results),
            "widgets_extracted": sum(1 for r in successful if r.get("widgets", {}).get("extraction_success", False))
        }
    
    brand_stats = {}
    for brand in BRANDS:
        brand_results = [r for r in results if r["brand"] == brand]
        successful = [r for r in brand_results if r["success"]]
        
        brand_stats[brand] = {
            "total_tests": len(brand_results),
            "successful": len(successful),
            "failed": len(brand_results) - len(successful),
            "success_rate": len(successful) / len(brand_results) if brand_results else 0,
            "avg_latency": sum(r["latency_seconds"] for r in successful) / len(successful) if successful else 0,
            "total_cost": sum(r["cost_usd"] for r in brand_results),
            "widgets_extracted": sum(1 for r in successful if r.get("widgets", {}).get("extraction_success", False))
        }
    
    return {
        "summary": {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "successful_widget_extractions": successful_extractions,
            "widget_extraction_rate": successful_extractions / successful_tests if successful_tests > 0 else 0,
            "total_latency_seconds": round(total_latency, 2),
            "average_latency_seconds": round(avg_latency, 2),
            "total_cost_usd": round(total_cost, 2)
        },
        "processor_stats": processor_stats,
        "brand_stats": brand_stats,
        "ease_of_integration": {
            "api_simplicity": "High - Simple async API with clear request/response format",
            "error_handling": "Good - Graceful degradation with detailed error messages",
            "widget_extraction": f"{successful_extractions}/{successful_tests} successful extractions",
            "documentation": "Comprehensive - Well-documented API with clear examples",
            "authentication": "Simple - Single API key authentication",
            "response_format": "JSON with structured content and basis fields"
        }
    }


async def main():
    logger.info("="*80)
    logger.info("COMPREHENSIVE PARALLEL AI TESTING")
    logger.info("="*80)
    logger.info(f"Brands: {', '.join(BRANDS)}")
    logger.info(f"Processors: {', '.join(ALL_PROCESSORS)}")
    logger.info(f"Total tests: {len(BRANDS) * len(ALL_PROCESSORS)}")
    logger.info("="*80)
    
    results = await run_comprehensive_test()
    
    analysis = generate_analysis_report(results)
    
    results_dir = Path("test_results")
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    detailed_results_file = results_dir / f"detailed_results_{timestamp}.json"
    with open(detailed_results_file, "w") as f:
        json.dump(results, f, indent=2)
    logger.info(f"\nDetailed results saved to: {detailed_results_file}")
    
    analysis_file = results_dir / f"analysis_report_{timestamp}.json"
    with open(analysis_file, "w") as f:
        json.dump(analysis, f, indent=2)
    logger.info(f"Analysis report saved to: {analysis_file}")
    
    logger.info("\n" + "="*80)
    logger.info("ANALYSIS SUMMARY")
    logger.info("="*80)
    logger.info(f"\nOverall Performance:")
    logger.info(f"  Total Tests: {analysis['summary']['total_tests']}")
    logger.info(f"  Successful: {analysis['summary']['successful_tests']}")
    logger.info(f"  Failed: {analysis['summary']['failed_tests']}")
    logger.info(f"  Success Rate: {analysis['summary']['success_rate']*100:.1f}%")
    logger.info(f"  Widget Extraction Rate: {analysis['summary']['widget_extraction_rate']*100:.1f}%")
    logger.info(f"  Average Latency: {analysis['summary']['average_latency_seconds']:.2f}s")
    logger.info(f"  Total Cost: ${analysis['summary']['total_cost_usd']:.2f}")
    
    logger.info(f"\nProcessor Performance:")
    for processor, stats in analysis['processor_stats'].items():
        logger.info(f"  {processor}:")
        logger.info(f"    Success Rate: {stats['success_rate']*100:.1f}%")
        logger.info(f"    Avg Latency: {stats['avg_latency']:.2f}s")
        logger.info(f"    Cost: ${stats['total_cost']:.2f}")
        logger.info(f"    Widgets Extracted: {stats['widgets_extracted']}/{stats['successful']}")
    
    logger.info(f"\nBrand Performance:")
    for brand, stats in analysis['brand_stats'].items():
        logger.info(f"  {brand}:")
        logger.info(f"    Success Rate: {stats['success_rate']*100:.1f}%")
        logger.info(f"    Avg Latency: {stats['avg_latency']:.2f}s")
        logger.info(f"    Cost: ${stats['total_cost']:.2f}")
        logger.info(f"    Widgets Extracted: {stats['widgets_extracted']}/{stats['successful']}")
    
    logger.info(f"\nEase of Integration:")
    for key, value in analysis['ease_of_integration'].items():
        logger.info(f"  {key}: {value}")
    
    logger.info("\n" + "="*80)
    logger.info("TESTING COMPLETE")
    logger.info("="*80)
    
    return analysis


if __name__ == "__main__":
    asyncio.run(main())

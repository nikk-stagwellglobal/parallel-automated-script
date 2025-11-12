import asyncio
import logging
from typing import List, Dict, Any
from parallel_ai_testing.logger_config import setup_logging
from parallel_ai_testing.parallel_client import ParallelAIClient, AVAILABLE_PROCESSORS, DEEP_RESEARCH_PROCESSORS
from parallel_ai_testing.prompt_generator import create_brand_query, create_prompt
from parallel_ai_testing.result_saver import ResultSaver

logger = logging.getLogger(__name__)


BRANDS = [
    "Stellantis",
    "BMW",
    "Toyota",
    "Ford",
    "Honda",
    "Tesla",
    "Mercedes",
    "Volkswagen",
    "Audi",
    "Hyundai"
]


async def process_brand(
    client: ParallelAIClient,
    brand: str,
    processors: List[str] = None
) -> List[Dict[str, Any]]:
    try:
        logger.info(f"Processing brand: {brand}")
        
        prompt = await create_prompt(brand)
        logger.info(f"Generated prompt for {brand}")
        
        results = await client.query_all_models(prompt, brand, processors)
        logger.info(f"Completed queries for {brand}")
        
        return results
    except Exception as e:
        logger.error(f"Error processing brand {brand}: {str(e)}")
        return [{
            "brand": brand,
            "processor": "unknown",
            "status": "error",
            "error": str(e)
        }]


async def process_all_brands(
    brands: List[str] = None,
    processors: List[str] = None,
    output_dir: str = "results"
) -> Dict[str, Any]:
    if brands is None:
        brands = BRANDS
    
    if processors is None:
        processors = DEEP_RESEARCH_PROCESSORS
    
    logger.info(f"Starting processing for {len(brands)} brands with {len(processors)} processors")
    logger.info(f"Brands: {', '.join(brands)}")
    logger.info(f"Processors: {', '.join(processors)}")
    
    client = ParallelAIClient()
    saver = ResultSaver(output_dir)
    
    all_results = []
    
    for brand in brands:
        brand_results = await process_brand(client, brand, processors)
        all_results.extend(brand_results)
        
        try:
            saver.save_brand_results(brand, brand_results)
        except Exception as e:
            logger.error(f"Failed to save results for {brand}: {str(e)}")
    
    try:
        overall_file = saver.save_results(all_results, "all_results.json")
        logger.info(f"All results saved to {overall_file}")
    except Exception as e:
        logger.error(f"Failed to save overall results: {str(e)}")
    
    summary = {
        "total_brands": len(brands),
        "total_processors": len(processors),
        "total_queries": len(all_results),
        "successful_queries": sum(1 for r in all_results if r.get("status") == "success"),
        "failed_queries": sum(1 for r in all_results if r.get("status") == "error"),
        "results": all_results
    }
    
    return summary


async def main():
    setup_logging(log_level="INFO", log_file="logs/parallel_testing.log")
    
    logger.info("=" * 80)
    logger.info("Starting Parallel AI Testing Script")
    logger.info("=" * 80)
    
    summary = await process_all_brands()
    

    logger.info("Processing Complete")
    logger.info(f"Total Brands: {summary['total_brands']}")
    logger.info(f"Total Processors: {summary['total_processors']}")
    logger.info(f"Total Queries: {summary['total_queries']}")
    logger.info(f"Successful: {summary['successful_queries']}")
    logger.info(f"Failed: {summary['failed_queries']}")



if __name__ == "__main__":
    asyncio.run(main())

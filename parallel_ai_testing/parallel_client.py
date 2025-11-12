import asyncio
import logging
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from parallel import Parallel

load_dotenv()
logger = logging.getLogger(__name__)


AVAILABLE_PROCESSORS = [
    "lite",
    "base",
    "core",
    "core2x",
    "pro",
    "ultra",
    "ultra2x",
    "ultra4x",
    "ultra8x",
]

DEEP_RESEARCH_PROCESSORS = [
    "pro",
    "ultra",
    "ultra2x",
    "ultra4x",
    "ultra8x",
]


class ParallelAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("PARALLEL_API_KEY")
        if not self.api_key:
            raise ValueError("PARALLEL_API_KEY must be set")
        self.client = Parallel(api_key=self.api_key)
    
    async def query_single_model(
        self, 
        prompt: str, 
        processor: str,
        brand: str
    ) -> Dict[str, Any]:
        try:
            logger.info(f"Querying {processor} for brand: {brand}")
            
            task_run = self.client.task_run.create(
                input=prompt,
                processor=processor
            )
            
            logger.info(f"Task created with ID: {task_run.run_id} for {processor}")
            
            run_result = self.client.task_run.result(
                task_run.run_id,
                api_timeout=3600
            )
            
            return {
                "brand": brand,
                "processor": processor,
                "run_id": task_run.run_id,
                "output": run_result.output,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error querying {processor} for {brand}: {str(e)}")
            return {
                "brand": brand,
                "processor": processor,
                "run_id": None,
                "output": None,
                "status": "error",
                "error": str(e)
            }
    
    async def query_all_models(
        self, 
        prompt: str, 
        brand: str,
        processors: List[str] = None
    ) -> List[Dict[str, Any]]:
        if processors is None:
            processors = AVAILABLE_PROCESSORS
        
        tasks = [
            self.query_single_model(prompt, processor, brand)
            for processor in processors
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Exception in query: {str(result)}")
                processed_results.append({
                    "brand": brand,
                    "processor": "unknown",
                    "status": "error",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results

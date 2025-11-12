import asyncio
from parallel_ai_testing.logger_config import setup_logging
from parallel_ai_testing.main import process_all_brands


async def custom_run():
    setup_logging(log_level="INFO", log_file="logs/custom_run.log")
    
    custom_brands = ["Tesla", "BMW", "Toyota"]
    custom_processors = ["pro", "ultra"]
    
    summary = await process_all_brands(
        brands=custom_brands,
        processors=custom_processors,
        output_dir="custom_results"
    )
    
    print("\n" + "=" * 80)
    print("CUSTOM RUN SUMMARY")
    print("=" * 80)
    print(f"Total Brands Processed: {summary['total_brands']}")
    print(f"Total Processors Used: {summary['total_processors']}")
    print(f"Total Queries Executed: {summary['total_queries']}")
    print(f"Successful Queries: {summary['successful_queries']}")
    print(f"Failed Queries: {summary['failed_queries']}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(custom_run())

#!/usr/bin/env python3
"""
Helper script to resume a partial test run.

Usage:
    python resume_test.py 20251117_143000
    
Where the timestamp is from the filename of the partial results you want to resume.
"""

import asyncio
import sys
from comprehensive_test import main
from parallel_ai_testing.logger_config import setup_logging

logger = setup_logging()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python resume_test.py <timestamp>")
        logger.error("Example: python resume_test.py 20251117_143000")
        sys.exit(1)
    
    timestamp = sys.argv[1]
    logger.info(f"Resuming test run with timestamp: {timestamp}")
    
    asyncio.run(main(resume_timestamp=timestamp))


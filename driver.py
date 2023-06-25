# This file will serve as the entry point of your program.
import asyncio
from extract_data import process_data

async def driver():
    await process_data()

if __name__ == '__main__':
    asyncio.run(driver())

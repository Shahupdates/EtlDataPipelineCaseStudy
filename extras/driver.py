import asyncio
from extract_data import process_data

async def main():
    await process_data()

if __name__ == '__main__':
    asyncio.run(main())

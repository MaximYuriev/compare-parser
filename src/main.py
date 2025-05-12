import asyncio
import time

from src.async_parser import start_async_parser
from src.sync_parser import start_sync_parser

print("Начинаю выполнение синхронного парсера!")
start_sync_time = time.time()
start_sync_parser()
end_sync_time = time.time()
print(f"Время выполнения синхронного парсера составило: {end_sync_time - start_sync_time}")

print("Начинаю выполнение асинхронного парсера!")
start_async_time = time.time()
asyncio.run(start_async_parser())
end_async_time = time.time()
print(f"Время выполнения асинхронного парсера составило: {end_async_time - start_async_time}")

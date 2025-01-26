import asyncio

stop_event = asyncio.Event()
stop_app_lock = asyncio.Lock()

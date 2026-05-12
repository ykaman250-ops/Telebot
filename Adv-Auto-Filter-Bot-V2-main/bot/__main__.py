#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import os
import asyncio
from aiohttp import web
from .bot import Bot

app = Bot()

async def start_web_server():
    async def handle_request(request):
        return web.Response(text="Bot is running!")
        
    web_app = web.Application()
    web_app.router.add_get('/', handle_request)
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Dummy web server started on port {port}")

loop = asyncio.get_event_loop()
loop.create_task(start_web_server())

app.run()
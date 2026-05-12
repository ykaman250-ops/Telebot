#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @SpEcHIDe

from pyrogram import Client, enums, __version__

from . import API_HASH, API_ID, LOGGER, BOT_TOKEN 

class Bot(Client):
    def __init__(self):
        super().__init__(
            "bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "bot/plugins"
            },
            workers=200,
            bot_token=BOT_TOKEN,
            sleep_threshold=10
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"@{bot_details.username}  started! "
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")

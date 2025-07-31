from pyrogram import Client
import asyncio
import config
from pyrogram.errors import RPCError
from ..logging import LOGGER

assistants = []
assistantids = []

async def safe_start(client: Client, name: str):
    try:
        await client.start()
    except TimeoutError:
        print(f"[Warning] {name} timed out. Retrying in 3s...")
        await asyncio.sleep(3)
        try:
            await client.start()
        except Exception as e:
            print(f"[Fatal] {name} failed to start: {e}")
            exit()
    except RPCError as e:
        print(f"[RPCError] {name} failed to start: {e}")
        exit()

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="AnonXAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="AnonXAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="AnonXAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="AnonXAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="AnonXAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")

        if config.STRING1:
            await safe_start(self.one, "Assistant 1")
            try:
                await self.one.join_chat("STORM_CORE")
                await self.one.join_chat("STORM_TECHH")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 1 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await self.one.get_me()
            self.one.id = me.id
            self.one.name = me.mention
            self.one.username = me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        if config.STRING2:
            await safe_start(self.two, "Assistant 2")
            try:
                await self.two.join_chat("STORM_CORE")
                await self.two.join_chat("STORM_TECHH")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 2 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await self.two.get_me()
            self.two.id = me.id
            self.two.name = me.mention
            self.two.username = me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.name}")

        if config.STRING3:
            await safe_start(self.three, "Assistant 3")
            try:
                await self.three.join_chat("STORM_CORE")
                await self.three.join_chat("STORM_TECHH")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 3 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await self.three.get_me()
            self.three.id = me.id
            self.three.name = me.mention
            self.three.username = me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.name}")

        if config.STRING4:
            await safe_start(self.four, "Assistant 4")
            try:
                await self.four.join_chat("STORM_CORE")
                await self.four.join_chat("STORM_TECHH")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 4 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await self.four.get_me()
            self.four.id = me.id
            self.four.name = me.mention
            self.four.username = me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.name}")

        if config.STRING5:
            await safe_start(self.five, "Assistant 5")
            try:
                await self.five.join_chat("STORM_CORE")
                await self.five.join_chat("STORM_TECHH")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 5 has failed to access the log Group. Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await self.five.get_me()
            self.five.id = me.id
            self.five.name = me.mention
            self.five.username = me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass

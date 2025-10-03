# ©️ qq_shark, 2025
# 🌐 https://github.com/qqshark/Modules/blob/main/always-online.py
# Licеnsed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# meta developer: @qq_shark

__version__ = (1, 3, 0)

import asyncio
from telethon.tl.functions.account import UpdateStatusRequest
from .. import loader, utils

@loader.tds
class AlwaysOnline(loader.Module):
    """Always Online - модуль вечного онлайна (by @qq_shark)."""

    strings = {
        "name": "Always Online",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Online mode enabled!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Online mode disabled!</b></blockquote>",
    }

    strings_ru = {
        "name": "Always Online",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Режим онлайн включен!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Режим онлайн выключен!</b></blockquote>",
    }

    strings_ua = {
        "name": "Always Online",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Режим онлайн увімкнено!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Режим онлайн вимкнено!</b></blockquote>",
    }

    strings_de = {
        "name": "Always Online",
        "online_on": "<blockquote><emoji document_id=5278411813468269386>✅</emoji> <b>Online-Modus aktiviert!</b></blockquote>",
        "online_off": "<blockquote><emoji document_id=5278578973595427038>🚫</emoji> <b>Online-Modus deaktiviert!</b></blockquote>",
    }

    def __init__(self):
        self.online_mode = False
        self._task = None

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.online_mode = self.db.get("AlwaysOnline", "online_mode", False)
        if self.online_mode:
            self._task = asyncio.create_task(self._keep_online_loop())

    async def _keep_online_loop(self):
        while True:
            try:
                await self.client(UpdateStatusRequest(offline=False))
            except Exception:
                pass
            await asyncio.sleep(3)

    @loader.command()
    async def onlinecmd(self, message):
        """- переключатель режима онлайн"""
        self.online_mode = not self.online_mode
        self.db.set("AlwaysOnline", "online_mode", self.online_mode)
        
        if self.online_mode:
            if not self._task or self._task.done():
                self._task = asyncio.create_task(self._keep_online_loop())
            await utils.answer(message, self.strings["online_on"])
        else:
            if self._task and not self._task.done():
                self._task.cancel()
            await utils.answer(message, self.strings["online_off"]) 

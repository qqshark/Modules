# ©️ qq_shark, 2025
# 🌐 ttps://github.com/qqshark/Modules/blob/main/storyes_manager.py
# Licensed under GNU AGPL v3.0
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

__version__ = (1, 0, 0)

from telethon.tl.types import Message
from telethon import functions, types
from .. import loader, utils
import os
import asyncio
import re

@loader.tds
class StoryManagesMod(loader.Module):
    """Story Manager (by @qq_shark)"""
    
    strings = {
        "name": "StoryManager",
        "uploading": "📤 Uploading story...",
        "success": """✅ Story successfully published!
⏰ Duration: {} hours""",
        "multi_start": "📤 Starting publication of {} stories...",
        "multi_progress": "✅ Published: {}/{} ⏳ Remaining: {}",
        "multi_complete": """🎉 Completed!
✅ Successfully published: {}/{} stories
⏰ Duration of each: {} hours""",
        "multi_error": "⚠️ Published {}/{} stories\n❌ Error on story #{}: {}",
        "no_media": "❌ Attach a photo or video to the command!",
        "no_reply": "❌ Reply to a message with media or attach a file!",
        "error": "❌ Error: {}",
        "no_premium": "❌ Telegram Premium is required to publish stories!",
        "download_error": "❌ Failed to download media",
        "limit_warning": "⚠️ {} stories specified, but Telegram limit is 100 stories per day!",
        "flood_wait": "⏳ FloodWait: waiting for {} seconds..."
    }
    
    strings_ru = {
        "_cls_doc": "Менеджер историй (by @qq_shark)",
        "uploading": "📤 Загружаю историю...",
        "success": """✅ История успешно опубликована!
⏰ Длительность: {} часов""",
        "multi_start": "📤 Начинаю публикацию {} историй...",
        "multi_progress": "✅ Опубликовано: {}/{} ⏳ Осталось: {}",
        "multi_complete": """🎉 Завершено!
✅ Успешно опубликовано: {}/{} историй
⏰ Длительность каждой: {} часов""",
        "multi_error": "⚠️ Опубликовано {}/{} историй\n❌ Ошибка на истории #{}: {}",
        "no_media": "❌ Прикрепи фото или видео к команде!",
        "no_reply": "❌ Ответь на сообщение с медиа или прикрепи файл!",
        "error": "❌ Ошибка: {}",
        "no_premium": "❌ Для публикации историй нужен Telegram Premium!",
        "download_error": "❌ Не удалось скачать медиа",
        "limit_warning": "⚠️ Указано {} историй, но лимит Telegram - 100 историй в сутки!",
        "flood_wait": "⏳ FloodWait: ожидание {} секунд..."
    }

    strings_ua = {
        "_cls_doc": "Менеджер історій (by @qq_shark)",
        "uploading": "📤 Завантажую історію...",
        "success": """✅ Історія успішно опублікована!
⏰ Тривалість: {} годин""",
        "multi_start": "📤 Починаю публікацію {} історій...",
        "multi_progress": "✅ Опубліковано: {}/{} ⏳ Залишилось: {}",
        "multi_complete": """🎉 Завершено!
✅ Успішно опубліковано: {}/{} історій
⏰ Тривалість кожної: {} годин""",
        "multi_error": "⚠️ Опубліковано {}/{} історій\n❌ Помилка на історії #{}: {}",
        "no_media": "❌ Прикріпи фото чи відео до команди!",
        "no_reply": "❌ Відповідай на повідомлення з медіа або прикріпи файл!",
        "error": "❌ Помилка: {}",
        "no_premium": "❌ Для публікації історій потрібен Telegram Premium!",
        "download_error": "❌ Не вдалося завантажити медіа",
        "limit_warning": "⚠️ Вказано {} історій, але ліміт Telegram - 100 історій на добу!",
        "flood_wait": "⏳ FloodWait: очікування {} секунд..."
    }

    strings_de = {
        "_cls_doc": "Story Manager (von @qq_shark)",
        "uploading": "📤 Lade Story hoch...",
        "success": """✅ Story erfolgreich veröffentlicht!
⏰ Dauer: {} Stunden""",
        "multi_start": "📤 Beginne Veröffentlichung von {} Stories...",
        "multi_progress": "✅ Veröffentlicht: {}/{} ⏳ Verbleibend: {}",
        "multi_complete": """🎉 Abgeschlossen!
✅ Erfolgreich veröffentlicht: {}/{} Stories
⏰ Dauer jeder Story: {} Stunden""",
        "multi_error": "⚠️ Veröffentlicht {}/{} Stories\n❌ Fehler bei Story #{}: {}",
        "no_media": "❌ Füge ein Foto oder Video zum Befehl hinzu!",
        "no_reply": "❌ Antworte auf eine Nachricht mit Medien oder füge eine Datei bei!",
        "error": "❌ Fehler: {}",
        "no_premium": "❌ Telegram Premium ist erforderlich, um Stories zu veröffentlichen!",
        "download_error": "❌ Medien-Download fehlgeschlagen",
        "limit_warning": "⚠️ {} Stories angegeben, aber das Telegram-Limit beträgt 100 Stories pro Tag!",
        "flood_wait": "⏳ FloodWait: warten auf {} Sekunden..."
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "period",
                86400,
                "Длительность истории в секундах (6ч=21600, 12ч=43200, 24ч=86400, 48ч=172800)",
                validator=loader.validators.Choice([21600, 43200, 86400, 172800])
            ),
            loader.ConfigValue(
                "privacy",
                "all",
                "Приватность: all (все), contacts (контакты), nobody (никто)",
                validator=loader.validators.Choice(["all", "contacts", "nobody"])
            ),
            loader.ConfigValue(
                "pinned",
                False,
                "Добавить в профиль после истечения",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "noforwards",
                False,
                "Запретить пересылку истории",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "repeat_count",
                30,
                "Сколько раз повторить публикацию одного медиа (по умолчанию 30)",
                validator=loader.validators.Integer(minimum=1, maximum=100)
            ),
            loader.ConfigValue(
                "repeat_delay",
                3,
                "Задержка между публикациями в секундах (рекомендуется 3-5 сек)",
                validator=loader.validators.Integer(minimum=1, maximum=60)
            )
        )
    
    async def _upload_story(self, client, media, caption, privacy_rule, period, pinned, noforwards):
        try:
            await client(functions.stories.SendStoryRequest(
                peer="me",
                media=media,
                privacy_rules=[privacy_rule],
                caption=caption,
                period=period,
                pinned=pinned,
                noforwards=noforwards
            ))
            return True, None
        except Exception as e:
            error_str = str(e)
            if "FLOOD_WAIT" in error_str:
                match = re.search(r'\d+', error_str)
                wait_time = int(match.group()) if match else 60
                return False, ("flood_wait", wait_time)
            return False, error_str

    def _get_media_and_mime_type(self, media_msg):
        if media_msg.photo or (media_msg.document and "image" in media_msg.document.mime_type):
            mime_type = "image"
        else:
            mime_type = media_msg.document.mime_type if media_msg.document else "video/mp4"
            
        return mime_type
    
    def _create_media_object(self, uploaded_file, mime_type):
        if mime_type == "image":
            return types.InputMediaUploadedPhoto(
                file=uploaded_file,
                spoiler=False
            )
        return types.InputMediaUploadedDocument(
            file=uploaded_file,
            mime_type=mime_type,
            attributes=[]
        )

    async def _handle_single_story_upload(self, message: Message, caption: str, period: int, pinned: bool, noforwards: bool, privacy_rule: types.TypeInputPrivacyRule):
        reply = await message.get_reply_message()
        media_msg = reply if reply and reply.media else message if message.media else None
        
        if not media_msg or not media_msg.media:
            await utils.answer(message, self.strings["no_reply"])
            return
        
        await utils.answer(message, self.strings["uploading"])
        
        file_path = None
        try:
            file_path = await media_msg.download_media()
            
            if not file_path:
                await utils.answer(message, self.strings["download_error"])
                return
            
            uploaded_file = await message.client.upload_file(file_path)
            
            mime_type = self._get_media_and_mime_type(media_msg)
            
            final_media = self._create_media_object(uploaded_file, mime_type)
            
            await self._upload_story(
                message.client,
                final_media,
                caption,
                privacy_rule,
                period,
                pinned,
                noforwards
            )
            
            hours = period // 3600
            await utils.answer(message, self.strings["success"].format(hours))
            
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
    
    @loader.command(
        ru_doc="- [описание] Опубликовать историю с медиа (ответь на фото/видео)",
        ua_doc="- [описання] Опублікувати історію з медіа (відповідай на фото/відео)",
        de_doc="- [beschreibung] Eine Story mit Medien veröffentlichen (auf Foto/Video antworten)",
    )
    async def storycmd(self, message: Message):
        """- [description] Publish a single story with media (reply to photo/video)"""
        me = await message.client.get_me()
        if not me.premium:
            await utils.answer(message, self.strings["no_premium"])
            return
        
        caption = utils.get_args_raw(message) or ""
        
        privacy_map = {
            "all": types.InputPrivacyValueAllowAll(),
            "contacts": types.InputPrivacyValueAllowContacts(),
            "nobody": types.InputPrivacyValueDisallowAll()
        }
        privacy_rule = privacy_map[self.config["privacy"]]
        
        await self._handle_single_story_upload(
            message,
            caption,
            self.config["period"],
            self.config["pinned"],
            self.config["noforwards"],
            privacy_rule
        )

    @loader.command(
        ru_doc="- [кол-во] Опубликовать несколько историй с одним медиа",
        ua_doc="- [кількість] Опублікувати декілька історій з одним медіа",
        de_doc="- [anzahl] Mehrere Stories mit denselben Medien veröffentlichen",
    )
    async def storymulticmd(self, message: Message):
        """- [quantity] [description] - Publish multiple stories with one media file"""
        me = await message.client.get_me()
        if not me.premium:
            await utils.answer(message, self.strings["no_premium"])
            return
        
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        media_msg = reply if reply and reply.media else message if message.media else None
      
        if not media_msg or not media_msg.media:
            await utils.answer(message, self.strings["no_reply"])
            return
        
        parts = args.split(maxsplit=1) if args else []
        
        if parts and parts[0].isdigit():
            count = int(parts[0])
            caption = parts[1] if len(parts) > 1 else ""
        else:
            count = self.config["repeat_count"]
            caption = args
        
        if count > 100:
            await utils.answer(message, self.strings["limit_warning"].format(count))
            count = 100
        
        await utils.answer(message, self.strings["multi_start"].format(count))
        await asyncio.sleep(1)
        
        file_path = None
        try:
            file_path = await media_msg.download_media()
            
            if not file_path:
                await utils.answer(message, self.strings["download_error"])
                return
            
            uploaded_file = await message.client.upload_file(file_path)
            
            mime_type = self._get_media_and_mime_type(media_msg)
            
            privacy_map = {
                "all": types.InputPrivacyValueAllowAll(),
                "contacts": types.InputPrivacyValueAllowContacts(),
                "nobody": types.InputPrivacyValueDisallowAll()
            }
            privacy_rule = privacy_map[self.config["privacy"]]
            
            successful = 0
            failed_at = None
            error_msg = None
            
            for i in range(1, count + 1):
                media = self._create_media_object(uploaded_file, mime_type)
                
                success, error = await self._upload_story(
                    message.client, 
                    media, 
                    caption, 
                    privacy_rule,
                    self.config["period"],
                    self.config["pinned"],
                    self.config["noforwards"]
                )
                
                if success:
                    successful += 1
                    
                    if i % 5 == 0 or i == count:
                        await utils.answer(
                            message,
                            self.strings["multi_progress"].format(
                                successful, 
                                count,
                                count - i
                            )
                        )
                    
                    if i < count:
                        await asyncio.sleep(self.config["repeat_delay"])
                else:
                    if error and error[0] == "flood_wait":
                        wait_time = error[1]
                        await utils.answer(
                            message,
                            self.strings["flood_wait"].format(wait_time)
                        )
                        await asyncio.sleep(wait_time)
              
                        media_retry = self._create_media_object(uploaded_file, mime_type)
                        success_retry, _ = await self._upload_story(
                            message.client,
                            media_retry,
                            caption,
                            privacy_rule,
                            self.config["period"],
                            self.config["pinned"],
                            self.config["noforwards"]
                        )
                        
                        if success_retry:
                            successful += 1
                            continue
                    
                    failed_at = i
                    error_msg = error[1] if isinstance(error, tuple) else str(error)
                    break
            
            if failed_at:
                await utils.answer(
                    message,
                    self.strings["multi_error"].format(
                        successful,
                        count,
                        failed_at,
                        error_msg
                    )
                )
            else:
                hours = self.config["period"] // 3600
                await utils.answer(
                    message,
                    self.strings["multi_complete"].format(
                        successful,
                        count,
                        hours
                    )
                )
            
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
   
    @loader.command(
        ru_doc="- [описание] Быстрая публикация истории (24ч, для всех)",
        ua_doc="- [описання] Швидка публікація історії (24г, для всіх)",
        de_doc="- [beschreibung] Schnelle Story-Veröffentlichung (24h, für alle)",
    )
    async def storyquickcmd(self, message: Message):
        """- [description] Quick story publication (24h, for all)"""
        me = await message.client.get_me()
        if not me.premium:
            await utils.answer(message, self.strings["no_premium"])
            return
        
        caption = utils.get_args_raw(message) or ""
        
        QUICK_PERIOD = 86400
        QUICK_PINNED = False
        QUICK_NOFORWARDS = False
        QUICK_PRIVACY = types.InputPrivacyValueAllowAll()
        
        await self._handle_single_story_upload(
            message,
            caption,
            QUICK_PERIOD,
            QUICK_PINNED,
            QUICK_NOFORWARDS,
            QUICK_PRIVACY
        )
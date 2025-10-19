# ©️ qq_shark, 2025
# 🌐 [https://github.com/qqshark/Modules/blob/main/birthday.py](https://github.com/qqshark/Modules/blob/main/birthday.py)
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

from datetime import datetime, date
import pytz
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class BirthdayMod(loader.Module):
    """Простой модуль показывающий сколько дней до дня рождения (by @qq_shark)"""

    strings = {
        "name": "Birthday",
        "birthday_today": "🎉 Сегодня твой день рождения! Поздравляю! 🎂",
        "days_left": "🎂 До дня рождения осталось: <b>{days} {days_word}</b>",
        "config_birthday": "Дата рождения в формате ДД.ММ.ГГГГ (например: 04.11.2008)", # эт тип моё др ыыы
        "invalid_date": "❌ Неверный формат даты в конфигурации. Используй ДД.ММ.ГГГГ",
        "no_config": "❌ Дата рождения не указана"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "birthday_date",
                "",
                lambda: self.strings["config_birthday"]
            )
        )

    def get_days_word(self, days):
        if days % 10 == 1 and days % 100 != 11:
            return "день"
        elif days % 10 in [2, 3, 4] and days % 100 not in [12, 13, 14]:
            return "дня"
        else:
            return "дней"

    def calculate_days_to_birthday(self, birthday_date):
        moscow_tz = pytz.timezone('Europe/Moscow')
        today = datetime.now(moscow_tz).date()
        
        current_year_birthday = date(today.year, birthday_date.month, birthday_date.day)
        
        if current_year_birthday < today:
            next_birthday = date(today.year + 1, birthday_date.month, birthday_date.day)
        else:
            next_birthday = current_year_birthday
        
        days_left = (next_birthday - today).days
        
        return days_left

    @loader.command()
    async def bday(self, message: Message):
        """- показать количество дней до дня рождения"""
        if not self.config["birthday_date"]:
            await utils.answer(message, self.strings["no_config"])
            return
        
        try:
            birthday_str = self.config["birthday_date"].strip()
            birthday_date = datetime.strptime(birthday_str, "%d.%m.%Y").date()
            
            days_left = self.calculate_days_to_birthday(birthday_date)
            
            if days_left == 0:
                await utils.answer(message, self.strings["birthday_today"])
            else:
                days_word = self.get_days_word(days_left)
                await utils.answer(
                    message, 
                    self.strings["days_left"].format(
                        days=days_left, 
                        days_word=days_word
                    )
                )
                
        except ValueError:
            await utils.answer(message, self.strings["invalid_date"])
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")

    @loader.command()
    async def bdayinfo(self, message: Message):
        """- показать текущие настройки"""
        
        if not self.config["birthday_date"]:
            await utils.answer(message, self.strings["no_config"])
            return
            
        try:
            birthday_str = self.config["birthday_date"].strip()
            birthday_date = datetime.strptime(birthday_str, "%d.%m.%Y").date()
            
            moscow_tz = pytz.timezone('Europe/Moscow')
            current_time = datetime.now(moscow_tz)
            
            today = current_time.date()
            age = today.year - birthday_date.year
            if today < date(today.year, birthday_date.month, birthday_date.day):
                age -= 1
            
            info_text = f"📅 <b>Дата рождения:</b> {birthday_date.strftime('%d.%m.%Y')}\n"
            info_text += f"🎂 <b>Возраст:</b> {age} лет\n"
            info_text += f"🕐 <b>Время по МСК:</b> {current_time.strftime('%d.%m.%Y %H:%M')}"
            
            await utils.answer(message, info_text)
            
        except ValueError:
            await utils.answer(message, self.strings["invalid_date"])

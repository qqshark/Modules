# ©️ qq_shark, 2025
# 🌐 [https://github.com/qqshark/Modules/blob/main/always-online.py](https://github.com/qqshark/Modules/blob/main/binchecker.py)
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

__version__ = (1, 0, 1)

from telethon.tl.types import Message
from .. import loader, utils
import aiohttp


@loader.tds
class BinCheckerMod(loader.Module):
    """Simple BIN checker via binlist.net (by @qq_shark)"""

    strings = {
        'name': 'BinChecker',
        'no_args': '<emoji document_id=5839380580080293813>🖋</emoji> Specify a BIN or card number',
        'digits_only': '<emoji document_id=5893444447286334441>📰</emoji> BIN must contain only digits',
        'checking': '<emoji document_id=6032653721853234759>🗣</emoji> Checking BIN: {}...',
        'not_found': '<emoji document_id=6039400853482246862>📥</emoji> BIN {} not found in database',
        'too_many_requests': '<emoji document_id=5850317551090800862>⏰</emoji> Too many requests. Try again later',
        'api_error': '<emoji document_id=6030864215139422409>🔗</emoji> API Error: {}',
        'request_error': '<emoji document_id=5778197572652897847>🙁</emoji> Request Error: {}',
        'bin_label': '<emoji document_id=5927169041595634481>💳</emoji> BIN:',
        'scheme_label': '<emoji document_id=5879785854284599288>ℹ️</emoji> Payment System:',
        'type_label': '<emoji document_id=5956561916573782596>📄</emoji> Card Type:',
        'brand_label': '<emoji document_id=5951584964305755220>#️⃣</emoji> Brand:',
        'country_label': '<emoji document_id=5778661935927004845>📍</emoji> Country:',
        'currency_label': '<emoji document_id=5992430854909989581>🪙</emoji> Currency:',
        'bank_label': '<emoji document_id=5778311685638984859>🪙</emoji> Bank:',
        'city_label': '<emoji document_id=5884123981706956210>➡️</emoji> City:',
        'phone_label': '<emoji document_id=5897938112654348733>📞</emoji> Phone:',
        'url_label': '<emoji document_id=5879585266426973039>🌐</emoji> Website:',
    }

    strings_ru = {
        '_cls_doc': 'Простой BIN чекер через binlist.net (by @qq_shark)',
        'name': 'BinChecker',
        'no_args': '<emoji document_id=5839380580080293813>🖋</emoji> Укажите BIN или номер карты',
        'digits_only': '<emoji document_id=5893444447286334441>📰</emoji> BIN должен содержать только цифры',
        'checking': '<emoji document_id=6032653721853234759>🗣</emoji> Проверяю BIN: {}...',
        'not_found': '<emoji document_id=6039400853482246862>📥</emoji> BIN {} не найден в базе данных',
        'too_many_requests': '<emoji document_id=5850317551090800862>⏰</emoji> Слишком много запросов. Попробуйте позже',
        'api_error': '<emoji document_id=6030864215139422409>🔗</emoji> Ошибка API: {}',
        'request_error': '<emoji document_id=5778197572652897847>🙁</emoji> Ошибка запроса: {}',
        'bin_label': '<emoji document_id=5927169041595634481>💳</emoji> BIN:',
        'scheme_label': '<emoji document_id=5879785854284599288>ℹ️</emoji> Платежная система:',
        'type_label': '<emoji document_id=5956561916573782596>📄</emoji> Тип карты:',
        'brand_label': '<emoji document_id=5951584964305755220>#️⃣</emoji> Бренд:',
        'country_label': '<emoji document_id=5778661935927004845>📍</emoji> Страна:',
        'currency_label': '<emoji document_id=5992430854909989581>🪙</emoji> Валюта:',
        'bank_label': '<emoji document_id=5778311685638984859>🪙</emoji> Банк:',
        'city_label': '<emoji document_id=5884123981706956210>➡️</emoji> Город:',
        'phone_label': '<emoji document_id=5897938112654348733>📞</emoji> Телефон:',
        'url_label': '<emoji document_id=5879585266426973039>🌐</emoji> Сайт:',
    }

    strings_ua = {
        '_cls_doc': 'Простий BIN чекер через binlist.net (by @qq_shark)',
        'name': 'BinChecker',
        'no_args': '<emoji document_id=5839380580080293813>🖋</emoji> Вкажіть BIN або номер картки',
        'digits_only': '<emoji document_id=5893444447286334441>📰</emoji> BIN повинен містити лише цифри',
        'checking': '<emoji document_id=6032653721853234759>🗣</emoji> Перевіряю BIN: {}...',
        'not_found': '<emoji document_id=6039400853482246862>📥</emoji> BIN {} не знайдено в базі даних',
        'too_many_requests': '<emoji document_id=5850317551090800862>⏰</emoji> Забагато запитів. Спробуйте пізніше',
        'api_error': '<emoji document_id=6030864215139422409>🔗</emoji> Помилка API: {}',
        'request_error': '<emoji document_id=5778197572652897847>🙁</emoji> Помилка запиту: {}',
        'bin_label': '<emoji document_id=5927169041595634481>💳</emoji> BIN:',
        'scheme_label': '<emoji document_id=5879785854284599288>ℹ️</emoji> Платіжна система:',
        'type_label': '<emoji document_id=5956561916573782596>📄</emoji> Тип картки:',
        'brand_label': '<emoji document_id=5951584964305755220>#️⃣</emoji> Бренд:',
        'country_label': '<emoji document_id=5778661935927004845>📍</emoji> Країна:',
        'currency_label': '<emoji document_id=5992430854909989581>🪙</emoji> Валюта:',
        'bank_label': '<emoji document_id=5778311685638984859>🪙</emoji> Банк:',
        'city_label': '<emoji document_id=5884123981706956210>➡️</emoji> Місто:',
        'phone_label': '<emoji document_id=5897938112654348733>📞</emoji> Телефон:',
        'url_label': '<emoji document_id=5879585266426973039>🌐</emoji> Сайт:',
    }

    strings_de = {
        '_cls_doc': 'Ein einfacher BIN-Checker über binlist.net (by @qq_shark)',
        'name': 'BinChecker',
        'no_args': '<emoji document_id=5839380580080293813>🖋</emoji> Geben Sie eine BIN oder Kartennummer an',
        'digits_only': '<emoji document_id=5893444447286334441>📰</emoji> BIN darf nur Ziffern enthalten',
        'checking': '<emoji document_id=6032653721853234759>🗣</emoji> Überprüfe BIN: {}...',
        'not_found': '<emoji document_id=6039400853482246862>📥</emoji> BIN {} nicht in der Datenbank gefunden',
        'too_many_requests': '<emoji document_id=5850317551090800862>⏰</emoji> Zu viele Anfragen. Versuchen Sie es später erneut',
        'api_error': '<emoji document_id=6030864215139422409>🔗</emoji> API-Fehler: {}',
        'request_error': '<emoji document_id=5778197572652897847>🙁</emoji> Anfragefehler: {}',
        'bin_label': '<emoji document_id=5927169041595634481>💳</emoji> BIN:',
        'scheme_label': '<emoji document_id=5879785854284599288>ℹ️</emoji> Zahlungssystem:',
        'type_label': '<emoji document_id=5956561916573782596>📄</emoji> Kartentyp:',
        'brand_label': '<emoji document_id=5951584964305755220>#️⃣</emoji> Marke:',
        'country_label': '<emoji document_id=5778661935927004845>📍</emoji> Land:',
        'currency_label': '<emoji document_id=5992430854909989581>🪙</emoji> Währung:',
        'bank_label': '<emoji document_id=5778311685638984859>🪙</emoji> Bank:',
        'city_label': '<emoji document_id=5884123981706956210>➡️</emoji> Stadt:',
        'phone_label': '<emoji document_id=5897938112654348733>📞</emoji> Telefon:',
        'url_label': '<emoji document_id=5879585266426973039>🌐</emoji> Webseite:',
    }

    @loader.command(
        ru_doc="- проверить BIN",
        ua_doc="- перевірити BIN",
        de_doc="- prüfen BIN",
    )
    async def bincmd(self, message: Message):
        """- check BIN"""
        args = utils.get_args_raw(message)
        
        if not args:
            await utils.answer(message, self.strings('no_args'))
            return
        
        card_input = args.replace(' ', '').replace('-', '')
        
        if not card_input.isdigit():
            await utils.answer(message, self.strings('digits_only'))
            return
        
        bin_number = card_input[:6] if len(card_input) >= 6 else card_input
        
        await utils.answer(message, self.strings('checking').format(bin_number))
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f'https://lookup.binlist.net/{bin_number}'
                async with session.get(url, headers={'Accept-Version': '3'}) as response:
                    
                    if response.status == 404:
                        await utils.answer(message, self.strings('not_found').format(bin_number))
                        return
                    elif response.status == 429:
                        await utils.answer(message, self.strings('too_many_requests'))
                        return
                    elif response.status != 200:
                        await utils.answer(message, self.strings('api_error').format(response.status))
                        return
                    
                    data = await response.json()
        
        except Exception as e:
            await utils.answer(message, self.strings('request_error').format(e))
            return
        
        scheme = data.get('scheme', 'N/A').upper()
        card_type = data.get('type', 'N/A').capitalize()
        brand = data.get('brand', 'N/A')
        
        country_data = data.get('country', {})
        country_name = country_data.get('name', 'N/A')
        country_emoji = country_data.get('emoji', '')
        country_currency = country_data.get('currency', 'N/A')
        country_alpha2 = country_data.get('alpha2', 'N/A')
        
        bank_data = data.get('bank', {})
        bank_name = bank_data.get('name', 'N/A')
        bank_url = bank_data.get('url', '')
        bank_phone = bank_data.get('phone', '')
        bank_city = bank_data.get('city', 'N/A')
        
        result = f'<b>{self.strings["bin_label"]}</b> {bin_number}\n\n'
        result += f'<b>{self.strings["scheme_label"]}</b> {scheme}\n'
        result += f'<b>{self.strings["type_label"]}</b> {card_type}\n'
        result += f'<b>{self.strings["brand_label"]}</b> {brand}\n\n'
        result += f'<b>{self.strings["country_label"]}</b> {country_emoji} {country_name} ({country_alpha2})\n'
        result += f'<b>{self.strings["currency_label"]}</b> {country_currency}\n\n'
        result += f'<b>{self.strings["bank_label"]}</b> {bank_name}'

        if bank_city and bank_city != 'N/A':
            result += f'\n<b>{self.strings["city_label"]}</b> {bank_city}'
        if bank_phone:
            result += f'\n<b>{self.strings["phone_label"]}</b> {bank_phone}'
        if bank_url:
            result += f'\n<b>{self.strings["url_label"]}</b> {bank_url}'
        
        await utils.answer(message, result)

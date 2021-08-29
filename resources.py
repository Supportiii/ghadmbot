import random
from aiogram import types
from locales_dict import LocalesDict

class QueryResults:
    def __init__(self, locales: LocalesDict):
        self.locales = locales

    def message_too_long(self, lang: str):
        message_content = types.InputTextMessageContent(self.locales[lang].too_long_message)
        return types.InlineQueryResultArticle(
            id = '1', title = self.locales[lang].too_long_title,
            input_message_content = message_content,
            description = self.locales[lang].too_long_description,
            thumb_url = 'https://i.imgur.com/xblMvAx.png')

    def mode_for(self, lang: str, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton(self.locales[lang].view, callback_data = str(post_id) + ' for')]])
        message_content = types.InputTextMessageContent(self.locales[lang].for_message % scope_string)
        return types.InlineQueryResultArticle(
            id = 'for', title = self.locales[lang].for_title % scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/hHIkDSu.png')

    def mode_except(self, lang: str, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton(self.locales[lang].view, callback_data = str(post_id) + ' except')]])
        message_content = types.InputTextMessageContent(self.locales[lang].except_message % scope_string)
        return types.InlineQueryResultArticle(
            id = 'except', title = self.locales[lang].except_title % scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/S6OZMHd.png')

    def spoiler(self, lang: str, post_id, body):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton(self.locales[lang].view, callback_data = str(post_id) + ' spoiler')]])
        message_content = types.InputTextMessageContent(self.locales[lang].spoiler_message)
        return types.InlineQueryResultArticle(
            id = 'spoiler', title = self.locales[lang].spoiler_title,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/mS2ir0T.png')

class Keyboards:
    def info_keyboard(self):
        return types.InlineKeyboardMarkup(inline_keyboard=
              [[types.InlineKeyboardButton('📑 HowTo',             url='https://telegra.ph/TGi-08-29')],
               [types.InlineKeyboardButton('👥 Group',             url='https://t.me/iSupGr')],
               [types.InlineKeyboardButton('👷 TestGroups',        url='https://t.me/iTestGroups'),
                types.InlineKeyboardButton('🌐 Official Bot Repo', url='https://github.com/undrcrxwn/hidethisbot')]])
class Media:
    def group_greeting_sticker_id(self):
        return random.choice(('CAACAgIAAxkBAAEpCbphK_C_---mCsuQDAkH1L7Efjx6HAACwQ0AAv86UUvmahUYxf0RgiAE',
                              'CAACAgIAAxkBAAEpCb9hK_DbX8gXxdXD-w_ZOj0GM2Et_wACRRIAAu8nWEt3iTB_7h6DdCAE',
                              'CAACAgIAAxkBAAEpCcFhK_DvPmbR3gi-fp4oKe7OXgsBTwACZQ4AAuB3WEvVwmBch1xaqSAE'))

class Resources:
    def __init__(self, locales: LocalesDict):
        self.query_results = QueryResults(locales)
        self.keyboards = Keyboards()
        self.media = Media()

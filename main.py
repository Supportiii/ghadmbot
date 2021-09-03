import os
import random
import re
import time
from datetime import datetime
from threading import Thread

import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from loguru import logger

from locales import locales
from resources import Resources

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked, TelegramAPIError
from os import getenv
from sys import exit
import logs

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsGroupJoin(BoundFilter):
    key = "is_group_join"

    def __init__(self, is_group_join: bool):
        self.is_group_join = is_group_join

    async def check(self, update: types.ChatMemberUpdated):
        return update.old_chat_member.status in ("kicked", "left") and \
               update.new_chat_member.status in ("member", "administrator") and \
               update.chat.type in ("group", "supergroup")
    

logger.add(os.environ['LOG_PATH'], level = 'DEBUG')
rsc = Resources(locales)

inline_query_regex = re.compile(r'^.+([ \n](@\w+|id[0-9]+))+$')
scope_regex = re.compile(r'([ \n](@\w+|id[0-9]+))+$')

ignored_chat_ids = set()
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
bot = Bot(token = os.environ['API_TOKEN'])
dp = Dispatcher(bot)
##################################
@dp.message_handler(commands="id")
async def cmd_id(message: types.Message):
    """
    /id command handler for all chats
    :param message: Telegram message with "/id" command
    """
    if message.chat.id == message.from_user.id:
        await message.answer(f"Your Telegram ID is <code>{message.from_user.id}</code>")
    else:
        await message.answer(f"This {message.chat.type} chat ID is <code>{message.chat.id}</code>")
    logs.track("/id")

@dp.message_handler(lambda message: message.forward_from, content_types=types.ContentTypes.ANY)
async def get_user_id_no_privacy(message: types.Message):
    """
    Handler for message forwarded from other user who doesn't hide their ID
    :param message: Telegram message with "forward_from" field not empty
    """
    if message.forward_from.is_bot:
        msg = f"This bot's ID is <code>{message.forward_from.id}</code>"
    else:
        msg = f"This user's ID is <code>{message.forward_from.id}</code>"
    if message.sticker:
        msg += f"\nAlso this sticker's ID is <code>{message.sticker.file_id}</code>"
    await message.reply(msg)
    logs.track("Check user or bot")


@dp.my_chat_member_handler(is_group_join=True)
async def new_chat(update: types.ChatMemberUpdated):
    """
    Handler bot being added to group or supergroup
    :param update: Update of type ChatMemberUpdated, where old_chat_member.status is "left",
        new_chat_member.status is "member" and chat.type is either "group" or "supergroup"
    """
    await update.bot.send_message(update.chat.id, f"This {update.chat.type} chat ID is <code>{update.chat.id}</code>")
    logs.track("Added to group")

    
@dp.message_handler(content_types=["migrate_to_chat_id"])
async def group_upgrade_to(message: types.Message):
    """
    When group is migrated to supergroup, sends new chat ID.
    Notice that the first argument of send_message is message.migrate_to_chat_id, not message.chat.id!
    Otherwise, MigrateChat exception will raise
    :param message: Telegram message with "migrate_to_chat_id" field not empty
    """
    await bot.send_message(message.migrate_to_chat_id, f"Group upgraded to supergroup.\n"
                                                       f"Old ID: <code>{message.chat.id}</code>\n"
                                                       f"New ID: <code>{message.migrate_to_chat_id}</code>")
    logs.track("Group migrate")


@dp.message_handler(chat_type=types.ChatType.PRIVATE, content_types=types.ContentTypes.ANY)
async def private_chat(message: types.Message):
    """
    Handler for messages in private chat (one-to-one dialogue)
    :param message: Telegram message sent to private chat (one-to-one dialogue)
    """
    msg = f"Your Telegram ID is <code>{message.chat.id}</code>"
    if message.sticker:
        msg += f"\n\nAlso this sticker's ID is <code>{message.sticker.file_id}</code>"
    await message.reply(msg)
    logs.track("Any message in PM")
######################################
    
    
def ignore(chat_id, timeout):
    ignored_chat_ids.add(chat_id)
    time.sleep(timeout)
    ignored_chat_ids.remove(chat_id)

def execute_query(query, data = None):
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        result = cursor.fetchall()
    except Exception as e:
        logger.error(e)
        connection.rollback()
        logger.info('transaction rollback: "' + query + '"')
    return result

def execute_read_query(query, data = None):
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        result = cursor.fetchall()
    except Exception as e:
        logger.error(e)
    return result

def get_formatted_username_or_id(user: types.User):
    return 'id' + str(user.id) if user.username is None else '@' + user.username

def get_post(post_id: int):
    result = None
    try:
        result = execute_read_query('SELECT * FROM posts WHERE id = %s', (str(post_id),))[0]
    except Exception as e:
        logger.error(e)

    if result is None:
        logger.warning('#' + str(post_id) + ' cannot be reached')
    return result

def insert_post(post_id: int, author: types.User, content: str, scope: list = None):
    result = None
    try:
        scope_string = '' if scope is None else ' '.join(scope).replace('@', '').lower()
        result = execute_query('INSERT INTO posts (id, author, content, scope, creation_time) '
                               'VALUES (%s, %s, %s, %s, NOW()) RETURNING id',
                               (post_id, author.id, content, scope_string))
    except Exception as e:
        logger.error(e)

    if result is None:
        logger.warning('#' + str(post_id) + ' cannot be inserted by ' + get_formatted_username_or_id(author))
    else:
        logger.info('#' + str(post_id) + ' has been inserted by ' + get_formatted_username_or_id(author))
    return result

def update_user_in_scope(post_id: int, username: str, user_id: int):
    try:
        (_, author, body, scope_string, creation_time) = get_post(post_id)
        scope = scope_string.split(' ')
        for i, mention in enumerate(scope):
            if mention == username:
                scope[i] = str(user_id)
        execute_query('UPDATE posts '
                      'SET scope = %s '
                      'WHERE id = %s;',
                      (' '.join(scope), post_id))
    except Exception as e:
        logger.error(e)
        logger.warning('cannot update @' +  username + ' to id: ' + str(user_id) + ' in scope #' + str(post_id))

@dp.inline_handler(lambda query: re.match(inline_query_regex, query.query.replace('\n', ' ')))
async def inline_query_hide(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        body = scope_regex.sub('', inline_query.query)
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        raw_scope = re.sub(r'(id)([0-9]+)', r'\g<2>', inline_query.query[len(body) + 1:]).split(' ')
        marker = set()
        scope = [not marker.add(x.casefold()) and x for x in raw_scope if x.casefold() not in marker]
        post_id = random.randint(0, 100000000)
        insert_post(post_id, target, body, scope)

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' %s ' % locales[target.language_code].and_connector + scope[-1]
        else:
            formatted_scope = scope[0]

        await inline_query.answer([rsc.query_results.mode_for(target.language_code, post_id, body, formatted_scope),
                                   rsc.query_results.mode_except(target.language_code, post_id, body, formatted_scope)],
                                   cache_time = 0)
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query hide from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.inline_handler(lambda query: len(query.query) > 0)
async def inline_query_spoiler(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        body = inline_query.query
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        post_id = random.randint(0, 100000000)
        insert_post(post_id, target, body)
        await inline_query.answer([rsc.query_results.spoiler(target.language_code, post_id, body)])
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query spoiler from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.inline_handler()
async def inline_query_help(inline_query: types.InlineQuery):
    try:
        await inline_query.answer([], switch_pm_text = locales[inline_query.from_user.language_code].how_to_use,
                                  switch_pm_parameter  = 'how_to_use')
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query help from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    try:
        target = call.from_user
        (post_id, mode) = str(call.data).split(' ')
        try:
            post = get_post(post_id)
        except Exception as e:
            logger.error(e)
            logger.warning('#' + post_id + ' cannot be reached by ' + get_formatted_username_or_id(target))
            await bot.answer_callback_query(call.id, text = locales[target.language_code].not_accessible, show_alert = True)
            return

        (_, author, body, scope_string, creation_time) = post
        scope = scope_string.split(' ')
        access_granted = False
        if mode == 'spoiler':
            access_granted = True
        elif mode == 'for':
            if target.username and target.username.lower() in scope:
                access_granted = True
                update_user_in_scope(post_id, target.username.lower(), target.id)
            else:
                access_granted = target.id == author or str(target.id) in scope
        elif mode == 'except':
            if target.username and target.username.lower() in scope:
                update_user_in_scope(post_id, target.username.lower(), target.id)
            else:
                access_granted = str(target.id) not in scope

        if access_granted:
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(target) + ' - access granted')
            await bot.answer_callback_query(call.id, body
                .replace('{username}''{nutzername}', get_formatted_username_or_id(target))
                .replace('{name}''{Name}', target.full_name)                         
                .replace('{uid}''{id}', 'id' + str(target.id))                          
                .replace('{lang}''{sprache}', 'unknown' if target.language_code is None else target.language_code)
                .replace('{pid}', '#' + post_id)
                .replace('{ts}', str(creation_time))                          
                .replace('{now}''{jetzt}', str(datetime.now()))                          
                .replace('{date}''{datum}', datetime.now().strftime('%d-.%m-.%Y'))                         
                .replace('{time}''{zeit}', datetime.now().strftime('%H:%M')),
                True)
        else:
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(target) + ' - access denied')
            await call.answer(locales[target.language_code].not_allowed, True)
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle callback query from ' +
                       get_formatted_username_or_id(call.from_user) + ' '
                       'with payload: "' + call.data + '"')

@dp.message_handler(commands = ['start', 'help', 'info'])
async def send_info(message: types.Message):
    try:
        if message.chat.id in ignored_chat_ids:
            return
        Thread(target = ignore, args = (message.chat.id, 1)).start()
        await message.answer(text = locales[message.from_user.language_code].info_message,
                             reply_markup = rsc.keyboards.info_keyboard(),
                             disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)
        logger.warning('cannot send info to chat_id: ' + message.chat.id)

@dp.my_chat_member_handler(lambda message: message.new_chat_member.status == 'member',
                           chat_type = (types.ChatType.GROUP, types.ChatType.SUPERGROUP))
async def send_group_greeting(message: types.ChatMemberUpdated):
    try:
        bot_user = await bot.get_me()
        await bot.send_sticker(message.chat.id, rsc.media.group_greeting_sticker_id())
        await bot.send_message(message.chat.id,
                               text = locales[message.from_user.language_code].group_greeting_message
                                    % (bot_user.full_name, bot_user.username),
                               parse_mode = 'html',
                               disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        execute_query("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                author INTEGER,
                content TEXT,
                scope TEXT,
                creation_time TIMESTAMP);
                """)

        logger.info('Start polling...')
        executor.start_polling(dp, skip_updates = True)
    except Exception as e:
        logger.error(e)

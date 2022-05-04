import logging
import os
import urllib
from uuid import uuid4
from aiogram import Bot, Dispatcher, executor, types

# полная документация в формате .html
# python -m pydoc -w  main

API_TOKEN = os.getenv('telegram_api_token_wordle')
GAME_NAME = 'wordle'
GAME_URL = urllib.request.urlopen("http://ifconfig.me.").read().decode('utf-8')
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

play_btn = types.InlineKeyboardButton('play', callback_game=types.CallbackGame())
help_btn = types.InlineKeyboardButton('help', callback_data='help')
rules_btn = ta_btn = types.InlineKeyboardButton('rules', callback_data='rules')

keyboard = types.InlineKeyboardMarkup(row_width=3)
keyboard.add(play_btn, help_btn, rules_btn)


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    """Устанавливает клавиатуру, в которой  первая кнопка должна запускать игру."""

    await bot.send_game(message.chat.id, game_short_name=GAME_NAME, reply_markup=keyboard)


@dp.inline_handler()
async def send_game(inline_query: types.InlineQuery):
    """Отправляет ответ на inline query, чтобы игра высвечивалась при вводе  @wordle_rtu_bot."""

    await bot.answer_inline_query(inline_query.id,
                                  [types.InlineQueryResultGame(id=str(uuid4()),
                                                               game_short_name=GAME_NAME)])


@dp.callback_query_handler(lambda message: message.game_short_name == GAME_NAME)
async def process_callback_button1(callback_query: types.CallbackQuery):
    """Перенаправляет юзера на его игру."""

    # print(callback_query.game_short_name)
    print(callback_query)
    # print(callback_query.message)
    user_url = GAME_URL + '?chat_id=%s&user_id=%d' % (callback_query.chat_instance, callback_query.from_user.id)
    print(user_url)
    await bot.answer_callback_query(callback_query.id, url=user_url)


@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_button2(callback_query: types.CallbackQuery):
    """Возвращает юзеру вспомогательную информацию об игре в качестве уведомления вверху экрана."""

    await bot.answer_callback_query(callback_query.id, 'Запустите по кнопке play')


@dp.callback_query_handler(lambda c: c.data == 'rules')
async def process_callback_button3(callback_query: types.CallbackQuery):
    """Возвращает юзеру правила игры в качестве уведомления вверху экрана."""

    await bot.answer_callback_query(callback_query.id, 'Рейтинг будет считаться так-то так-то.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

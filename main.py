import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'token'
GAME_NAME = 'wordle'
GAME_URL = 'url'

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
    await bot.send_game(message.chat.id, game_short_name=GAME_NAME, reply_markup=keyboard)


@dp.callback_query_handler(lambda message: message.game_short_name == GAME_NAME)
async def process_callback_button1(callback_query: types.CallbackQuery):
    print(callback_query.game_short_name)
    await bot.answer_callback_query(callback_query.id, 'игра началась', url=GAME_URL)


@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, 'Запустите по кнопке play')


@dp.callback_query_handler(lambda c: c.data == 'rules')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, 'Рейтинг будет считаться так-то так-то.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

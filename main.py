import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command, CommandObject
from dotenv import load_dotenv
from handlers import router
dp = Dispatcher()

'''@dp.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    if command.args.isdigit():
        if command.args == '242':
            await message.answer(f'Привет! Ты пришел от Рустама')
    else:
        await message.answer('Ошибка')
'''

'''@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Пока что бот ничего не умеет')
    '''

#отправить фото обратно в первоначальном качестве

'''
@dp.message(Command('id'))
async def cmd_help(message: Message):
    await message.answer(f'{message.from_user.first_name}, вам нужна помощь?')
    await message.answer(f'Ваш ID: {message.from_user.id}')
команда id, выдает id пользователя
'''

# код ниже можешь добавлять в каждый проект
async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))  #для дальнейшей разработки в будущем надо делать именно так
    dp = Dispatcher()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)

    await dp.start_polling(bot)


#чтобы красиво было
async def startup(dispatcher: Dispatcher):
    print('starting up...')

async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

# это нужно, чтобы при остановке бота не возникало ошибок на windows
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

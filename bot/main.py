import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor

from bot.database.core.init import init_db_connection
from bot.database.models import InviteCode
from database.invite_codes import get_invite_code, user_got_code, invalidate_invite_code
from database.utils import get_tg_token, get_admin_ids

logging.basicConfig(level="DEBUG")
bot = Bot(token=get_tg_token())
dp = Dispatcher(bot)


@dp.message_handler(CommandStart())
async def _get_token(message: types.Message):
    await message.answer("Привет!")
    if await user_got_code(message.from_user.id):
        await message.answer("Ты уже получил свой код регистрации!")
    else:
        code = await get_invite_code()
        if code is not None:
            await message.answer("Твой код регистрации для Flareboard:")
            await message.answer("`{}`".format(code.code), parse_mode="MarkdownV2")
            await invalidate_invite_code(code, message.from_user.id)
        else:
            await message.answer("Коды закончились :(")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def _upload_codes(message: types.Message):
    if message.from_user.id in get_admin_ids():
        file = await bot.get_file(message.document.file_id)
        await bot.download_file(file.file_path, "invites.txt")

        with open("invites.txt", "r") as f:
            codes = map(lambda line: line.replace("\n", ""), f.readlines())

        for code in codes:
            await InviteCode.create(code=code)

        await message.answer("Файл загружен")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(init_db_connection())
    executor.start_polling(dp, skip_updates=False)

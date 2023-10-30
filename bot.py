import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from calculations import aggregate_salary_data
from config import get_token

logging.basicConfig(level=logging.INFO)
token = get_token()
bot = Bot(token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@dp.message(F.text)
async def process_json_message(message: types.Message):
    try:
        received_json = json.loads(message.text)
        result = await aggregate_salary_data(**received_json)

        result_json = json.dumps(result)
        response_text = json.dumps(result_json).replace("\\", "")[1:-1]

        await message.answer(response_text, parse_mode=ParseMode.HTML)
    except json.JSONDecodeError:
        await message.answer("Error parsing JSON. Please send the correct JSON.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

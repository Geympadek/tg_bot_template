import loader
from loader import dp, bot

from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

@dp.message(Command("start"))
async def on_start(msg: types.Message, state: FSMContext):
    await msg.answer(text="")

@dp.callback_query()
async def on_query(query: CallbackQuery, state: FSMContext):
    pass

async def main():
    await loader.launch()
    pass

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
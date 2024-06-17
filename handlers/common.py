from aiogram import F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder

from replies.text import *
from db import RandomCoffeeDB

router = Router()

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Начало',
    '/profile': 'Как выглядит твой профиль',
    '/acquaintance': 'Анкета',
    '/help': 'Список команд',
}

@router.message(Command(commands=["start"]))
async def welcome(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=go_button,
        callback_data="acquaintance")
    )

    await message.answer(
        text=start_msg,
        reply_markup=builder.as_markup()
    )

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_RU.items()
    ]
    await bot.set_my_commands(main_menu_commands)

@router.message(Command(commands=["help"]))
async def welcome(message: Message, state: FSMContext):
    await message.answer(
        text=help_msg)
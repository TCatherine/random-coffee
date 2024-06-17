from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from replies.text import *

from db import RandomCoffeeDB

router = Router()

async def empty_profile(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Анкета 🌟",
        callback_data="acquaintance")
    )
    await message.answer(
        text=empty_profile_msg,
        reply_markup=builder.as_markup()
    )

async def get_profile(profile: dict, message: Message):
    if profile[6] == "100":
        motivation = "100% Польза"
    elif profile[6] == "50":
        motivation = "50% Польза - 50% Фан"
    else:
        motivation = "100% Фан"
    
    if profile[7].lower() == "both":
        format = "Онлайн/Оффлайн"
    elif profile[7].lower() == "online":
        format = "Онлайн"
    else:
        format = "Оффлайн"

    profile_msg =f"""
    {profile[2]} {emoji_list[profile[0] % len(emoji_list)]}
<b>Профиль:</b> @{profile[3]}

<b>Чем занимается:</b> {profile[4]}
<b>Зацепки для начала разговора:</b> {profile[5]}
<b>От встречи ожидает:</b>  {motivation}
<b>Формат встречи:</b>  {format}
    """
    await message.answer(profile_msg, parse_mode=ParseMode.HTML)


@router.message(Command(commands=["profile"]))
async def profile(message: Message, state: FSMContext):
    db = RandomCoffeeDB('random_coffee.db')
    profile=db.get_profile(message.from_user.id)
    if not profile:
        await empty_profile(message)
    else:
        await get_profile(profile, message)

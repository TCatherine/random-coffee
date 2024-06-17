from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import logging
from urllib.request import urlopen
import json

from db import RandomCoffeeDB
from replies.text import *
from handlers.profile import get_profile

router = Router()
logging.basicConfig(level=logging.DEBUG)

class Profile(StatesGroup):
    name = State()
    telegram_name = State()
    telegram_id = State()
    city = State()
    link = State()
    job = State()
    job_area = State()
    hobby = State()
    birth_day = State()
    motivation = State()
    meeting_format = State()


@router.message(Command(commands=["acquaintance"]))
async def acquaintance(message: Message, state: FSMContext):
    await state.update_data(telegram_name=message.from_user.username)
    await state.update_data(telegram_id=message.from_user.id)
    await message.answer(
        text=name_question,
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Profile.name)


@router.callback_query(F.data == "acquaintance")
async def acquaintance(callback: CallbackQuery, state: FSMContext):
    await state.update_data(telegram_name=callback.from_user.username)
    await state.update_data(telegram_id=callback.from_user.id)
    await callback.message.edit_text(
        f"{callback.message.text}\n\n➪ {go_button}")
    await callback.message.answer(
        text=name_question,
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(Profile.name)
    

@router.message(Profile.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await ask_job_area(message)
    await state.set_state(Profile.job_area)
    # await ask_city(message)
    # await state.set_state(Profile.city)


# async def ask_city(message: Message):
#     builder = InlineKeyboardBuilder()
#     builder.add(InlineKeyboardButton(
#         text=spb_button,
#         callback_data="spb")
#     )
#     await message.answer(
#         text=city_question,
#         reply_markup=builder.as_markup()
#     )


# @router.callback_query(F.data == "spb")
# async def set_city(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text(
#         f"{city_question}\n\n➪ {spb_button}")
#     await state.update_data(city="Санкт-Петербург")
#     await ask_link(callback.message)
#     await state.set_state(Profile.link)


# async def ask_link(message: Message):
#     await message.answer(
#         text=link_question,
#         reply_markup=ReplyKeyboardRemove()
#     )


# @router.message(Profile.link)
# async def set_link(message: Message, state: FSMContext):
#     entities = message.entities
#     is_correct = False
#     if entities:
#         for item in entities:
#             if item.type == 'url':
#                 is_correct = True
#                 await state.update_data(link=item.extract_from(message.text))
#                 await ask_job(message)
#                 await state.set_state(Profile.job)
    
#     if is_correct is False:
#         await message.answer(
#             text=link_error,
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await ask_link(message)
#         await state.set_state(Profile.link)


# async def ask_job(message: Message):
#     await message.answer(
#         text=job_question,
#         reply_markup=ReplyKeyboardRemove()
#     )


# @router.message(Profile.job)
# async def job(message: Message, state: FSMContext):
#     await state.update_data(job=message.text)
#     await ask_job_area(message)
#     await state.set_state(Profile.job_area)


async def ask_job_area(message: Message):
    await message.answer(
        text=job_area_question,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Profile.job_area)
async def set_job_area(message: Message, state: FSMContext):
    await state.update_data(job_area=message.text.lower())
    await ask_hobby(message)
    await state.set_state(Profile.hobby)


async def ask_hobby(message: Message):
    await message.answer(
        text=hobby_question,
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Profile.hobby)
async def set_hobby(message: Message, state: FSMContext):
    await state.update_data(hobby=message.text.lower())
    await ask_motivation(message)
    # await ask_birth_day(message)
    # await state.set_state(Profile.birth_day)


# async def ask_birth_day(message: Message):
#     await message.answer(
#         text=birth_day_question,
#         reply_markup=ReplyKeyboardRemove()
#     )


# @router.message(Profile.birth_day)
# async def set_birth_day(message: Message, state: FSMContext):
#     try:
#         format = "%d.%m.%Y"
#         res = bool(datetime.strptime(message.text, format))
#         await state.update_data(birth_day=message.text.lower())
#         await ask_motivation(message)
#     except ValueError:
#         await message.answer(
#             text=date_error,
#             reply_markup=ReplyKeyboardRemove()
#         )
#         await ask_birth_day(message)
#         await state.set_state(Profile.birth_day)


async def ask_motivation(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="100% Польза",
            callback_data="100% Польза"
        ),
        InlineKeyboardButton(
            text="50% Польза - 50% Фан",
            callback_data="50% Польза - 50% Фан"
        ),
        InlineKeyboardButton(
            text="100% Фан",
            callback_data="100% Фан"
        ),
        width=1
    )
    
    await message.answer(
        text=motivation_question,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "100% Фан")
async def set_motivation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{motivation_question}\n\n➪ 100% Фан")
    await state.update_data(motivation="0")
    await ask_meet_format(callback.message)
    await state.set_state(Profile.meeting_format)

@router.callback_query(F.data == "50% Польза - 50% Фан")
async def set_motivation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{motivation_question}\n\n➪ 50/50")
    await state.update_data(motivation="50")
    await ask_meet_format(callback.message)
    await state.set_state(Profile.meeting_format)

@router.callback_query(F.data == "100% Польза")
async def set_motivation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{motivation_question}\n\n➪ 100% Польза")
    await state.update_data(motivation="100")
    await ask_meet_format(callback.message)
    await state.set_state(Profile.meeting_format)


async def ask_meet_format(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Online",
        callback_data="Online")
    )
    builder.row()
    builder.add(InlineKeyboardButton(
        text="Offline",
        callback_data="Offline")
    )
    builder.row()
    builder.add(InlineKeyboardButton(
        text="Без разница",
        callback_data="Без разницы")
    )
    await message.answer(
        text=meeting_format_question,
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "Online")
async def set_meet_format(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{meeting_format_question}\n\n➪ Online")
    await state.update_data(meeting_format="Online")
    await result(callback.message, state)

@router.callback_query(F.data == "Offline")
async def set_meet_format(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{meeting_format_question}\n\n➪ Offline")
    await state.update_data(meeting_format="Offline")
    await result(callback.message, state)

@router.callback_query(F.data == "Без разницы")
async def set_meet_format(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"{meeting_format_question}\n\n➪ Без разницы")
    await state.update_data(meeting_format="Both")
    await result(callback.message, state)


async def result(message: Message, state: FSMContext):
    data = await state.get_data()
    db = RandomCoffeeDB('random_coffee.db')
    db.insert_data(
        telegram_id=data['telegram_id'],
        name=data['name'],
        telegram_name=data['telegram_name'],
        job_area=data['job_area'],
        hobby=data["hobby"],
        motivation=data['motivation'],
        format=data['meeting_format'] )

    await message.answer(
        text=result_info,
        reply_markup=ReplyKeyboardRemove()
    )
    await get_profile(db.get_profile(data['telegram_id']), message)

from datetime import datetime, timezone, timedelta
import logging
from typing import Dict, Union, Any

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError

from src.db.queries.dao.dao import AsyncOrm
from src.fsm.fsm import FSMStartShift
from src.handlers.user_handler.common import safe_tg_call
from src.keyboards.keyboard import create_cancel_kb, create_places_kb, create_rules_kb
from src.callbacks.place import PlaceCallbackFactory
from src.middleware.album_middleware import AlbumsMiddleware
from src.config import settings
from src.lexicon.lexicon_ru import LEXICON_RU, rules
from src.db import cached_places

router_start_shift = Router()
router_start_shift.message.middleware(middleware=AlbumsMiddleware(2))
logger = logging.getLogger(__name__)


async def report(dictionary: Dict[str, Any], date: str, user_id: Union[str, int]) -> str:
    return f"📝Открытие смены\n\n" \
           f"Дата: {date}\n" \
           f"Точка: {dictionary['place']}\n" \
           f"Имя: {await AsyncOrm.get_current_name(user_id=user_id)}\n"


async def send_report_text(message: Message, data: dict, date: str, chat_id: Union[str, int]):
    return await message.bot.send_message(
        chat_id=chat_id,
        text=await report(
            dictionary=data,
            date=date,
            user_id=message.chat.id,
        ),
        parse_mode="html",
    )


async def send_report(message: Message, state: FSMContext, data: dict, date: str, chat_id: Union[str, int]):
    try:
        await safe_tg_call(
            lambda: send_report_text(
                message=message,
                data=data,
                date=date,
                chat_id=chat_id,
            ),
        )

        await safe_tg_call(
            lambda: message.bot.send_photo(
                chat_id=chat_id,
                photo=data['my_photo'],
                caption='Фото сотрудника',
            ),
        )

        object_photos = [
            InputMediaPhoto(
                media=photo_file_id,
                caption="Фото объекта" if i == 0 else ""
            ) for i, photo_file_id in enumerate(data['object_photo'])
        ]

        await safe_tg_call(
            lambda: message.bot.send_media_group(
                chat_id=chat_id,
                media=object_photos,
            ),
        )

        await message.answer(
            text="Данные успешно записаны!\n"
                 "Передаю руководству отчёт...",
            reply_markup=ReplyKeyboardRemove(),
        )

        await message.answer(
            text="Вы вернулись в главное меню",
        )

    except TelegramAPIError as e:
        logger.exception("Ошибка с телеграм в start_shift.py")
        await message.bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Start shift report error:\n\n{e}",
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.answer(
            text="Упс... что-то пошло не так, сообщите руководству!",
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as e:
        logger.exception("Ошибка не с телеграм в start_shift.py")
        await message.bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"Start shift report error:\n\n{e}",
            reply_markup=ReplyKeyboardRemove(),
        )
        await message.answer(
            text="Упс... что-то пошло не так, сообщите руководству!",
            reply_markup=ReplyKeyboardRemove(),
        )
    finally:
        await state.clear()


@router_start_shift.message(Command(commands="start_shift"), StateFilter(default_state))
async def process_start_shift_command(message: Message, state: FSMContext):
    await message.answer(
        text="Пожалуйста, выберите свою рабочую точку из списка <b>ниже</b>",
        reply_markup=create_places_kb(),
        parse_mode="html",
    )
    await state.set_state(FSMStartShift.place)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), PlaceCallbackFactory.filter())
async def process_place_command(callback: CallbackQuery, callback_data: PlaceCallbackFactory, state: FSMContext):
    await state.update_data(place=callback_data.title)
    await callback.message.delete_reply_markup()
    await callback.message.edit_text(
        text="Пожалуйста, выберите свою рабочую точку из списка <b>ниже</b>\n\n"
             f"➢ {callback_data.title}",
        parse_mode="html",
    )
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=create_rules_kb(),
        parse_mode="html",
    )
    await callback.answer()
    await state.set_state(FSMStartShift.rules)


@router_start_shift.message(StateFilter(FSMStartShift.place))
async def warning_start_shift_command(message: Message):
    await message.answer(
        text="Пожалуйста, выберите рабочую точку из списка",
        reply_markup=create_cancel_kb(),
    )


@router_start_shift.callback_query(StateFilter(FSMStartShift.rules), F.data == "agree")
async def process_rules_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.edit_text(
        text=f"{rules}\n\n"
             "➢ Согласен",
        parse_mode="html",
    )
    await callback.message.answer(
        text="Пожалуйста, сделайте фотографию себя на рабочем месте",
        reply_markup=create_cancel_kb(),
    )
    await callback.answer()
    await state.set_state(FSMStartShift.my_photo)


@router_start_shift.message(StateFilter(FSMStartShift.rules))
async def warning_rules_command(message: Message):
    await message.answer(
        text="Вам нужно ознакомиться с правилами выше и нажать кнопку согласия\n\n"
             'Если Вы хотите выйти из команды, напишите <b>"Отмена"</b>'
             ' или нажмите <b>кнопку "Отмена"</b> внизу экрана',
        reply_markup=create_cancel_kb(),
        parse_mode="html",
    )


@router_start_shift.message(StateFilter(FSMStartShift.my_photo), F.photo)
async def process_my_photo_command(message: Message, state: FSMContext):
    await state.update_data(my_photo=message.photo[-1].file_id)
    await message.answer(
        text="Пожалуйста, сфотографируйте комнату (площадку) с 3-х ракурсов\n"
             "(соответственно, нужно 3 фотографии)",
        reply_markup=create_cancel_kb(),
    )
    await state.set_state(FSMStartShift.object_photo)


@router_start_shift.message(StateFilter(FSMStartShift.my_photo))
async def warning_my_photo_command(message: Message):
    await message.answer(
        text="Пожалуйста, пришлите Ваше фото",
    )


@router_start_shift.message(StateFilter(FSMStartShift.object_photo))
async def process_object_photo_command(message: Message, state: FSMContext):
    if message.photo:
        if 'object_photo' not in await state.get_data():
            await state.update_data(object_photo=[message.photo[-1].file_id])

        start_shift_dict = await state.get_data()

        day_of_week = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime('%A')
        current_date = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime(f'%d/%m/%Y - {LEXICON_RU[day_of_week]}')

        await send_report(
            message=message,
            state=state,
            data=start_shift_dict,
            date=current_date,
            chat_id=cached_places[start_shift_dict['place']],
        )
    else:
        await message.answer(
            text="Нужны фотографии!",
            reply_markup=create_cancel_kb(),
        )

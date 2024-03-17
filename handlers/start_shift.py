from typing import Union
from datetime import datetime, timezone, timedelta

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from fsm.fsm import FSMStartShift
from keyboards.keyboards import create_cancel_kb, create_places_kb, create_agree_kb
from middleware.album_middleware import AlbumsMiddleware
from config.config import config, place_chat
from lexicon.lexicon_ru import LEXICON_RU, rules
from db import DB

router_start_shift = Router()
router_start_shift.message.middleware(middleware=AlbumsMiddleware(2))


async def report(report_dict: dict, date: str, user_id: Union[int, str]) -> str:
    return f"📝Открытие смены\n\n" \
           f"Дата: {date}\n" \
           f"Точка: {report_dict['place']}\n" \
           f"Имя: {DB.get_current_name(user_id)}\n"


@router_start_shift.message(Command(commands="start_shift"), StateFilter(default_state))
async def process_start_shift_command(message: Message, state: FSMContext):
    await state.set_state(FSMStartShift.place)
    await message.answer(
        text="Пожалуйста, выберите рабочую точку",
        reply_markup=await create_places_kb(),
    )


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_ryzanka_room")
async def process_place_1_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка комната")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_ryzanka_square")
async def process_place_2_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_153_room")
async def process_place_3_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 комната")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_153_square")
async def process_place_4_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_cloud_square")
async def process_place_5_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Облака площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_dirt_room")
async def process_place_6_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Черная грязь комната")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_june_square")
async def process_place_7_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Июнь площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_park_kosino")
async def process_place_8_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Косино парк площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_city_kosino")
async def process_place_9_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Город Косино карусель+площадка")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_varskva_room")
async def process_place_10_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Варшавский комната")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_ryazanka_tokens")
async def process_place_11_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Город Рязанка Жетоны")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_kosino_tokens")
async def process_place_12_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Косино Парк Жетоны")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "place_myakinino")
async def process_place_13_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Мякинино")
    await callback.message.answer(
        text=f"{rules}",
        reply_markup=await create_agree_kb(),
        parse_mode="html",
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMStartShift.rules)


@router_start_shift.callback_query(StateFilter(FSMStartShift.place), F.data == "cancel")
async def process_place_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer(text="✅")
    await state.clear()


@router_start_shift.message(StateFilter(FSMStartShift.place))
async def warning_start_shift_command(message: Message):
    await message.answer(
        text="Пожалуйста, выберите рабочую точку из списка выше",
        reply_markup=await create_cancel_kb(),
    )


@router_start_shift.callback_query(StateFilter(FSMStartShift.rules), F.data == "agree")
async def process_rules_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Пожалуйста, сделайте фотографию себя на рабочем месте",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Соглашение принято")
    await state.set_state(FSMStartShift.my_photo)


@router_start_shift.message(StateFilter(FSMStartShift.rules))
async def warning_rules_command(message: Message):
    await message.answer(
        text="Вам нужно ознакомиться с правилами выше и нажать кнопку согласия\n\n"
             'Если Вы хотите выйти из команды, напишите <b>"Отмена"</b>'
             ' или нажмите <b>кнопку "Отмена"</b> внизу экрана',
        reply_markup=await create_cancel_kb(),
        parse_mode="html",
    )


@router_start_shift.message(StateFilter(FSMStartShift.my_photo), F.photo)
async def process_my_photo_command(message: Message, state: FSMContext):
    await state.update_data(my_photo=message.photo[-1].file_id)
    await message.answer(
        text="Пожалуйста, сфотографируйте комнату (площадку) с 3-х ракурсов\n"
             "(соответственно, нужно 3 фотографии)",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMStartShift.object_photo)


@router_start_shift.message(StateFilter(FSMStartShift.my_photo))
async def warning_my_photo_command(message: Message):
    await message.answer(text="Пожалуйста, пришлите Ваше фото")


@router_start_shift.message(StateFilter(FSMStartShift.object_photo), F.photo)
async def process_object_photo_command(message: Message, state: FSMContext, bot: Bot):
    if 'object_photo' not in await state.get_data():
        await state.update_data(object_photo=[message.photo[-1].file_id])

    try:
        start_shift_dict = await state.get_data()

        day_of_week = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime('%A')
        current_date = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime(f'%d/%m/%Y - {LEXICON_RU[day_of_week]}')

        await message.bot.send_message(
            chat_id=place_chat[start_shift_dict['place']],
            text=await report(start_shift_dict, current_date, message.from_user.id),
        )

        await message.bot.send_photo(
            chat_id=place_chat[start_shift_dict['place']],
            photo=start_shift_dict['my_photo'],
            caption='Фото сотрудника',
        )

        object_photos = [InputMediaPhoto(
            media=photo_file_id,
            caption="Фото объекта" if i == 0 else ""
        ) for i, photo_file_id in enumerate(start_shift_dict['object_photo'])]

        await message.bot.send_media_group(
            chat_id=place_chat[start_shift_dict['place']],
            media=object_photos,
        )

        await message.answer(
            text="Данные успешно записаны!\n"
                 "Передаю руководству отчёт...",
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as e:
        await message.answer(
            text="Упс... что-то пошло не так, сообщите руководству!",
            reply_markup=ReplyKeyboardRemove(),
        )
        await bot.send_message(
            chat_id=config.admins[0],
            text=f"Start shift report error:\n\n{e}",
            reply_markup=ReplyKeyboardRemove(),
        )
    finally:
        await state.clear()


@router_start_shift.message(StateFilter(FSMStartShift.object_photo))
async def warning_object_photo_command(message: Message):
    await message.answer(
        text="Нужны фотографии!",
        reply_markup=await create_cancel_kb(),
    )

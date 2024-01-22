from datetime import datetime, timezone, timedelta

from typing import Union

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter, Command

from db import DB
from fsm.fsm import FSMFinishShift
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import create_cancel_kb, create_places_kb, create_yes_no_kb
from middleware.album_middleware import AlbumsMiddleware
from config.config import place_chat, config

from decimal import Decimal
import re

router_finish = Router()
router_finish.message.middleware(middleware=AlbumsMiddleware(2))


async def report(dictionary: dict, date, user_id: Union[str, int]) -> str:
    return "📝Закрытие смены:\n\n"\
           f"Дата: {date}\n" \
           f"Точка: {dictionary['place']}\n" \
           f"Имя: {DB.get_current_name(user_id)}\n" \
           f"Льготники: {dictionary['beneficiaries']}\n" \
           f"Общая выручка: {dictionary['summary']}\n" \
           f"Наличные: {dictionary['cash']}\n" \
           f"Безнал: {dictionary['online_cash']}\n" \
           f"QR-код: {dictionary['qr_code']}\n" \
           f"Расход: {dictionary['expenditure']}\n" \
           f"Зарплата: {dictionary['salary']}\n" \
           f"Инкассация: {dictionary['encashment']}\n\n" \
           f"Общее количество часов посещения: {dictionary['total_hours']}\n" \
           f"Общее количество детей: {dictionary['total_children']}\n\n" \
           f"Общее количество проданных жетонов: {dictionary['total_tokens']}\n" \
           f"Остаток жетонов: {dictionary['remaining_token']}\n\n" \
           f"Количество проката машинок 5 минут (7): {dictionary['count_cars_5']}\n" \
           f"Количество проката машинок 10 минут (20): {dictionary['count_cars_10']}\n\n" \
           f"Количество прокатов на карусели: {dictionary['count_carousel']}\n\n" \
           f"Общее количество мастер-классов: {dictionary['count_master']}\n\n" \
           f"Количество проданного доп.товара: {dictionary['count_additional']}\n"


@router_finish.message(Command(commands="finish_shift"), StateFilter(default_state))
async def process_place_command(message: Message, state: FSMContext):
    await message.answer(
        text="Выберите точку, на которой Вы сейчас находитесь",
        reply_markup=await create_places_kb(),
    )
    await state.set_state(FSMFinishShift.place)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_ryzanka_room")
async def process_place_1_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка комната")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_ryzanka_square")
async def process_place_2_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_153_room")
async def process_place_3_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 комната")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_153_square")
async def process_place_4_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_cloud_square")
async def process_place_5_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Облака площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_dirt_room")
async def process_place_6_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Черная грязь комната")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_june_square")
async def process_place_7_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Июнь площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_park_kosino")
async def process_place_8_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Косино парк площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_city_kosino")
async def process_place_9_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Город Косино карусель+площадка")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "place_varskva_room")
async def process_place_10_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Варшавский комната")
    await callback.message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMFinishShift.summary)


@router_finish.callback_query(StateFilter(FSMFinishShift.place), F.data == "cancel")
async def process_place_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer(text="✅")
    await state.clear()


@router_finish.message(StateFilter(FSMFinishShift.place))
async def warning_place_command(message: Message):
    await message.answer(
        text="Выберите рабочую точку ниже из выпадающего списка",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.summary), F.text)
async def process_summary_command(message: Message, state: FSMContext):
    money_message = message.text.lower()
    pattern = r'\b\w*рубл[ьяей]?\w*\b'

    if "," in message.text:
        money_message = message.text.replace(",", ".")

    money_message = re.sub(pattern, '', money_message)

    await state.update_data(summary=str(Decimal(money_message)))
    await message.answer(
        text="Были ли льготники сегодня?",
        reply_markup=await create_yes_no_kb(),
    )
    await state.set_state(FSMFinishShift.beneficiaries)


@router_finish.message(StateFilter(FSMFinishShift.summary))
async def warning_summary_command(message: Message):
    await message.answer(
        text="Напишите общую выручку за сегодня",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.callback_query(StateFilter(FSMFinishShift.beneficiaries), F.data == "yes")
async def process_beneficiaries_yes_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(beneficiaries="yes")
    await callback.message.answer(
        text="Прикрепите подтвреждающее фото (справка, паспорт родителей)",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="✅")
    await state.set_state(FSMFinishShift.photo_of_beneficiaries)


@router_finish.callback_query(StateFilter(FSMFinishShift.beneficiaries), F.data == "no")
async def process_beneficiaries_no_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(beneficiaries="no")
    await callback.message.answer(
        text="Напишите сумму наличных за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="✅")
    await state.set_state(FSMFinishShift.cash)


@router_finish.callback_query(StateFilter(FSMFinishShift.beneficiaries), F.data == "cancel")
async def process_beneficiaries_cancel_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer(text="✅")


@router_finish.message(StateFilter(FSMFinishShift.photo_of_beneficiaries))
async def process_photo_beneficiaries_command(message: Message, state: FSMContext):
    if message.photo:
        if "photo_beneficiaries" not in await state.get_data():
            await state.update_data(photo_of_beneficiaries=[message.photo[-1].file_id])

        await message.answer(
            text="Напишите сумму наличных за сегодня",
            reply_markup=await create_cancel_kb(),
        )
        await state.set_state(FSMFinishShift.cash)
    else:
        await message.answer(
            text="Прикрепите подтвреждающее фото (справка, паспорт родителей)",
            reply_markup=await create_cancel_kb(),
        )


@router_finish.message(StateFilter(FSMFinishShift.cash), F.text)
async def process_cash_command(message: Message, state: FSMContext):
    await state.update_data(cash=message.text)
    await message.answer(
        text="Напишите сумму безнала за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.online_cash)


@router_finish.message(StateFilter(FSMFinishShift.cash))
async def warning_cash_command(message: Message):
    await message.answer(
        text="Напишите сумму наличных за сегодня",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.online_cash), F.text)
async def process_online_cash_command(message: Message, state: FSMContext):
    await state.update_data(online_cash=message.text)
    await message.answer(
        text="Напишите сумму по QR-коду за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.qr_code)


@router_finish.message(StateFilter(FSMFinishShift.online_cash))
async def warning_online_cash_command(message: Message):
    await message.answer(
        text="Напишите сумму безнала за сегодня",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.qr_code), F.text)
async def process_qr_code_command(message: Message, state: FSMContext):
    await state.update_data(qr_code=message.text)
    await message.answer(
        text="Напишите, сколько суммарно вышло на расход за сегодня",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.expenditure)


@router_finish.message(StateFilter(FSMFinishShift.qr_code))
async def warning_qr_code_command(message: Message):
    await message.answer(
        text="Напишите сумму по QR-коду за сегодня",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.expenditure), F.text)
async def process_expenditure_command(message: Message, state: FSMContext):
    await state.update_data(expenditure=message.text)
    await message.answer(
        text="Напишите, сколько вы взяли ЗП за сегодня\n\n"
             "Если вы <b>не</b> брали ЗП, напишите 0",
        reply_markup=await create_cancel_kb(),
        parse_mode="html",
    )
    await state.set_state(FSMFinishShift.salary)


@router_finish.message(StateFilter(FSMFinishShift.expenditure))
async def warning_expenditure_command(message: Message):
    await message.answer(
        text="Напишите, сколько суммарно вышло на расход за сегодня",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.salary), F.text)
async def process_salary_command(message: Message, state: FSMContext):
    msg = message.text

    if msg == "0":
        await state.update_data(salary=msg)
    else:
        await state.update_data(salary=message.text)

    await message.answer(
        text="Напишите сумму инкассации\n\n"
             "Если инкассации <b>нет</b>, напишите 0",
        reply_markup=await create_cancel_kb(),
        parse_mode="html",
    )
    await state.set_state(FSMFinishShift.encashment)


@router_finish.message(StateFilter(FSMFinishShift.salary))
async def warning_salary_command(message: Message):
    await message.answer(
        text="Напишите, сколько вы взяли ЗП за сегодня\n\n"
             "Если вы <b>не</b> брали ЗП, напишите 0",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.encashment), F.text)
async def process_encashment_command(message: Message, state: FSMContext):
    await state.update_data(encashment=message.text)
    await message.answer(
        text="Напишите общее количество часов посещения за день",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.total_hours)


@router_finish.message(StateFilter(FSMFinishShift.encashment))
async def warning_encashment_command(message: Message):
    await message.answer(
        text="Напишите сумму инкассации\n\n"
             "Если инкассации <b>нет</b>, напишите 0",
        reply_markup=await create_cancel_kb(),
        parse_mode="html",
    )


@router_finish.message(StateFilter(FSMFinishShift.total_hours), F.text)
async def process_total_hours_command(message: Message, state: FSMContext):
    await state.update_data(total_hours=message.text)
    await message.answer(
        text="Напишите общее количество детей за день",
        reply_markup=await create_cancel_kb()
    )
    await state.set_state(FSMFinishShift.total_children)


@router_finish.message(StateFilter(FSMFinishShift.total_hours))
async def warning_total_hours_command(message: Message):
    await message.answer(
        text="Напишите общее количество часов посещения за день",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.total_children), F.text.isdigit())
async def process_total_child_command(message: Message, state: FSMContext):
    await state.update_data(total_children=message.text)
    await message.answer(
        text="Напишите общее количество проданных жетонов",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.total_tokens)


@router_finish.message(StateFilter(FSMFinishShift.total_children))
async def warning_total_child_command(message: Message):
    await message.answer(
        text="Напишите общее количество детей за день",
        reply_markup=await create_cancel_kb()
    )


@router_finish.message(StateFilter(FSMFinishShift.total_tokens), F.text)
async def process_total_tokens_command(message: Message, state: FSMContext):
    await state.update_data(total_tokens=message.text)
    await message.answer(
        text="Напишите остаток жетонов",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.remaining_tokens)


@router_finish.message(StateFilter(FSMFinishShift.total_tokens))
async def warning_total_tokens_command(message: Message):
    await message.answer(
        text="Напишите общее количество проданных жетонов",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.remaining_tokens), F.text)
async def process_remaining_token_command(message: Message, state: FSMContext):
    await state.update_data(remaining_token=message.text)
    await message.answer(
        text="Напишите количество проката машинок 5 минут (7 минут)",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.count_cars_5)


@router_finish.message(StateFilter(FSMFinishShift.remaining_tokens))
async def warning_remaining_tokens_command(message: Message):
    await message.answer(
        text="Напишите остаток жетонов",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.count_cars_5), F.text)
async def process_cars_5_command(message: Message, state: FSMContext):
    await state.update_data(count_cars_5=message.text)
    await message.answer(
        text="Напишите количество проката машинок 10 минут (20 минут)",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.count_cars_10)


@router_finish.message(StateFilter(FSMFinishShift.count_cars_5))
async def warning_cars_5_command(message: Message):
    await message.answer(
        text="Напишите количество проката машинок 5 минут (7 минут)",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.count_cars_10), F.text)
async def process_cars_10_command(message: Message, state: FSMContext):
    await state.update_data(count_cars_10=message.text)
    await message.answer(
        text="Напишите количество прокатов на карусели",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.count_carousel)


@router_finish.message(StateFilter(FSMFinishShift.count_cars_10))
async def warning_cars_10_command(message: Message):
    await message.answer(
        text="Напишите количество проката машинок 10 минут (20 минут)",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.count_carousel), F.text)
async def process_carousel_command(message: Message, state: FSMContext):
    await state.update_data(count_carousel=message.text)
    await message.answer(
        text="Напишите общее количество мастер-классов за день",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.count_master)


@router_finish.message(StateFilter(FSMFinishShift.count_carousel))
async def warning_carousel_command(message: Message):
    await message.answer(
        text="Напишите количество прокатов на карусели",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.count_master), F.text)
async def process_master_class_command(message: Message, state: FSMContext):
    await state.update_data(count_master=message.text)
    await message.answer(
        text="Напишите общее количество продаж доп.товара за день\n(шарики, слаймы и т.д)",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.count_additional)


@router_finish.message(StateFilter(FSMFinishShift.count_master))
async def warning_master_class_command(message: Message):
    await message.answer(
        text="Напишите общее количество мастер-классов за день",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.count_additional), F.text)
async def process_count_additional_command(message: Message, state: FSMContext):
    await state.update_data(count_additional=message.text)
    await message.answer(
        text="Прикрепите чеки и необходимые фотографии за смену "
             "(чеки о закрытии смены, оплата QR-кода, чек расхода)",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMFinishShift.necessary_photos)


@router_finish.message(StateFilter(FSMFinishShift.count_additional))
async def warning_count_additional_command(message: Message):
    await message.answer(
        text="Напишите общее количество продаж доп.товара за день\n(шарики, слаймы и т.д)",
        reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.necessary_photos))
async def process_necessary_photos_command(message: Message, state: FSMContext):
    if message.photo:
        if "necessary_photos" not in await state.get_data():
            await state.update_data(necessary_photos=[message.photo[-1].file_id])

        await message.answer(
            text="Сфотографируйте тетрадь (остатки товара на складе)",
            reply_markup=await create_cancel_kb(),
        )
        await state.set_state(FSMFinishShift.photo_copybook)
    else:
        await message.answer(
            text="Прикрепите чеки и необходимые фотографии за смену "
                 "(чеки о закрытии смены, оплата QR-кода, чек расхода)",
            reply_markup=await create_cancel_kb(),
    )


@router_finish.message(StateFilter(FSMFinishShift.photo_copybook))
async def process_photo_copybook_command(message: Message, state: FSMContext):
    if message.photo:
        if "photo_copybook" not in await state.get_data():
            await state.update_data(photo_copybook=[message.photo[-1].file_id])

        await message.answer(
            text="Сфотографируйте комнату (площадку) (1 фото)",
            reply_markup=await create_cancel_kb(),
        )

        await state.set_state(FSMFinishShift.object_photo)
    else:
        await message.answer(
            text="Сфотографируйте тетрадь (остатки товара на складе)",
            reply_markup=await create_cancel_kb(),
        )


@router_finish.message(StateFilter(FSMFinishShift.object_photo))
async def process_object_photo_command(message: Message, state: FSMContext):
    if message.photo:
        if "object_photo" not in await state.get_data():
            await state.update_data(object_photo=[message.photo[-1].file_id])

        finish_shift_dict = await state.get_data()

        try:
            day_of_week = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime('%A')
            current_date = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime(f'%d/%m/%Y - {LEXICON_RU[day_of_week]}')

            DB.set_data(
                user_id=message.from_user.id,
                date=datetime.now(tz=timezone(timedelta(hours=3.0))).strftime("%Y.%m.%d"),
                place=finish_shift_dict["place"],
                cash=finish_shift_dict["summary"]
            )

            necessary_photos = [InputMediaPhoto(
                media=photo_file_id,
                caption="Необходимые фото за смену (чеки о закрытии смены, оплата QR-кода, "
                        "чек расхода)",
            ) for i, photo_file_id in enumerate(finish_shift_dict["necessary_photos"])]

            photos_copybook = [InputMediaPhoto(
                media=photo_file_id,
                caption="Фото тетради" if i == 0 else ""
            ) for i, photo_file_id in enumerate(finish_shift_dict["photo_copybook"])]

            photos_object = [InputMediaPhoto(
                media=photo_file_id,
                caption="Фото объекта" if i == 0 else ""
            ) for i, photo_file_id in enumerate(finish_shift_dict["object_photo"])]

            await message.bot.send_message(
                chat_id=place_chat[finish_shift_dict["place"]],
                text=await report(
                    dictionary=finish_shift_dict,
                    date=current_date,
                    user_id=message.from_user.id,
                )
            )

            await message.bot.send_media_group(
                media=necessary_photos,
                chat_id=place_chat[finish_shift_dict["place"]],
            )

            if "photo_of_beneficiaries" in finish_shift_dict:
                photo_of_beneficiaries = [InputMediaPhoto(
                    media=photo_file_id,
                    caption="Необходимые фото льготников",
                ) for i, photo_file_id in enumerate(finish_shift_dict["photo_of_beneficiaries"])]

                await message.bot.send_media_group(
                    media=photo_of_beneficiaries,
                    chat_id=place_chat[finish_shift_dict["place"]],
                )

            await message.bot.send_media_group(
                media=photos_copybook,
                chat_id=place_chat[finish_shift_dict["place"]],
            )

            await message.bot.send_media_group(
                media=photos_object,
                chat_id=place_chat[finish_shift_dict["place"]],
            )

            await message.answer(
                text="Отлично! Формирую отчёт...\nОтправляю начальству!",
                reply_markup=ReplyKeyboardRemove(),
            )

        except Exception as e:
            await message.bot.send_message(
                text=f"Check attractions report error: {e}\n"
                     f"User_id: {message.from_user.id}",
                chat_id=config.admins[0],
                reply_markup=ReplyKeyboardRemove(),
            )
            await message.answer(
                text="Упс... что-то пошло не так, сообщите руководству!",
                reply_markup=ReplyKeyboardRemove(),
            )
        finally:
            await state.clear()
    else:
        await message.answer(
            text="Сфотографируйте комнату (площадку) (1 фото)",
            reply_markup=await create_cancel_kb(),
        )


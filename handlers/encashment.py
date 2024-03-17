from datetime import datetime, timedelta, timezone

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from config.config import config
from fsm.fsm import FSMEncashment
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import create_cancel_kb, create_places_kb, create_yes_no_kb
from middleware.album_middleware import AlbumsMiddleware
from config.config import place_chat

router_encashment = Router()
router_encashment.message.middleware(middleware=AlbumsMiddleware(2))


async def report(dictionary: dict, date):
    return "📝Инкассация:\n\n" \
           f"Точка: {dictionary['place']}\n" \
           f"Дата: {date}\n\n" \
           f"Дата инкассации: {dictionary['date']}\n" \
           f"Сумма инкассации: {dictionary['summary']}\n"


@router_encashment.message(Command(commands="encashment"), StateFilter(default_state))
async def process_place_command(message: Message, state: FSMContext):
    await state.set_state(FSMEncashment.place)
    await message.answer(
        text="Выберите точку, на которой Вы сейчас находитесь",
        reply_markup=await create_places_kb(),
    )


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_ryzanka_room")
async def process_place_1_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка комната")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_ryzanka_square")
async def process_place_2_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Рязанка площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_153_room")
async def process_place_3_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 комната")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_153_square")
async def process_place_4_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Л-153 площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_cloud_square")
async def process_place_5_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Облака площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_dirt_room")
async def process_place_6_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Черная грязь комната")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_june_square")
async def process_place_7_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Июнь площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_park_kosino")
async def process_place_8_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Косино парк площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_city_kosino")
async def process_place_9_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Город Косино карусель+площадка")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_varskva_room")
async def process_place_10_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Варшавский комната")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_ryazanka_tokens")
async def process_place_11_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Город Рязанка Жетоны")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_kosino_tokens")
async def process_place_12_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Косино Парк Жетоны")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "place_myakinino")
async def process_place_13_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place="Мякинино")
    await callback.message.answer(
        text="У вас есть инкассация за вчерашний день?",
        reply_markup=await create_yes_no_kb(),
    )
    await callback.answer(text="Рабочая точка успешно записана")
    await state.set_state(FSMEncashment.encashment)


@router_encashment.callback_query(StateFilter(FSMEncashment.place), F.data == "cancel")
async def process_place_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer(text="✅")
    await state.clear()


@router_encashment.message(StateFilter(FSMEncashment.place))
async def warning_place_command(message: Message):
    await message.answer(
        text="Выберите рабочую точку ниже из выпадающего списка",
        reply_markup=await create_cancel_kb(),
    )


@router_encashment.callback_query(StateFilter(FSMEncashment.encashment), F.data == "yes")
async def process_yes_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_encashment="yes")
    await callback.message.answer(
        text="Пожалуйста, сфотографируйте чек",
        reply_markup=await create_cancel_kb(),
    )
    await callback.answer(text="✅")
    await state.set_state(FSMEncashment.photo_of_check)


@router_encashment.callback_query(StateFilter(FSMEncashment.encashment), F.data == "no")
async def process_no_command(callback: CallbackQuery, state: FSMContext):
    await state.update_data(is_encashment="no")

    encashment_dict = await state.get_data()

    day_of_week = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime('%A')
    date = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime(f'%d/%m/%Y - {LEXICON_RU[day_of_week]}')

    try:
        await callback.message.bot.send_message(
            chat_id=place_chat[encashment_dict['place']],
            text="📝Инкассация:\n\n"
                 f"Точка: {encashment_dict['place']}\n"
                 f"Дата: {date}\n\n"
                 "Инкассации <b>нет</b>",
            parse_mode="html")

        await callback.message.answer(
            text="Отлично, все данные отправлены начальству!",
            reply_markup=ReplyKeyboardRemove())
        await callback.answer(text="✅")

    except Exception as e:
        await callback.message.bot.send_message(
            text=f"Encashment report error: {e}\n"
                 f"User_id: {callback.message.from_user.id}",
            chat_id=config.admins[0],
            reply_markup=ReplyKeyboardRemove())
        await callback.message.answer(
            text="Упс... что-то пошло не так, сообщите руководству!",
            reply_markup=ReplyKeyboardRemove())

    finally:
        await state.clear()


@router_encashment.callback_query(StateFilter(FSMEncashment.encashment), F.data == "cancel")
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=ReplyKeyboardRemove(),
    )
    await callback.answer("✅")


@router_encashment.message(StateFilter(FSMEncashment.encashment))
async def warning_yes_no_command(message: Message):
    await message.answer(text="Выберите нужную кнопку из выпадающего списка выше!")


@router_encashment.message(StateFilter(FSMEncashment.photo_of_check))
async def process_wait_for_check_command(message: Message, state: FSMContext):
    if message.photo:
        if 'photo_of_check' not in await state.get_data():
            await state.update_data(photo_of_check=[message.photo[-1].file_id])

        await message.answer(
            text="Отлично, а теперь пришлите сумму инкассации числом",
            reply_markup=await create_cancel_kb(),
        )
        await state.set_state(FSMEncashment.summary)
    else:
        await message.answer(
            text="Это не похоже на фото\n"
                 "Отправьте фото чека инкассации",
            reply_markup=await create_cancel_kb(),
        )


@router_encashment.message(StateFilter(FSMEncashment.summary), F.text)
async def process_wait_for_summary_command(message: Message, state: FSMContext):
    await state.update_data(summary=message.text)
    await message.answer(
        text="Отлично, а теперь пришлите дату, за которую делали инкассацию",
        reply_markup=await create_cancel_kb(),
    )
    await state.set_state(FSMEncashment.date_of_cash)


@router_encashment.message(StateFilter(FSMEncashment.summary))
async def warning_wait_for_summary_command(message: Message):
    await message.answer(
        text="Пришлите сумму инкассации числом!",
        reply_markup=await create_cancel_kb(),
    )


@router_encashment.message(StateFilter(FSMEncashment.date_of_cash), F.text)
async def process_wait_for_date_command(message: Message, state: FSMContext):
    await state.update_data(date=message.text)

    encashment_dict = await state.get_data()

    day_of_week = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime('%A')
    date = datetime.now(tz=timezone(timedelta(hours=3.0))).strftime(f'%d/%m/%Y - {LEXICON_RU[day_of_week]}')

    try:
        await message.bot.send_message(
            chat_id=place_chat[encashment_dict['place']],
            text=await report(
                dictionary=encashment_dict,
                date=date
            ),
        )

        if not isinstance(encashment_dict['photo_of_check'], str):
            media_check = [InputMediaPhoto(
                media=photo_file_id,
                caption="Фото чека инкассации" if i == 0 else "")
                for i, photo_file_id in enumerate(encashment_dict['photo_of_check'])]
            await message.bot.send_media_group(
                chat_id=place_chat[encashment_dict['place']],
                media=media_check,
            )

        await message.answer(
            text="Отлично, все данные отправлены начальству!",
            reply_markup=ReplyKeyboardRemove(),
        )
    except Exception as e:
        await message.bot.send_message(
            text=f"Encashment report error: {e}\n"
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


@router_encashment.message(StateFilter(FSMEncashment.date_of_cash))
async def warning_wait_for_date_command(message: Message):
    await message.answer(
        text="Отправьте дату инкассации!",
        reply_markup=await create_cancel_kb(),
    )

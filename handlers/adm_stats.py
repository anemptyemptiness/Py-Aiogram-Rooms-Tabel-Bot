from datetime import datetime, timezone, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from db import DB
from fsm.fsm import FSMAdmin
from filters.is_admin import isAdminFilter
from config.config import config
from keyboards.keyboards import create_admin_kb

router_adm = Router()


async def report_money_in_range(date_from: str, date_to: str, msg: Message):
    rows = DB.get_statistics_money(
        date_from=date_from,
        date_to=date_to
    )

    year_from, month_from, day_from = date_from.split(".")
    year_to, month_to, day_to = date_to.split(".")

    places = {
        "Рязанка комната": sum([row[0].count("Рязанка комната") for row in rows]),
        "Рязанка площадка": sum([row[0].count("Рязанка площадка") for row in rows]),
        "Л-153 комната": sum([row[0].count("Л-153 комната") for row in rows]),
        "Л-153 площадка": sum([row[0].count("Л-153 площадка") for row in rows]),
        "Облака площадка": sum([row[0].count("Облака площадка") for row in rows]),
        "Черная грязь комната": sum([row[0].count("Черная грязь комната") for row in rows]),
        "Июнь площадка": sum([row[0].count("Июнь площадка") for row in rows]),
        "Косино парк площадка": sum([row[0].count("Косино парк площадка") for row in rows]),
        "Город Косино карусель+площадка": sum([row[0].count("Город Косино карусель+площадка") for row in rows]),
        "Варшавский комната": sum([row[0].count("Варшавский комната") for row in rows]),
    }

    report = f"📊Статистика по приходу финансов на точках\n<b>от</b> {day_from}.{month_from}.{year_from}" \
             f" <b>до</b> {day_to}.{month_to}.{year_to}\n\n"
    index_place = 0
    index_rows = 0

    for key in sorted(places.keys()):
        if places[key]:
            report += f"Рабочая точка: <b>{rows[index_place][0]}</b>\n"

            for i in range(places[key]):
                report += f"📝Работник: <em>{rows[index_rows][1]}</em>\n└"
                report += f"выручка: <em>{rows[index_rows][3]}</em> <b>₽</b>\n"

                index_rows += 1

            report += "\n"
            index_place += places[key]

    total_money = DB.get_total_money(
        date_from=date_from,
        date_to=date_to
    )

    await msg.answer(
        text=f"{report}"
             f"💰Суммарно денег заработано:\n└<em>{total_money}</em> <b>₽</b>",
        parse_mode="html",
        reply_markup=await create_admin_kb(),
    )


@router_adm.message(Command(commands="stats"), isAdminFilter(config.admins))
async def get_money_menu(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.money)
    await message.answer(
        text="💵Выберите временной диапазон",
        reply_markup=await create_admin_kb(),
    )


@router_adm.callback_query(isAdminFilter(config.admins), StateFilter(FSMAdmin.money), F.data == "last_week")
async def get_stats_week_money(callback: CallbackQuery, bot: Bot):
    try:
        date_to = datetime.now(tz=timezone(timedelta(hours=3.0)))
        date_from = date_to - timedelta(days=7)

        await callback.answer(text="⏳")

        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )

        await report_money_in_range(date_from.strftime("%Y.%m.%d"), date_to.strftime("%Y.%m.%d"), callback.message)
    except Exception as e:
        await callback.message.bot.send_message(
            text=f"Get stats-money last week error: {e}\n"
                 f"User_id: {callback.message.from_user.id}",
            chat_id=config.admins[0],
        )
        await callback.message.answer(
            text="⚠️ ВНИМАНИЕ ⚠️\n\n"
                 "Возникла <b>ошибка</b> при сборе данных, "
                 "проверьте правильность введенных значений и повторите команду",
            parse_mode="html",
        )


@router_adm.callback_query(isAdminFilter(config.admins), StateFilter(FSMAdmin.money), F.data == "last_month")
async def get_stats_month_money(callback: CallbackQuery, bot: Bot):
    try:
        date_to = datetime.now(tz=timezone(timedelta(hours=3.0)))
        date_from = date_to - timedelta(days=30)

        await callback.answer(text="⏳")

        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )

        await report_money_in_range(date_from.strftime("%Y.%m.%d"), date_to.strftime("%Y.%m.%d"), callback.message)
    except Exception as e:
        await callback.message.bot.send_message(
            text=f"Get stats-money last month error: {e}\n"
                 f"User_id: {callback.message.from_user.id}",
            chat_id=config.admins[0],
        )
        await callback.message.answer(
            text="⚠️ ВНИМАНИЕ ⚠️\n\n"
                 "Возникла <b>ошибка</b> при сборе данных, "
                 "проверьте правильность введенных значений и повторите команду",
            parse_mode="html",
        )


@router_adm.callback_query(isAdminFilter(config.admins), StateFilter(FSMAdmin.money), F.data == "last_year")
async def get_stats_year_money(callback: CallbackQuery, bot: Bot):
    try:
        date_to = datetime.now(tz=timezone(timedelta(hours=3.0)))
        date_from = date_to - timedelta(days=365)

        await callback.answer(text="⏳")

        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )

        await report_money_in_range(date_from.strftime("%Y.%m.%d"), date_to.strftime("%Y.%m.%d"), callback.message)
    except Exception as e:
        await callback.message.bot.send_message(
            text=f"Get stats-money last year error: {e}\n"
                 f"User_id: {callback.message.from_user.id}",
            chat_id=config.admins[0],
        )
        await callback.message.answer(
            text="⚠️ ВНИМАНИЕ ⚠️\n\n"
                 "Возникла <b>ошибка</b> при сборе данных, "
                 "проверьте правильность введенных значений и повторите команду",
            parse_mode="html",
        )


@router_adm.callback_query(isAdminFilter(config.admins), StateFilter(FSMAdmin.money), F.data == "by_hand")
async def prepare_for_get_stats_money_by_hand(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(FSMAdmin.money_by_hand)
    await callback.answer(text="👌🏻")
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text="⏳Введите диапазон дат <b>через пробел</b>\n\n"
             "Например: <em>31.12.2023 06.01.2024</em>",
        parse_mode="html",
    )


@router_adm.message(isAdminFilter(config.admins), StateFilter(FSMAdmin.money_by_hand), F.text)
async def get_stats_money_by_hand(message: Message, bot: Bot):
    try:
        date_from, date_to = message.text.split()
        day_from, month_from, year_from = date_from.split(".")
        day_to, month_to, year_to = date_to.split(".")

        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id,
        )

        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id - 1,
        )

        await report_money_in_range(f"{year_from}.{month_from}.{day_from}",
                                    f"{year_to}.{month_to}.{day_to}", message)
    except Exception as e:
        await message.bot.send_message(
            text=f"Get stats-money by hand error: {e}\n"
                 f"User_id: {message.from_user.id}",
            chat_id=config.admins[0],
        )
        await message.answer(
            text="⚠️ ВНИМАНИЕ ⚠️\n\n"
                 "Возникла <b>ошибка</b> при сборе данных, "
                 "проверьте правильность введенных значений и повторите команду",
            parse_mode="html",
        )


@router_adm.message(isAdminFilter(config.admins), StateFilter(FSMAdmin.money_by_hand))
async def warning_get_stats_money_by_hand(message: Message):
    await message.answer(
        text="⏳Введите диапазон дат <b>через пробел</b>\n\n"
             "Например: <em>31.12.2023 06.01.2024</em>",
        parse_mode="html",
    )


@router_adm.callback_query(
    isAdminFilter(config.admins),
    F.data == "exit"
)
async def adm_cancel_command(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer(text="👋")
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await callback.message.answer(
        text="Вы вернулись в главное меню",
    )
    await state.clear()

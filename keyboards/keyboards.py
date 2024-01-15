from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


async def create_yes_no_kb() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Да",
                              callback_data="yes"),
         InlineKeyboardButton(text="Нет",
                              callback_data="no")],
        [InlineKeyboardButton(text="Отмена",
                              callback_data="cancel")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


async def create_cancel_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Отмена")]
    ]

    return ReplyKeyboardMarkup(keyboard=kb,
                               resize_keyboard=True)


async def create_places_kb() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(
            text="Рязанка комната",
            callback_data="place_ryzanka_room",
        )], [InlineKeyboardButton(
            text="Рязанка площадка",
            callback_data="place_ryzanka_square",
        )],
        [InlineKeyboardButton(
            text="Л-153 комната",
            callback_data="place_153_room",
        )], [InlineKeyboardButton(
            text="Л-153 площадка",
            callback_data="place_153_square",
        )],
        [InlineKeyboardButton(
            text="Облака площадка",
            callback_data="place_cloud_square",
        )], [InlineKeyboardButton(
            text="Черная грязь комната",
            callback_data="place_dirt_room",
        )],
        [InlineKeyboardButton(
            text="Июнь площадка",
            callback_data="place_june_square",
        )], [InlineKeyboardButton(
            text="Косино парк площадка",
            callback_data="place_park_kosino",
        )],
        [InlineKeyboardButton(
            text="Город Косино карусель+площадка",
            callback_data="place_city_kosino",
        )], [InlineKeyboardButton(
            text="Варшавский комната",
            callback_data="place_varskva_room",
        )],
        [InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


async def create_agree_kb() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(
            text="Согласен",
            callback_data="agree")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)


async def create_admin_kb() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(
            text="Статистика за последнюю неделю",
            callback_data="last_week",
        )],
        [InlineKeyboardButton(
            text="Статистика за последний месяц",
            callback_data="last_month",
        )],
        [InlineKeyboardButton(
            text="Статистика за последний год",
            callback_data="last_year",
        )],
        [InlineKeyboardButton(
            text="Задать вручную",
            callback_data="by_hand",
        )],
        [InlineKeyboardButton(
            text="Назад",
            callback_data="back",
        )],
        [InlineKeyboardButton(
            text="Выход",
            callback_data="exit",
        )],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)

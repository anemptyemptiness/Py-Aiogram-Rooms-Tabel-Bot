from aiogram.fsm.state import StatesGroup, State


class Authorise(StatesGroup):
    fullname = State()


class FSMStartShift(StatesGroup):
    place = State()
    rules = State()
    my_photo = State()
    object_photo = State()


class FSMEncashment(StatesGroup):
    encashment = State()
    place = State()
    photo_of_check = State()
    summary = State()
    date_of_cash = State()


class FSMAttractionsCheck(StatesGroup):
    place = State()
    bill_acceptor = State()
    defects_on_bill_acceptor = State()
    attracts = State()
    defects_on_attracts = State()


class FSMFinishShift(StatesGroup):
    place = State()
    summary = State()
    beneficiaries = State()
    photo_of_beneficiaries = State()
    cash = State()
    online_cash = State()
    qr_code = State()
    expenditure = State()
    salary = State()
    encashment = State()
    total_hours = State()
    total_children = State()
    total_tokens = State()
    remaining_tokens = State()
    count_cars_5 = State()
    count_cars_10 = State()
    count_carousel = State()
    count_master = State()
    count_additional = State()
    necessary_photos = State()
    photo_copybook = State()
    object_photo = State()


class FSMAdmin(StatesGroup):
    stats = State()
    money = State()
    money_by_hand = State()

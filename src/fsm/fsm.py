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
    visitors = State()
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
    # главное меню
    in_adm = State()

    # добавление сотрудника в БД
    add_employee_id = State()
    add_employee_name = State()
    add_employee_username = State()
    add_employee_phone = State()
    check_employee = State()
    rename_employee = State()
    reid_employee = State()
    reusername_employee = State()

    # удаление сотрудника из БД
    which_employee_to_delete = State()
    deleting_employee = State()

    # получить список сотрудников
    watching_employees = State()
    current_employee = State()

    # добавить админа в БД
    add_admin_id = State()
    add_admin_name = State()
    add_admin_username = State()
    add_admin_phone = State()
    check_admin = State()
    rename_admin = State()
    reid_admin = State()
    reusername_admin = State()

    # удалить админа в БД
    which_admin_to_delete = State()
    deleting_admin = State()

    # получить список админов
    watching_admin = State()
    current_admin = State()

    # добавить рабочую точку в БД
    add_place = State()
    add_place_id = State()
    check_place = State()
    rename_place = State()
    reid_place = State()

    # удалить рабочую точку в БД
    which_place_to_delete = State()
    deleting_place = State()

    # получить список рабочих точек
    watching_place = State()
    current_place = State()


class FSMStatistics(StatesGroup):
    in_stats = State()
    go_back = State()
    exit = State()


class FSMStatisticsVisitors(StatesGroup):
    in_stats = State()
    custom_date = State()


class FSMStatisticsMoney(StatesGroup):
    in_stats = State()
    custom_date = State()

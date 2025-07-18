# app/states/admin.py

from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    choose_action = State()
    
    city_name = State()

    product_city = State()
    product_name = State()

    area_product = State()
    area_name = State()

    amount_area = State()
    amount_label = State()
    amount_price = State()

    editing_note = State()

    refund_user_id = State()
    balance_user_id = State()
    balance_amount = State()

    lookup_user = State()

    remove_city = State()
    remove_product = State()
    remove_area = State()
    remove_amount = State()

    edit_amount_select = State()
    edit_amount_image = State()
    edit_amount_description = State()
    edit_amount_note = State()
    edit_amount_remove_option = State() 
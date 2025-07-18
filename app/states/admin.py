# app/states/admin.py

from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    '''
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
'''
    choose_action = State()

    # City
    city_add = State()
    city_remove = State()

    # Product
    product_choose_city = State()
    product_add = State()
    product_remove = State()

    # Area
    area_choose_city = State()
    area_add = State()
    area_remove = State()

    # Amount
    amount_choose_city = State()
    amount_choose_area = State()
    amount_choose_product = State()
    amount_add = State()
    amount_remove = State()

    # Image / Description / Delivery Note
    image_choose_amount = State()
    set_image = State()
    set_description = State()
    set_delivery_note = State()
    remove_image_or_note = State()

    # Other
    broadcast_text = State()
    balance_user = State()
    balance_amount = State()
    refund_user = State()
    lookup_user = State()
    bot_stats = State()
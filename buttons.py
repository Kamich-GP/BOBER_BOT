from telebot import types


# Кнопка отправки номера
def number_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить номер📞', request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(but1)

    return kb


# Кнопка отправки локации
def location_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить локацию📍', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)

    return kb


# Кнопки выбора товара
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=i[0]) for i in products]
    # Добавить кнопки в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb

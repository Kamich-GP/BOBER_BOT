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


# Кнопки выбора количества
def choice_pr_buttons(pr_amount, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    to_cart = types.InlineKeyboardButton(text='В корзину🛒', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад⬅', callback_data='back')
    # Алгоритм изменения товара
    if plus_or_minus == 'increment':
        if amount <= pr_amount:
            count = types.InlineKeyboardButton(text=str(amount + 1), callback_data=str(amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount - 1), callback_data=str(amount))
    # Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)

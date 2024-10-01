# Алгоритмы бота
import telebot
import database as db
import buttons as bt


# Создаем объект бота
bot = telebot.TeleBot('7652238824:AAHbZCfTFE4Le7mfkbXdcthKJzUuAnPBSXA')
# ID администратора
admin_id = 6775701667

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    products = db.get_pr_buttons()
    if db.check_user(user_id):
        bot.send_message(user_id, f'Здравствуйте, @{message.from_user.username}!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:', reply_markup=bt.main_menu(products))
    else:
        bot.send_message(user_id, 'Привет! Давайте начнем регистрацию!\n'
                                  'Введите ваше Имя!', reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер через кнопку!',
                     reply_markup=bt.number_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_number, user_name)


# Этап получения номера
def get_number(message, user_name):
    user_id = message.from_user.id
    # Проверяем, отправлен ли номер по кнопке
    if message.contact:
        user_number = message.contact.phone_number
        db.register(user_id, user_name, user_number)
        bot.send_message(user_id, 'Вы успешно зарегистрированы!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        products = db.get_pr_buttons()
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(products))
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку ниже!')
        # Возвращение на этап получения номера
        bot.register_next_step_handler(message, get_number, user_name)


## Админ панель ##
# Обработчик команды /admin
@bot.message_handler(commands=['admin'])
def start_admin(message):
    if message.from_user.id == admin_id:
        bot.send_message(admin_id, 'Добро пожаловать в админ-панель!',
                         reply_markup=bt.admin_menu())
        # Переход на этап выбора
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'Вы не администратор!')


# Этап выбора
def admin_choice(message):
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Начнем добавления продукта\n'
                                   'Введите название, описание, цену, количество и фото товара через запятую\n'
                                   'Пример:\n'
                                   'Картошка, Классный клубень, 4999.99, 1000, https://kartoshka.jpg\n\n'
                                   'Для отправки фотографии, воспользуйтесь https://postimages.org/, '
                                   'загрузите фото товара и впишите прямую на нее ссылку',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения товара
        bot.register_next_step_handler(message, get_product)
    elif message.text == 'Удалить продукт':
        if db.check_pr():
            products = db.get_all_pr()
            bot.send_message(admin_id, 'Выберите товар для удаления',
                             reply_markup=bt.admin_pr(products))
            # Переход на этап получения товара для удаления
            bot.register_next_step_handler(message, get_product_to_del)
        else:
            bot.send_message(admin_id, 'Товаров в базе нет!')
            # Возврат на этап выбора
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Изменить продукт':
        if db.check_pr():
            products = db.get_all_pr()
            bot.send_message(admin_id, 'Выберите товар для изменения',
                             reply_markup=bt.admin_pr(products))
            # Переход на этап получения товара для изменения
            bot.register_next_step_handler(message, get_product_to_chng)
        else:
            bot.send_message(admin_id, 'Товаров в базе нет!')
            # Возврат на этап выбора
            bot.register_next_step_handler(message, admin_choice)
    elif message.text == 'Перейти в главное меню':
        products = db.get_pr_buttons()
        bot.send_message(admin_id, 'Перенаправляю вас обратно в меню',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(admin_id, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(products))


# Этап получения товара на добавление
def get_product(message):
    pr_attrs = message.text.split(', ')
    db.pr_to_db(pr_attrs[0], pr_attrs[1], pr_attrs[2], pr_attrs[3], pr_attrs[4])
    bot.send_message(admin_id, f'Продукт {pr_attrs[0]} успешно добавлен! Что-то ещё?',
                     reply_markup=bt.admin_menu())
    # Возвращение на этап выбора
    bot.register_next_step_handler(message, admin_choice)


# Этап получения товара на удаление
def get_product_to_del(message):
    bot.send_message(admin_id, 'Вы уверены?', reply_markup=bt.confirm_buttons())
    # Переход на этап подтверждения
    # bot.register_next_step_handler(message, confirm_delete)


# Этап получения товара на изменение
def get_product_to_chng():
    bot.send_message(admin_id, 'Какой аттрибут вы хотите изменить?',
                     reply_markup=bt.change_buttons())


@bot.callback_query_handler(lambda call: call.data in ['name', 'description', 'price', 'count', 'photo'])
def change_attr(call):
    if call.data == 'name':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое название товара')
        attr = call.data
        # Переход на этап получения подтверждения
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'description':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новое описание товара')
        attr = call.data
        # Переход на этап получения подтверждения
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'price':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новую цену товара')
        attr = call.data
        # Переход на этап получения подтверждения
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'count':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите кол-во прибытия товара')
        attr = call.data
        # Переход на этап получения подтверждения
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'photo':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(admin_id, 'Введите новую ссылку товара')
        attr = call.data
        # Переход на этап получения подтверждения
        bot.register_next_step_handler(call, confirm_change, attr)


# Этап подтверждения
def confirm_change(message, attr):
    bot.send_message(admin_id, 'Вы уверены?',
                     reply_markup=bt.confirm_buttons())
    # Переход на этап изменения
    #bot.register_next_step_handler(message, confirm_change_attr, attr)


# Этап подтверждения удаления
# def confirm_delete(message):
#     if message.text == 'Да':
#         db.del_product()
#

bot.polling()

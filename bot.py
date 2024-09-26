# Алгоритмы бота
import telebot
import database as db
import buttons as bt


# Создаем объект бота
bot = telebot.TeleBot('7652238824:AAHbZCfTFE4Le7mfkbXdcthKJzUuAnPBSXA')


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.check_user(user_id):
        bot.send_message(user_id, 'Привет!')
    else:
        bot.send_message(user_id, 'Привет! Давайте начнем регистрацию!\n'
                                  'Введите ваше Имя!')
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
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку ниже!')
        # Возвращение на этап получения номера
        bot.register_next_step_handler(message, get_number, user_name)


bot.polling()


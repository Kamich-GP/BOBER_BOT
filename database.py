# Работа с БД
import sqlite3


# Подключаемся к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()

# Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, number TEXT);')
# Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_price REAL, '
            'pr_count INTEGER, pr_photo TEXT);')
# Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_product TEXT, '
            'product_amount INTEGER);')


## Методы для пользователя ##
# Регистрация пользователя в БД
def register(tg_id, name, number):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);',
                (tg_id, name, number))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие в БД
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False


## Методы для продуктов ##
# Вывод продуктов для кнопок
def get_pr_buttons():
    all_products = sql.execute('SELECT * FROM products;').fetchall()
    result = [i for i in all_products if i[4] > 0]
    return result


# Вывод всех продуктов
def get_all_pr():
    return sql.execute('SELECT * FROM products;').fetchall()


# Вывод информации о конкретном продукте
def get_exact_pr(pr_id):
    return sql.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()


# Вывод цены конкретного продукта
def get_exact_price(pr_id):
    return sql.execute('SELECT pr_price FROM products WHERE pr_id=?;', (pr_id,)).fetchone()


## Методы для администрирования продуктов ##
# Добавление продукта в БД
def pr_to_db(pr_name, pr_des, pr_price, pr_count, pr_photo):
    if (pr_name,) in sql.execute('SELECT pr_name FROM products;').fetchall():
        return False
    else:
        sql.execute('INSERT INTO products (pr_name, pr_des, pr_price, pr_count, pr_photo) '
                    'VALUES (?, ?, ?, ?, ?);', (pr_name, pr_des, pr_price, pr_count, pr_photo))
        # Фиксируем изменения
        connection.commit()


# Изменения аттрибута продукта
def change_pr_attr(keyword, new_value, attr=''):
    if attr == 'name':
        sql.execute('UPDATE products SET pr_name=? WHERE pr_name=?;',
                    (new_value, keyword))
    elif attr == 'description':
        sql.execute('UPDATE products SET pr_des=? WHERE pr_name=?;',
                    (new_value, keyword))
    elif attr == 'price':
        sql.execute('UPDATE products SET pr_price=? WHERE pr_name=?;',
                    (new_value, keyword))
    elif attr == 'count':
        sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;',
                    (new_value, keyword))
    elif attr == 'photo':
        sql.execute('UPDATE products SET pr_photo=? WHERE pr_name=?;',
                    (new_value, keyword))

    # Фиксируем изменения
    connection.commit()


# Удаление товара из БД
def del_product(pr_id):
    sql.execute('DELETE FROM products WHERE pr_name=?;', (pr_id,))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие продуктов в БД
def check_pr():
    if sql.execute('SELECT * FROM products;').fetchall():
        return True
    else:
        return False

import sqlite3

connection = sqlite3.connect('translation.db', check_same_thread=False)
cursor = connection.cursor()


cursor.executescript('''
    DROP TABLE IF EXISTS users;
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        chat_id BIGINT NOT NULL
    );

    DROP TABLE IF EXISTS translations;
    CREATE TABLE IF NOT EXISTS translations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lang_from TEXT,
        lang_to TEXT,
        original_text TEXT,
        translated_text TEXT,
        user_id INTEGER REFERENCES users(id)
    );
''')

def is_user_exists(chat_id):
    sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql, (chat_id,))
    user_id = cursor.fetchone()  # (1,)
    if not user_id:
        return False
    return True


def add_user(first_name, chat_id):
    sql = 'INSERT INTO users(first_name, chat_id) VALUES (?, ?)'
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()

def get_user_id(chat_id):
    user_sql = 'SELECT id FROM users WHERE chat_id = ?;'
    cursor.execute(user_sql, (chat_id,))
    user_id = cursor.fetchone()[0]
    return user_id

def add_translation(lang_from, lang_to, original_text, translated_text, chat_id):
    user_id = get_user_id(chat_id)
    sql = 'INSERT INTO translations(lang_from, lang_to, original_text, translated_text, user_id) VALUES (?, ?, ?, ?, ?)'
    cursor.execute(sql, (lang_from, lang_to, original_text, translated_text, user_id))
    connection.commit()


connection.commit()

# соединиться с БД
# создать объект для отправки запросов в БД
# создать 2 таблицы
# users
# id
# first_name
# chat_id BIGINT

# translations
# id
# lang_from
# lang_to
# original_text
# translated_text
# user_id

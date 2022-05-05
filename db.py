import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        
#TELEGRAM ----------------------------------------------------------------------------------

    def user_exists_tg(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE tgid = ?', (user_id,)).fetchall()
            return bool(len(result))

    def take_users(self):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users').fetchall()
            return result

    def user_info_tg(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE tgid = ?', (user_id,)).fetchone()  
                 
    def add_user_tg(self, user_id, username, name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (tgid, tgname, name, msgID, needTrust) VALUES (?, ?, ?, ?, ?)", (user_id, username, name, 0, 0))

    def take_readers_list(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM publishers WHERE tgid = ?', (user_id,)).fetchall()

    def add_publisher_and_user(self, referrer_candidate, user_id, reader_name):
        with self.connection:
            self.cursor.execute("INSERT INTO publishers (tgid, readerid, reader_name, trust) VALUES (?, ?, ?, ?)", (referrer_candidate, user_id, reader_name, 0))

    def select_trust_for_reader(self, referrer_candidate, user_id, trust):
        with self.connection:
            self.cursor.execute('UPDATE publishers SET trust = ? WHERE tgid = ? AND readerid = ?', (trust, referrer_candidate, user_id))

    def new_publicationID(self, user_id, msgid):
        with self.connection:
            self.cursor.execute('UPDATE users SET msgID = ? WHERE tgid = ?', (msgid, user_id))

    def setTrust(self, user_id, needTrust):
        with self.connection:
            self.cursor.execute('UPDATE users SET needTrust = ? WHERE tgid = ?', (needTrust, user_id))

    def reader_exists(self, user_id, publisher):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM publishers WHERE tgid = ? AND readerid = ?', (publisher, user_id)).fetchall()
            return bool(len(result))

    def readers_for_publication(self, user_id, trust):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM publishers WHERE tgid = ? AND trust <= ?', (user_id, trust)).fetchall()

    def take_publisher_list(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM publishers WHERE readerid = ?', (user_id,)).fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
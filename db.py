import sqlite3
import logging
class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user` = ?", (user_id,))
        return result.fetchone()

    def get_record(self, user_id, data):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` = ?", (user_id, data))
        logging.info(result)
        return result.fetchall()

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, date, time, activity):
        self.cursor.execute("INSERT INTO records (`users_id`, `date`, `time`, `activity`) VALUES (?, ?, ?, ?)", (user_id, date, time, activity) )
        self.conn.commit()
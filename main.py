import sqlite3
from datetime import datetime


# Класс User для хранения информации об обычных сотрудниках
class User:
    def __init__(self, user_id, name):
        """
        Конструктор класса User.
        """
        self._user_id = user_id
        self._name = name
        self._access_level = 'user'

    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    def get_access_level(self):
        return self._access_level


# Класс Admin, наследуется от User
class Admin(User):
    def __init__(self, user_id, name, db_name='company.db'):
        """
        Конструктор класса Admin.
        """
        super().__init__(user_id, name)
        self._access_level = 'admin'
        self._db_name = db_name
        self._create_tables()

    def _connect(self):
        """Внутренний метод подключения к БД."""
        return sqlite3.connect(self._db_name)

    def _create_tables(self):
        """Создаёт таблицы в БД, если их ещё нет."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                access_level TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AdminLogs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_name TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def log_action(self, action):
        """Записывает действие администратора в таблицу логов."""
        conn = self._connect()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO AdminLogs (admin_name, action, timestamp)
            VALUES (?, ?, ?)
        ''', (self.get_name(), action, timestamp))
        conn.commit()
        conn.close()

    def add_user(self, new_user):
        """Добавляет пользователя в базу данных."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Users (id, name, access_level)
            VALUES (?, ?, ?)
        ''', (new_user.get_user_id(), new_user.get_name(), new_user.get_access_level()))

        conn.commit()
        conn.close()

        self.log_action(f"Добавил пользователя {new_user.get_name()} (ID: {new_user.get_user_id()})")

    def remove_user(self, user_id_to_remove):
        """Удаляет пользователя по ID."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM Users WHERE id = ?', (user_id_to_remove,))
        result = cursor.fetchone()

        if result:
            user_name = result[0]
            cursor.execute('DELETE FROM Users WHERE id = ?', (user_id_to_remove,))
            conn.commit()
            self.log_action(f"Удалил пользователя {user_name} (ID: {user_id_to_remove})")
        else:
            print(f"Пользователь с ID {user_id_to_remove} не найден.")

        conn.close()

    def list_users(self):
        """Выводит всех пользователей из базы."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('SELECT id, name, access_level FROM Users')
        users = cursor.fetchall()

        if users:
            print("\nТекущие пользователи:")
            for user_record in users:
                print(f"ID: {user_record[0]}, Имя: {user_record[1]}, Доступ: {user_record[2]}")
        else:
            print("Пользователи отсутствуют.")

        conn.close()

    def list_logs(self):
        """Выводит все записи из логов администратора."""
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('SELECT log_id, admin_name, action, timestamp FROM AdminLogs ORDER BY log_id DESC')
        logs = cursor.fetchall()

        if logs:
            print("\nЖурнал действий администратора:")
            for log in logs:
                print(f"[{log[3]}] {log[1]} — {log[2]}")
        else:
            print("Логи отсутствуют.")

        conn.close()


# === Пример использования системы ===

if __name__ == "__main__":
    # Создаём администратора
    admin1 = Admin(1, "Алексей")

    # Создаём сотрудников
    employee1 = User(2, "Мария")
    employee2 = User(3, "Иван")

    # Добавляем сотрудников
    admin1.add_user(employee1)
    admin1.add_user(employee2)

    # Список пользователей
    admin1.list_users()

    # Удаляем одного сотрудника
    admin1.remove_user(3)

    # Список пользователей после удаления
    admin1.list_users()

    # Показать логи действий администратора
    admin1.list_logs()

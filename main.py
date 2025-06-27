# Импортируем модуль tkinter для создания GUI
import tkinter as tk
# Импортируем стандартный диалог для всплывающих сообщений
from tkinter import messagebox
# Импортируем модуль logging для ведения журнала действий
import logging

# Настраиваем базовое логирование
logging.basicConfig(
    filename='log.txt',                      # Указываем имя файла журнала
    level=logging.INFO,                      # Уровень логируемых сообщений
    format='%(asctime)s - %(message)s'       # Формат записей в логе: время и сообщение
)

# Создаем класс User для описания обычного пользователя
class User:
    # Конструктор класса, принимает ID и имя пользователя
    def __init__(self, user_id, name):
        self.__user_id = user_id             # Приватный атрибут для хранения ID
        self.__name = name                   # Приватный атрибут для хранения имени
        self.__access_level = 'user'         # По умолчанию — уровень доступа 'user'

    # Метод для получения ID пользователя
    def get_id(self):
        return self.__user_id

    # Метод для получения имени пользователя
    def get_name(self):
        return self.__name

    # Метод для получения уровня доступа пользователя
    def get_access_level(self):
        return self.__access_level

# Создаем класс Admin, который наследуется от User и расширяет его функциональность
class Admin(User):
    # Конструктор класса Admin, принимает ID и имя администратора
    def __init__(self, user_id, name):
        super().__init__(user_id, name)      # Вызываем конструктор родительского класса User
        self.__access_level = 'admin'        # Устанавливаем уровень доступа 'admin'
        self.__user_list = []                # Создаем локальный список пользователей

    # Метод для добавления нового пользователя в список
    def add_user(self, new_user):
        self.__user_list.append(new_user)    # Добавляем экземпляр User в список
        # Записываем информацию о добавлении в лог
        logging.info(f"Добавлен пользователь: {new_user.get_name()} с ID {new_user.get_id()}")

    # Метод для удаления пользователя по его ID
    def remove_user(self, user_id_to_remove):
        # Проходим по списку пользователей
        for user_item in self.__user_list:
            # Если найден пользователь с нужным ID
            if user_item.get_id() == user_id_to_remove:
                self.__user_list.remove(user_item)  # Удаляем его из списка
                # Записываем информацию об удалении в лог
                logging.info(f"Удален пользователь: {user_item.get_name()} с ID {user_item.get_id()}")
                return True                    # Возвращаем True, если удаление успешно
        return False                           # Если пользователь не найден, возвращаем False

    # Метод для получения полного списка пользователей
    def get_user_list(self):
        return self.__user_list

# Функция для создания графического интерфейса приложения
def create_gui():
    # Создаем главное окно приложения (переименовано с root → main_window)
    main_window = tk.Tk()
    main_window.title("User Management System")  # Устанавливаем заголовок окна

    # Создаем экземпляр администратора для работы с пользователями
    admin_instance = Admin(1, "SuperAdmin")      # Экземпляр класса Admin

    # Вложенная функция для добавления пользователя через GUI
    def gui_add_user():
        user_id = entry_id.get()                 # Получаем ID из поля ввода
        user_name = entry_name.get()             # Получаем имя из поля ввода
        if user_id and user_name:                # Проверяем, что оба поля заполнены
            new_user = User(user_id, user_name)  # Создаем нового пользователя
            admin_instance.add_user(new_user)    # Добавляем его в список через администратора
            messagebox.showinfo("Успех", f"Пользователь {user_name} добавлен.")  # Выводим сообщение об успехе
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля.")  # Сообщение об ошибке если поля пустые

    # Вложенная функция для удаления пользователя через GUI
    def gui_remove_user():
        user_id = entry_id.get()                 # Получаем ID из поля ввода
        if user_id:                              # Проверяем, что поле заполнено
            result = admin_instance.remove_user(user_id)  # Пытаемся удалить пользователя
            if result:                           # Если удаление прошло успешно
                messagebox.showinfo("Успех", f"Пользователь с ID {user_id} удален.")
            else:
                messagebox.showwarning("Ошибка", "Пользователь не найден.")  # Если ID не найден
        else:
            messagebox.showwarning("Ошибка", "Укажите ID пользователя.")  # Если поле пустое

    # Вложенная функция для отображения всех текущих пользователей
    def gui_show_users():
        users = admin_instance.get_user_list()   # Получаем список пользователей от администратора
        if users:                                # Если список не пуст
            # Формируем строку со списком пользователей
            user_info = "\n".join([f"{u.get_id()}: {u.get_name()}" for u in users])
            messagebox.showinfo("Пользователи", user_info)  # Показываем окно со списком
        else:
            messagebox.showinfo("Пользователи", "Список пользователей пуст.")  # Если список пуст

    # Создаем метку и поле ввода для ID пользователя
    tk.Label(main_window, text="ID пользователя").pack()
    entry_id = tk.Entry(main_window)
    entry_id.pack()

    # Создаем метку и поле ввода для имени пользователя
    tk.Label(main_window, text="Имя пользователя").pack()
    entry_name = tk.Entry(main_window)
    entry_name.pack()

    # Создаем кнопку для добавления пользователя
    tk.Button(main_window, text="Добавить пользователя", command=gui_add_user).pack(pady=5)

    # Создаем кнопку для удаления пользователя
    tk.Button(main_window, text="Удалить пользователя", command=gui_remove_user).pack(pady=5)

    # Создаем кнопку для отображения списка пользователей
    tk.Button(main_window, text="Показать пользователей", command=gui_show_users).pack(pady=5)

    # Запускаем главный цикл обработки событий
    main_window.mainloop()

# Проверяем, что скрипт запущен как основная программа
if __name__ == "__main__":
    create_gui()  # Запускаем функцию создания GUI

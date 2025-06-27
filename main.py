import tkinter as tk  # 📦 Импортируем модуль Tkinter для создания GUI
from tkinter import messagebox, simpledialog  # 📦 Импортируем диалоговые окна и сообщения из Tkinter
import logging  # 📦 Импортируем модуль логирования для записи действий в файл

# 📑 Настраиваем систему логирования, чтобы писать данные в файл 'user_management.log'
logging.basicConfig(filename='user_management.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class User:
    """
    📌 Базовый класс User — описывает пользователя компании.
    Инкапсулирует ID, имя и уровень доступа.
    """
    def __init__(self, user_id, name):
        self._user_id = user_id  # защищённый атрибут ID пользователя
        self._name = name  # защищённый атрибут имени пользователя
        self._access_level = 'user'  # защищённый атрибут уровня доступа (по умолчанию 'user')

    def get_user_id(self):
        """📌 Геттер для получения ID пользователя."""
        return self._user_id

    def get_name(self):
        """📌 Геттер для получения имени пользователя."""
        return self._name

    def get_access_level(self):
        """📌 Геттер для получения уровня доступа пользователя."""
        return self._access_level


class Admin(User):
    """
    📌 Класс Admin — наследует от User.
    Добавляет возможность добавлять и удалять пользователей из системы.
    """
    def __init__(self, user_id, name):
        super().__init__(user_id, name)  # 📌 Наследуем конструктор от родителя
        self._access_level = 'admin'  # 📌 Переопределяем уровень доступа на 'admin'

    def add_user(self, target_list, new_user):
        """
        📌 Метод для добавления нового пользователя в список.
        :param target_list: список пользователей
        :param new_user: экземпляр класса User
        """
        target_list.append(new_user)  # добавляем пользователя в список
        # 📌 Записываем действие в лог
        logging.info(f"Администратор {self._name} добавил пользователя {new_user.get_name()} (ID: {new_user.get_user_id()})")

    def remove_user(self, target_list, user_id):
        """
        📌 Метод для удаления пользователя по ID.
        :param target_list: список пользователей
        :param user_id: идентификатор пользователя для удаления
        :return: True если удалено успешно, иначе False
        """
        for u in target_list:  # перебираем список пользователей
            if u.get_user_id() == user_id:
                target_list.remove(u)  # удаляем пользователя из списка
                # 📌 Логируем действие
                logging.info(f"Администратор {self._name} удалил пользователя {u.get_name()} (ID: {user_id})")
                return True  # успешное удаление
        return False  # если пользователь не найден


class UserManagerGUI:
    """
    📌 Класс GUI для управления пользователями.
    Использует Tkinter.
    """
    def __init__(self, root, admin):
        self.root = root  # 📌 основное окно приложения
        self.admin = admin  # 📌 активный администратор
        self.users = []  # 📌 список пользователей

        # 📌 Настройка заголовка окна
        self.root.title("Система управления пользователями")

        # 📌 Список пользователей в виде Listbox
        self.user_listbox = tk.Listbox(root, width=50)
        self.user_listbox.pack(pady=10)

        # 📌 Блок кнопок
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        # 📌 Кнопка для добавления пользователя
        tk.Button(btn_frame, text="Добавить пользователя", command=self.add_user).pack(side=tk.LEFT, padx=5)

        # 📌 Кнопка для удаления пользователя
        tk.Button(btn_frame, text="Удалить пользователя", command=self.remove_user).pack(side=tk.LEFT, padx=5)

        # 📌 Кнопка для обновления списка
        tk.Button(btn_frame, text="Обновить список", command=self.refresh_list).pack(side=tk.LEFT, padx=5)

        # 📌 Кнопка для открытия лога действий
        tk.Button(root, text="Открыть лог действий", command=self.show_logs).pack(pady=5)

    def add_user(self):
        """📌 Метод добавления пользователя через диалоговые окна."""
        try:
            user_id = simpledialog.askinteger("Добавление пользователя", "Введите ID пользователя:")
            if user_id is None:  # отмена ввода
                return
            name = simpledialog.askstring("Добавление пользователя", "Введите имя пользователя:")
            if not name:
                return
            new_user = User(user_id, name)  # создаём экземпляр User
            self.admin.add_user(self.users, new_user)  # добавляем его через метод администратора
            self.refresh_list()  # обновляем список в окне
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))  # обработка исключений

    def remove_user(self):
        """📌 Метод удаления пользователя по ID через диалоговое окно."""
        try:
            user_id = simpledialog.askinteger("Удаление пользователя", "Введите ID пользователя для удаления:")
            if user_id is None:
                return
            success = self.admin.remove_user(self.users, user_id)  # пробуем удалить пользователя
            if success:
                messagebox.showinfo("Успех", f"Пользователь с ID {user_id} удалён.")
            else:
                messagebox.showwarning("Не найден", f"Пользователь с ID {user_id} не найден.")
            self.refresh_list()  # обновляем отображение списка
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def refresh_list(self):
        """📌 Обновляет отображение списка пользователей в Listbox."""
        self.user_listbox.delete(0, tk.END)  # очищаем текущий список
        for u in self.users:  # проходимся по пользователям
            display_text = f"ID: {u.get_user_id()} | Имя: {u.get_name()} | Доступ: {u.get_access_level()}"
            self.user_listbox.insert(tk.END, display_text)  # добавляем строку в Listbox

    def show_logs(self):
        """📌 Отображает содержимое лог-файла в отдельном окне."""
        try:
            with open('user_management.log', 'r', encoding='utf-8') as f:
                logs = f.read()  # читаем файл логов
            log_window = tk.Toplevel(self.root)  # создаём новое окно
            log_window.title("Лог действий")
            text = tk.Text(log_window, wrap=tk.WORD)  # текстовое поле для логов
            text.insert(tk.END, logs)  # вставляем текст логов
            text.pack(expand=True, fill=tk.BOTH)  # размещаем на весь размер окна
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Лог-файл не найден.")


# 📦 Запуск программы, если файл выполняется как основной
if __name__ == "__main__":
    root = tk.Tk()  # создаём главное окно приложения
    admin = Admin(1, "Администратор")  # создаём администратора с ID 1
    gui = UserManagerGUI(root, admin)  # создаём GUI и передаём ему администратора
    root.mainloop()  # запускаем главный цикл приложения

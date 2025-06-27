# Класс User для хранения информации об обычных сотрудниках
class User:
    def __init__(self, user_id, name):
        """
        Конструктор класса User.
        Инициализирует уникальный идентификатор, имя и уровень доступа.
        Атрибуты инкапсулируются (protected, с одним подчёркиванием).
        """
        self._user_id = user_id         # Уникальный ID пользователя (protected)
        self._name = name               # Имя пользователя (protected)
        self._access_level = 'user'     # Уровень доступа по умолчанию — 'user'

    # Метод для получения ID пользователя
    def get_user_id(self):
        """Возвращает ID пользователя"""
        return self._user_id

    # Метод для получения имени пользователя
    def get_name(self):
        """Возвращает имя пользователя"""
        return self._name

    # Метод для установки нового имени
    def set_name(self, new_name):
        """Устанавливает новое имя пользователя"""
        self._name = new_name

    # Метод для получения уровня доступа пользователя
    def get_access_level(self):
        """Возвращает уровень доступа пользователя"""
        return self._access_level

# Класс Admin — наследник класса User, представляет администратора компании
class Admin(User):
    def __init__(self, user_id, name):
        """
        Конструктор класса Admin.
        Вызывает конструктор родительского класса User.
        Устанавливает уровень доступа администратора.
        """
        super().__init__(user_id, name)   # Инициализируем базовые атрибуты от User
        self._access_level = 'admin'      # Меняем уровень доступа на 'admin'

    def add_user(self, user_list, new_user):
        """
        Метод для добавления нового пользователя в систему.
        Принимает список пользователей и экземпляр User.
        """
        user_list.append(new_user)  # Добавляем нового пользователя в список
        print(f"Пользователь '{new_user.get_name()}' успешно добавлен.")

    def remove_user(self, user_list, user_id):
        """
        Метод для удаления пользователя по ID.
        Принимает список пользователей и ID удаляемого пользователя.
        """
        for user in user_list:
            if user.get_user_id() == user_id:
                user_list.remove(user)
                print(f"Пользователь '{user.get_name()}' успешно удалён.")
                return
        # Если пользователь с таким ID не найден — выводим сообщение
        print(f"Пользователь с ID {user_id} не найден.")

# === Пример использования системы ===

# Создаём пустой список для хранения всех пользователей компании
user_list = []

# Создаём администратора
admin1 = Admin(1, "Алексей")

# Создаём нескольких обычных сотрудников
user1 = User(2, "Мария")
user2 = User(3, "Иван")
user3 = User(4, "Светлана")

# Администратор добавляет пользователей в систему
admin1.add_user(user_list, user1)
admin1.add_user(user_list, user2)
admin1.add_user(user_list, user3)

# Проверяем содержимое списка пользователей
print("\nСписок пользователей после добавления:")
for user in user_list:
    print(f"ID: {user.get_user_id()}, Имя: {user.get_name()}, Доступ: {user.get_access_level()}")

# Удаляем пользователя с ID 3
admin1.remove_user(user_list, 3)

# Проверяем содержимое списка после удаления
print("\nСписок пользователей после удаления:")
for user in user_list:
    print(f"ID: {user.get_user_id()}, Имя: {user.get_name()}, Доступ: {user.get_access_level()}")

# Пробуем удалить несуществующего пользователя
admin1.remove_user(user_list, 5)

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

    def get_user_id(self):
        """Возвращает ID пользователя"""
        return self._user_id

    def get_name(self):
        """Возвращает имя пользователя"""
        return self._name

    def set_name(self, new_name):
        """Устанавливает новое имя пользователя"""
        self._name = new_name

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
        super().__init__(user_id, name)
        self._access_level = 'admin'

    @staticmethod
    def add_user(user_collection, new_user):
        """
        Статический метод для добавления нового пользователя в систему.
        Принимает список пользователей и экземпляр User.
        """
        user_collection.append(new_user)
        print(f"Пользователь '{new_user.get_name()}' успешно добавлен.")

    @staticmethod
    def remove_user(user_collection, user_id_to_remove):
        """
        Статический метод для удаления пользователя по ID.
        Принимает список пользователей и ID удаляемого пользователя.
        """
        for existing_user in user_collection:
            if existing_user.get_user_id() == user_id_to_remove:
                user_collection.remove(existing_user)
                print(f"Пользователь '{existing_user.get_name()}' успешно удалён.")
                return
        print(f"Пользователь с ID {user_id_to_remove} не найден.")


# === Пример использования системы ===

# Создаём пустой список для хранения всех пользователей компании
all_users = []

# Создаём администратора
admin1 = Admin(1, "Алексей")

# Создаём нескольких обычных сотрудников
employee1 = User(2, "Мария")
employee2 = User(3, "Иван")
employee3 = User(4, "Светлана")

# Администратор добавляет пользователей в систему
Admin.add_user(all_users, employee1)
Admin.add_user(all_users, employee2)
Admin.add_user(all_users, employee3)

# Проверяем содержимое списка пользователей
print("\nСписок пользователей после добавления:")
for person in all_users:
    print(f"ID: {person.get_user_id()}, Имя: {person.get_name()}, Доступ: {person.get_access_level()}")

# Удаляем пользователя с ID 3
Admin.remove_user(all_users, 3)

# Проверяем содержимое списка после удаления
print("\nСписок пользователей после удаления:")
for person in all_users:
    print(f"ID: {person.get_user_id()}, Имя: {person.get_name()}, Доступ: {person.get_access_level()}")

# Пробуем удалить несуществующего пользователя
Admin.remove_user(all_users, 5)

from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Або використайте MongoDB Atlas URL
db = client["cat_database"]  # Створюємо або використовуємо базу даних
collection = db["cats"]  # Створюємо або використовуємо колекцію

# Функція для додавання нового кота (Create)
def create_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(cat)
        print(f"Кіт доданий з _id: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка додавання кота: {e}")

# Функція для виведення всіх котів (Read)
def read_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка читання котів: {e}")

# Функція для виведення кота за іменем (Read)
def find_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з іменем {name} не знайдено.")
    except Exception as e:
        print(f"Помилка пошуку кота: {e}")

# Функція для оновлення віку кота за іменем (Update)
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено.")
        else:
            print(f"Кота з іменем {name} не знайдено.")
    except Exception as e:
        print(f"Помилка оновлення віку кота: {e}")

# Функція для додавання нової характеристики до кота (Update)
def add_feature_to_cat(name, new_feature):
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Характеристика '{new_feature}' додана до кота {name}.")
        else:
            print(f"Кота з іменем {name} не знайдено.")
    except Exception as e:
        print(f"Помилка додавання характеристики коту: {e}")

# Функція для видалення кота за ім'ям (Delete)
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кота з іменем {name} видалено.")
        else:
            print(f"Кота з іменем {name} не знайдено.")
    except Exception as e:
        print(f"Помилка видалення кота: {e}")

# Функція для видалення всіх котів (Delete)
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except Exception as e:
        print(f"Помилка видалення всіх котів: {e}")

# Приклад виклику функцій
if __name__ == "__main__":
    # Додавання кота
    create_cat("barsik", 3, ["рудий", "ходить в капці"])
    create_cat("lama", 2, ["сірий", "ходить в лоток", "не дає себе гладити"])
    create_cat("liza", 4, ["білий", "ходить в лоток", "дає себе гладити"])
    create_cat("boris", 12, ["сірий", "ходить в лоток", "не дає себе гладити"])
    create_cat("murzik", 1, ["чорний", "ходить в лоток", "дає себе гладити"])

    # Виведення всіх котів
    read_all_cats()

    # Пошук кота за ім'ям
    find_cat_by_name("barsik")

    # Оновлення віку кота
    update_cat_age("barsik", 4)

    # Додавання нової характеристики
    add_feature_to_cat("barsik", "любить рибу")

    # Видалення кота за ім'ям
    delete_cat_by_name("barsik")

    # Видалення всіх котів
    # delete_all_cats()
    read_all_cats()
import psycopg2
from faker import Faker

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123QWEasd",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Ініціалізація Faker
fake = Faker()

# Вставляємо статуси
statuses = [('new',), ('in progress',), ('completed',)]
cursor.executemany("INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", statuses)
conn.commit()

# Вставляємо користувачів та завдання
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    
    # Вставляємо користувача
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id", (fullname, email))
    user_id = cursor.fetchone()[0]
    
    # Вставляємо кілька завдань для користувача
    for _ in range(5):
        title = fake.sentence(nb_words=4)
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)
        
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )

# Фіксуємо зміни
conn.commit()

# Закриваємо з'єднання
cursor.close()
conn.close()

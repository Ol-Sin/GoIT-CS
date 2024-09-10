import psycopg2

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123QWEasd",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# SQL для створення таблиць
create_tables_query = '''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
'''

# Виконання SQL запиту для створення таблиць
cursor.execute(create_tables_query)
conn.commit()

print("Таблиці успішно створені!")

# Закриваємо з'єднання
cursor.close()
conn.close()

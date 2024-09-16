import threading
import os
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_files(files, keywords, results, lock):
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        with lock:
                            if keyword not in results:
                                results[keyword] = []
                            results[keyword].append(file)
        except Exception as e:
            print(f"Помилка під час обробки файлу {file}: {e}")

# Багатопотокова реалізація
def multithreaded_search(directory, keywords):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    num_threads = 4
    chunk_size = len(files) // num_threads

    threads = []
    results = {}
    lock = threading.Lock()

    start_time = time.time()

    # Створюємо та запускаємо потоки
    for i in range(num_threads):
        start = i * chunk_size
        end = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread = threading.Thread(target=search_keywords_in_files, args=(files[start:end], keywords, results, lock))
        threads.append(thread)
        thread.start()

    # Очікуємо завершення роботи всіх потоків
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Час виконання (threading): {end_time - start_time} секунд")
    return results

# Приклад використання
if __name__ == "__main__":
    directory = './text_files/'  # Директорія з файлами
    keywords = ['Python', 'and', 'data']  # Ключові слова для пошуку
    results = multithreaded_search(directory, keywords)
    print(results)

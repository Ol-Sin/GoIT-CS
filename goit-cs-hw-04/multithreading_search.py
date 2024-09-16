import multiprocessing
import os
import time

# Функція для пошуку ключових слів у файлі
def search_keywords_in_files(files, keywords, queue):
    results = {}
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for keyword in keywords:
                    if keyword in content:
                        if keyword not in results:
                            results[keyword] = []
                        results[keyword].append(file)
        except Exception as e:
            print(f"Помилка під час обробки файлу {file}: {e}")
    queue.put(results)

# Багатопроцесорна реалізація
def multiprocess_search(directory, keywords):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    num_processes = 4
    chunk_size = len(files) // num_processes

    processes = []
    queue = multiprocessing.Queue()

    start_time = time.time()

    # Створюємо та запускаємо процеси
    for i in range(num_processes):
        start = i * chunk_size
        end = None if i == num_processes - 1 else (i + 1) * chunk_size
        process = multiprocessing.Process(target=search_keywords_in_files, args=(files[start:end], keywords, queue))
        processes.append(process)
        process.start()

    # Збираємо результати
    results = {}
    for process in processes:
        process.join()
        partial_results = queue.get()
        for keyword, files in partial_results.items():
            if keyword not in results:
                results[keyword] = []
            results[keyword].extend(files)

    end_time = time.time()
    print(f"Час виконання (multiprocessing): {end_time - start_time} секунд")
    return results

# Приклад використання
if __name__ == "__main__":
    directory = './text_files/'  # Директорія з файлами
    keywords = ['Python', 'and', 'data']  # Ключові слова для пошуку
    results = multiprocess_search(directory, keywords)
    print(results)

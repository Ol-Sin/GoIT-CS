import requests
import re
import threading
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Функція для завантаження тексту з URL
def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Mapper: Розбиває текст на слова і рахує частоту
def map_words(text_chunk):
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    return Counter(words)

# Reducer: Об'єднує два лічильники частот слів
def reduce_counts(count1, count2):
    return count1 + count2

# Основна функція для MapReduce
def map_reduce(text, num_threads=4):
    chunk_size = len(text) // num_threads
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        word_counts = list(executor.map(map_words, chunks))
    
    total_counts = Counter()
    for count in word_counts:
        total_counts = reduce_counts(total_counts, count)
    
    return total_counts

# Візуалізація топ слів
def visualize_top_words(word_counts, top_n=10):
    common_words = word_counts.most_common(top_n)
    words, counts = zip(*common_words)
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title(f"Топ {top_n} слів за частотою використання")
    plt.xlabel("Слова")
    plt.ylabel("Частота")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Головний блок коду
if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Наприклад, текст роману "Гордість і упередження"
    
    # Завантажуємо текст із URL
    try:
        text = download_text(url)
    except Exception as e:
        print(f"Не вдалося завантажити текст: {e}")
        exit()

    # Застосовуємо MapReduce для аналізу частоти слів
    word_counts = map_reduce(text)

    # Візуалізуємо топ-10 слів
    visualize_top_words(word_counts, top_n=10)

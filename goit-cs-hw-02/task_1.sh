#!/bin/bash

# Список вебсайтів для перевірки
websites=("https://google.com" "https://facebook.com" "https://twitter.com")

# Назва файлу логів
logfile="website_status.log"

# Очищаємо файл логів перед новою перевіркою
> $logfile

# Перевірка доступності кожного вебсайту
for website in "${websites[@]}"; do
    # Виконуємо curl запит з прапорцем -L (для обробки перенаправлень)
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -L $website)

    # Перевірка статусу
    if [ $status_code -eq 200 ]; then
        echo "[$website] is UP" | tee -a $logfile
    else
        echo "[$website] is DOWN (HTTP Status: $status_code)" | tee -a $logfile
    fi
done

# Вивід повідомлення про завершення
echo "Результати перевірки записано у файл $logfile"

import asyncio
import os
import shutil
import logging
from pathlib import Path
from argparse import ArgumentParser

# Обробка аргументів командного рядка
def parse_arguments():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source_folder", type=str, help="Вихідна папка")
    parser.add_argument("output_folder", type=str, help="Цільова папка")
    return parser.parse_args()

# Асинхронне копіювання файлів у фоновому потоці
async def copy_file(file_path, output_folder):
    ext = file_path.suffix[1:].lower()  # Отримуємо розширення файлу без крапки
    target_folder = Path(output_folder) / ext

    try:
        # Створюємо папку, якщо вона не існує
        target_folder.mkdir(parents=True, exist_ok=True)

        # Копіюємо файл у відповідну підпапку
        target_path = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, target_path)
        logging.info(f"Копіювання завершено: {file_path} -> {target_path}")
    except Exception as e:
        logging.error(f"Помилка під час копіювання {file_path}: {e}")

# Асинхронне читання папки та її файлів
async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))

    await asyncio.gather(*tasks)

# Налаштування логування
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("file_sorting.log"),
            logging.StreamHandler()
        ]
    )

# Головна функція
async def main():
    args = parse_arguments()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error(f"Вихідна папка не існує або не є папкою: {source_folder}")
        return

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    setup_logging()
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Сталася непередбачена помилка: {e}")

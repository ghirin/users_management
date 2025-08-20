import os
import shutil

# Папки и файлы, которые нужно удалить
CLEAN_PATHS = [
    '__pycache__',
    '*.pyc',
    '*.log',
    '*.sqlite3',
    'db.sqlite3',
    'media/',
    'staticfiles/',
]

# Миграции, кроме __init__.py
def clean_migrations():
    for root, dirs, files in os.walk('.'):
        if 'migrations' in root:
            for file in files:
                if file != '__init__.py' and file.endswith('.py'):
                    os.remove(os.path.join(root, file))
                    print(f'Удалена миграция: {os.path.join(root, file)}')

# Удаление по шаблону
def clean_by_pattern():
    import glob
    for pattern in CLEAN_PATHS:
        for path in glob.glob(f'**/{pattern}', recursive=True):
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    print(f'Удалён файл: {path}')
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f'Удалена папка: {path}')
            except Exception as e:
                print(f'Ошибка при удалении {path}: {e}')

# Запуск
if __name__ == '__main__':
    print('🚀 Начинаем очистку проекта...')
    clean_migrations()
    clean_by_pattern()
    print('✅ Очистка завершена.')

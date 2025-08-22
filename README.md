# Переключение Django-проекта на PostgreSQL

1. Установите PostgreSQL и psycopg2:
	```bash
	sudo apt install postgresql postgresql-contrib
	pip install psycopg2-binary
	```

2. Создайте базу данных и пользователя:
	```bash
	sudo -u postgres psql
	CREATE DATABASE user_management_db;
	CREATE USER user_management_user WITH PASSWORD 'your_password';
	ALTER ROLE user_management_user SET client_encoding TO 'utf8';
	ALTER ROLE user_management_user SET default_transaction_isolation TO 'read committed';
	ALTER ROLE user_management_user SET timezone TO 'UTC';
	GRANT ALL PRIVILEGES ON DATABASE user_management_db TO user_management_user;
	\q
	```

3. В `settings.py` измените DATABASES:
	```python
	DATABASES = {
		 'default': {
			  'ENGINE': 'django.db.backends.postgresql',
			  'NAME': 'user_management_db',
			  'USER': 'user_management_user',
			  'PASSWORD': 'your_password',
			  'HOST': 'localhost',
			  'PORT': '',
		 }
	}
	```

4. Примените миграции:
	```bash
	python manage.py migrate
	```

5. (Опционально) Перенесите данные из SQLite:
	```bash
	python manage.py dumpdata > data.json
	# После смены БД
	python manage.py loaddata data.json
	```

6. Проверьте работу поиска: PostgreSQL корректно поддерживает регистронезависимый поиск по icontains и Lower для Unicode.
Скрипт очистки:
Как использовать
Сохрани скрипт как clean_project.py в корне проекта.

Запусти его:

bash
python clean_project.p
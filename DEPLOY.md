# Развёртывание GreenFit на PythonAnywhere

Пошаговая инструкция для публикации проекта на бесплатном хостинге
[PythonAnywhere](https://www.pythonanywhere.com). Везде ниже замените `zawisla`
на ваше имя пользователя, если оно отличается.

Итоговый адрес сайта будет: **https://zawisla.pythonanywhere.com**

---

## Подготовка

1. Зарегистрируйте бесплатный аккаунт **Beginner** на pythonanywhere.com.
2. Убедитесь, что код залит на GitHub: https://github.com/zawisla/GreenFit

---

## 1. Загрузка кода на сервер

Откройте на PythonAnywhere вкладку **Consoles → Bash** и выполните:

```bash
git clone https://github.com/zawisla/GreenFit.git
cd GreenFit
```

## 2. Виртуальное окружение и зависимости

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Переменные окружения

Создайте файл `.env` в корне проекта (он не хранится в git). Сгенерируйте
секретный ключ и впишите значения:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
nano .env
```

Содержимое `.env`:

```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=вставьте-сгенерированный-ключ
DJANGO_ALLOWED_HOSTS=zawisla.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://zawisla.pythonanywhere.com
```

Сохраните файл (`Ctrl+O`, `Enter`, `Ctrl+X`).

## 4. База данных, данные и статика

```bash
python manage.py migrate
python manage.py seed_plants          # 14 категорий, 133 растения с фото
python manage.py createsuperuser       # учётная запись администратора
python manage.py collectstatic --noinput
```

`seed_plants` также копирует фотографии растений в папку `media/plants/`.

## 5. Настройка веб-приложения

1. Откройте вкладку **Web → Add a new web app**.
2. Выберите **Manual configuration** и **Python 3.13**.
3. В разделе **Virtualenv** укажите путь: `/home/zawisla/GreenFit/.venv`
4. В разделе **Code** задайте:
   - **Source code:** `/home/zawisla/GreenFit`
   - **Working directory:** `/home/zawisla/GreenFit`
5. Откройте **WSGI configuration file** (ссылка в разделе Code) и замените его
   содержимое на:

```python
import os
import sys

path = "/home/zawisla/GreenFit"
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["DJANGO_SETTINGS_MODULE"] = "greenfit.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Сохраните файл.

## 6. Статические и медиафайлы

На вкладке **Web → Static files** добавьте две записи:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/zawisla/GreenFit/staticfiles` |
| `/media/`  | `/home/zawisla/GreenFit/media` |

> Карта `/media/` обязательна — через неё отдаются фотографии растений
> (при `DEBUG=False` Django их сам не раздаёт).

## 7. Запуск

Нажмите большую зелёную кнопку **Reload** на вкладке Web и откройте
**https://zawisla.pythonanywhere.com**.

После публикации добавьте ссылку на сайт в `README.md` и в файл задания.

---

## Обновление сайта после изменений

```bash
cd ~/GreenFit
source .venv/bin/activate
git pull
pip install -r requirements.txt      # если менялись зависимости
python manage.py migrate             # если менялись модели
python manage.py collectstatic --noinput
```

Затем нажмите **Reload** на вкладке Web.

---

## Возможные проблемы

- **DisallowedHost / 400** — проверьте `DJANGO_ALLOWED_HOSTS` в `.env`.
- **Ошибка CSRF при входе** — проверьте `DJANGO_CSRF_TRUSTED_ORIGINS`.
- **Нет стилей (CSS)** — выполните `collectstatic` и проверьте карту `/static/`.
- **Не видно фотографий** — проверьте карту `/media/` и что `seed_plants`
  отработал без ошибок.
- **Журнал ошибок** доступен на вкладке Web → Error log.

> Бесплатный аккаунт использует SQLite — этого достаточно. Чтобы перейти на
> MySQL (бонус за продакшен-БД), создайте базу на вкладке **Databases** и
> добавьте в `.env` строку
> `DATABASE_URL=mysql://пользователь:пароль@хост/имя_базы`, затем установите
> драйвер `pip install mysqlclient` и повторите `migrate` и `seed_plants`.

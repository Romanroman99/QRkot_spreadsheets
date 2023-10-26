# QRkot_spreadseets

# Проект: Google API для приложение Благотворительного фонда поддержки котиков QRKot

## Описание проекта:
API сервис по сбору средств для благотворительных проектов.

## Использованные технологии:
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- SQLite
- Google API 

### Инструкция по установке

1. Клонировать репозиторий и перейти в него:

```
git clone https://github.com/vartexxx/cat_charity_fund.git
cd cat_charity_fund
```

2. Создать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/bin/activate (для Linux/macOS)
venv\Scripts\activate (для Windows)
```

3. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Создать и заполнить файл конфигурации .env по шаблону:

APP_TITLE=Название
DESCRIPTION=Описание
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET=Секретный ключ


5. Применить миграции:
```
alembic upgrade head
```

6. Запустить проект:
```
uvicorn app.main:app --reload
```

Теперь вы можете открыть приложение в браузере и начать пользоваться функциональностью фонда.


### Автор:
Роман Романцов
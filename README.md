# Проект Syola

### Описание ###

Проект **Syola**  является неофициальным ресурсом поселения с. Сёла


***


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
bash
git clone https://github.com/taren4ik/Sela
cd Sela
```

Cоздать и активировать виртуальное окружение:

```
bash
python -m venv venv
```

Для Unix-систем:
```
bash
source venv/bin/activate
```

Для windows-систем:
```
bash
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

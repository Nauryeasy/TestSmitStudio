Установка make
```
apt install make
```

После этого необходимо создать виртуальную среду Python.


Установка poetry
```
pip install poetry
```

Далее необходимо установить зависимости
```
poetry install
```

После этого нужно либо переименовать .env.example в .env, либо создать .env по подобию .env.example.

Для запуска приложения
```
make all
```
# Быки и коровы

Это приложение реализует известную игру [быки и коровы](https://ru.wikipedia.org/wiki/Быки_и_коровы).
Человек играет с компьютером, поддерживаются два режима: пользователь
может угадывать число или загадывать его.

Также поддерживается локальное хранение таблицы лучших результатов.

Проект использует библиотеку PySide2 для работы с графическим интерфейсом.

## Работа с программой

Для начала игры нужно выбрать режим, а дальше вводить варианты ответа или
отвечать на поставленные компьютером вопросы.

При некорректном вводе или других ошибках программа сообщит об этом пользователю,
и можно будет начать игру заново.

В режиме угадывания после успешной игры можно при желании внести свое имя в таблицу лучших результатов.
Таблица сохраняется между запусками программы.

## Дополнительная информация

Программа была написана в рамках
[школьного проекта](https://server.179.ru/wiki/?page=Informatika/Arxiv/20_21/11_V)
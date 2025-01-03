# Эмулятор Оболочки

Это базовый эмулятор командной оболочки, реализованный на Python. Он поддерживает виртуальную файловую систему, загружаемую из tar-архива, и предоставляет несколько общих команд оболочки.

## Возможности

- **Виртуальная файловая система:** Загружает файловую систему из tar-архива.
- **Базовые команды оболочки:**
  - `ls [путь]`: Выводит содержимое каталога.
  - `cd <путь>`: Меняет текущий каталог.
  - `tail <файл>`: Отображает последние 10 строк файла.
  - `find <файл>`: Ищет файл и отображает его путь.
  - `help`: Показывает доступные команды.
  - `exit`: Выход из эмулятора
- **Логирование:** Записывает все выполненные команды в CSV-файл.

## Как запустить

1.  **Склонируйте репозиторий:**
    ```bash
    git clone <ссылка_на_репозиторий>
    cd <папка_репозитория>
    ```
2.  **Подготовьте tar-архив:**
    Создайте tar-архив (`.tar`), содержащий структуру файловой системы с корневой папкой `fs`. Для удобства был создан файл `utils/create_test_fs.py`, который создает пример структуры файловой системы.

    - Пример структуры файлов внутри tar-архива:

    ```
    fs/
    ├── dir1/
    │   ├── file1.txt
    │   └── file2.txt
    └── dir2/
        └── file3.txt

    ```

3.  **Запустите эмулятор:**
    ```bash
    python emulator.py -u <имя_пользователя> -o <имя_хоста> -f <путь_к_архиву.tar> -l <путь_к_файлу_журнала>
    ```
    - Замените `<имя_пользователя>` желаемым именем пользователя (по умолчанию `guest`).
    - Замените `<имя_хоста>` желаемым именем хоста (по умолчанию `localhost`).
    - Замените `<путь_к_архиву.tar>` фактическим путем к вашему файлу tar-архива.
    - Замените `<путь_к_файлу_журнала>` фактическим путем, куда вы хотите сохранить файл журнала. (по умолчанию `emulator.log`)

## Пример

```bash
python emulator.py -u testuser -o myhost -f test_fs.tar -l myemulator.log
testuser@myhost:/fs> ls
dir1  dir2
testuser@myhost:/fs> cd dir1
testuser@myhost:/fs/dir1> ls
file1.txt  file2.txt
testuser@myhost:/fs/dir1> tail file1.txt
Это первая строка
Это вторая строка
testuser@myhost:/fs/dir1> find file3.txt
/fs/dir2/file3.txt
testuser@myhost:/fs/dir1> exit
```

## Тесты

Тесты находятся в файле `./tests.py`
Запуск тестов:

```bash
python -m unittest tests.py
```

@echo off

echo Запуск автотестов...
python -m unittest discover -s tests -v

if errorlevel 1 (
    echo Тесты не пройдены. Запуск программы отменен.
    exit /b 1
)

echo Все тесты пройдены!
echo Запуск программы...

python src\main.py %*
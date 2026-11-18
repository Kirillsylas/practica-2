#!/bin/bash

echo "Запуск автотестов..."
python3 -m unittest discover -s tests -v

if [ $? -ne 0 ]; then
    echo "Тесты не пройдены. Запуск программы отменён."
    exit 1
fi

echo "Все тесты пройдены!"
echo "Запуск программы..."

python3 src/main.py "$@"
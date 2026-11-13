import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

def check_package(value):
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", value):
        raise argparse.ArgumentTypeError(
            "Имя пакета содержит недопустимые символы"
        )
    return value

def check_version(value):
    if not re.fullmatch(r"\d+(\.\d+)*", value):
        raise argparse.ArgumentTypeError(
            "Версия должна иметь формат, например 1.0 или 2.1.3"
        )
    return value

def check_filename(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("Имя файла не может быть пустым")

    if Path(value).suffix.lower() != ".png":
        raise argparse.ArgumentTypeError(
            "Файл изображения должен иметь расширение .png"
        )

    return value

parser = argparse.ArgumentParser(
    description="Инструмент визуализации графа зависимостей"
)

parser.add_argument(
    "--package",
    required=True,
    type=check_package,
    help="Имя анализируемого пакета"
)

parser.add_argument(
    "--repo",
    required=True,
    help="URL или путь к тестовому репозиторию"
)

parser.add_argument(
    "--repo-mode",
    required=True,
    choices=["local", "remote"],
    help="Режим репозитория: local или remote"
)

parser.add_argument(
    "--version",
    required=True,
    type=check_version,
    help="Версия анализируемого пакета"
)

parser.add_argument(
    "--output",
    default="graph.png",
    type=check_filename,
    help="Имя выходного файла"
)

parser.add_argument(
    "--ascii",
    action="store_true",
    help="Вывод зависимостей в виде ASCII-дерева"
)

parser.add_argument(
    "--filter",
    default="",
    help="Подстрока для фильтрации пакетов"
)

args = parser.parse_args()

if args.repo_mode == "local":
    if not Path(args.repo).exists():
        parser.error("Указанный локальный репозиторий не существует")

elif args.repo_mode == "remote":
    url = urlparse(args.repo)

    if url.scheme not in ("http", "https") or not url.netloc:
        parser.error("Укажите правильный URL репозитория (http или https)")

print("\nПараметры программы:")
print("------------------------------")
print(f"Имя пакета: {args.package}")
print(f"Репозиторий: {args.repo}")
print(f"Режим репозитория: {args.repo_mode}")
print(f"Версия пакета: {args.version}")
print(f"Имя файла изображения: {args.output}")
print(f"ASCII-дерево: {args.ascii}")
print(f"Фильтр пакетов: {args.filter}")
print("------------------------------")
print("Настройки успешно проверены!")

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


# Проверка имени пакета
def check_package(value):
    if not re.fullmatch(r"(@[a-z0-9._-]+/)?[a-z0-9._-]+", value):
        raise argparse.ArgumentTypeError(
            "Некорректное имя пакета"
        )
    return value


# Проверка URL или пути к репозиторию
def check_repo(value):
    return value


# Проверка версии пакета
def check_version(value):
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise argparse.ArgumentTypeError(
            "Версия должна иметь формат X.Y.Z, например 4.18.2"
        )
    return value


# Проверка имени выходного файла
def check_output(value):
    if Path(value).suffix.lower() not in (".png", ".svg"):
        raise argparse.ArgumentTypeError(
            "Файл должен иметь расширение .png или .svg"
        )
    if Path(value).name != value or value in (".", ".."):
        raise argparse.ArgumentTypeError(
            "Укажите имя файла без пути к папке"
        )
    return value


# Проверка параметров программы
def validate_args(args):
    if args.repo_mode == "remote":
        url = urlparse(args.repo)
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ValueError(
                "Для remote необходимо указать корректный URL"
            )

    if args.repo_mode == "local":
        if not Path(args.repo).exists():
            raise ValueError(
                f"Локальный репозиторий не найден: {args.repo}"
            )

    if args.filter is not None and not args.filter.strip():
        raise ValueError("Фильтр не может быть пустой строкой")


# Создание параметров командной строки
def create_parser():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей пакетов"
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
        type=check_repo,
        help="URL репозитория или путь к тестовому репозиторию"
    )

    parser.add_argument(
        "--repo-mode",
        required=True,
        choices=["remote", "local"],
        help="Режим работы с репозиторием"
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
        type=check_output,
        help="Имя файла изображения графа"
    )

    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Включить вывод зависимостей в виде ASCII-дерева"
    )

    parser.add_argument(
        "--filter",
        default=None,
        help="Подстрока для фильтрации пакетов"
    )

    return parser


# Главная функция программы
def main():
    parser = create_parser()

    try:
        args = parser.parse_args()
        validate_args(args)

        print("\nПараметры программы:")
        print("-" * 40)

        print(f"Имя пакета: {args.package}")
        print(f"Репозиторий: {args.repo}")
        print(f"Режим репозитория: {args.repo_mode}")
        print(f"Версия пакета: {args.version}")
        print(f"Имя файла изображения: {args.output}")
        print(f"ASCII-дерево: {'Да' if args.ascii else 'Нет'}")
        print(f"Фильтр пакетов: {args.filter or 'Не задан'}")

        print("-" * 40)
        print("Этап 1 успешно выполнен.")

    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
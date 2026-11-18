import argparse
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import quote, urlparse

def check_package(value):
    if not re.fullmatch(r"(@[a-z0-9._-]+/)?[a-z0-9._-]+", value):
        raise argparse.ArgumentTypeError("Некорректное имя пакета")
    return value

def check_repo(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("Репозиторий не может быть пустым")
    return value

def check_version(value):
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise argparse.ArgumentTypeError("Версия должна иметь формат X.Y.Z")
    return value

def check_output(value):
    if Path(value).suffix.lower() not in (".png", ".svg"):
        raise argparse.ArgumentTypeError("Разрешены файлы PNG и SVG")
    if Path(value).name != value:
        raise argparse.ArgumentTypeError("Укажите только имя файла")
    return value

def check_filter(value):
    if not value.strip():
        raise argparse.ArgumentTypeError("Фильтр не может быть пустым")
    return value

def get_remote_data(repo, package):
    url = repo.rstrip("/") + "/" + quote(package, safe="@")

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Dependency-Visualizer"}
        )

        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise ValueError("Пакет не найден в репозитории")
        raise ValueError(f"Ошибка HTTP: {error.code}")

    except urllib.error.URLError:
        raise ValueError("Не удалось подключиться к репозиторию")

    except json.JSONDecodeError:
        raise ValueError("Репозиторий вернул некорректный JSON")

def get_local_data(repo):
    try:
        with open(repo, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise ValueError("Файл локального репозитория не найден")

    except json.JSONDecodeError:
        raise ValueError("Локальный файл содержит некорректный JSON")

def get_dependencies(data, version):
    if not isinstance(data, dict):
        raise ValueError("Некорректная структура данных репозитория")

    versions = data.get("versions")

    if not isinstance(versions, dict):
        raise ValueError("В репозитории отсутствует список версий")

    if version not in versions:
        raise ValueError(f"Версия {version} не найдена")

    package_data = versions[version]

    if not isinstance(package_data, dict):
        raise ValueError("Некорректные данные выбранной версии")

    dependencies = package_data.get("dependencies", {})

    if not isinstance(dependencies, dict):
        raise ValueError("Некорректный список зависимостей")

    for name, dep_version in dependencies.items():
        if not isinstance(name, str) or not isinstance(dep_version, str):
            raise ValueError("Некорректная информация о зависимости")

    return dependencies

def create_parser():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей npm"
    )

    parser.add_argument("--package", required=True, type=check_package)
    parser.add_argument("--repo", required=True, type=check_repo)
    parser.add_argument(
        "--repo-mode",
        required=True,
        choices=["remote", "local"]
    )
    parser.add_argument("--version", required=True, type=check_version)
    parser.add_argument("--output", default="graph.png", type=check_output)
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--filter", default=None, type=check_filter)

    return parser

def validate_args(args):
    if args.repo_mode == "remote":
        url = urlparse(args.repo)
        if url.scheme not in ("http", "https") or not url.netloc:
            return False

    if args.repo_mode == "local":
        if not Path(args.repo).is_file():
            return False

    return True
    
def main():
    parser = create_parser()
if __name__ == "__main__":
    main()

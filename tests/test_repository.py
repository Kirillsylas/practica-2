
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from io import BytesIO
from urllib.error import HTTPError, URLError

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from main import (
    get_local_data,
    get_remote_data,
    get_dependencies
)


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repo = Path(__file__).resolve().parents[1] / "test_repo.json"

        self.data = {
            "name": "express",
            "versions": {
                "4.18.2": {
                    "dependencies": {
                        "accepts": "~1.3.8",
                        "body-parser": "1.20.1",
                        "debug": "2.6.9"
                    }
                },
                "5.0.0": {
                    "dependencies": {
                        "accepts": "~2.0.0",
                        "debug": "4.3.6"
                    }
                }
            }
        }

    def test_local_repository(self):
        data = get_local_data(str(self.repo))
        self.assertIn("versions", data)

    def test_get_dependencies(self):
        dependencies = get_dependencies(self.data, "4.18.2")
        self.assertEqual(len(dependencies), 3)
        self.assertIn("accepts", dependencies)

    def test_another_version(self):
        dependencies = get_dependencies(self.data, "5.0.0")
        self.assertEqual(len(dependencies), 2)

    def test_missing_version(self):
        with self.assertRaises(ValueError):
            get_dependencies(self.data, "9.9.9")

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            get_local_data("missing.json")

    # Проверка неправильной структуры JSON
    def test_invalid_structure(self):
        with self.assertRaises(ValueError):
            get_dependencies({}, "4.18.2")

    # Проверка пустого списка зависимостей
    def test_empty_dependencies(self):
        data = {
            "versions": {
                "1.0.0": {
                    "dependencies": {}
                }
            }
        }

        self.assertEqual(get_dependencies(data, "1.0.0"), {})

    # Проверка удаленного репозитория
    @patch("main.urllib.request.urlopen")
    def test_remote_repository(self, mock_urlopen):
        mock_urlopen.return_value = BytesIO(
            json.dumps(self.data).encode("utf-8")
        )

        result = get_remote_data(
            "https://registry.npmjs.org",
            "express"
        )

        self.assertIn("versions", result)

    # Проверка ошибки подключения
    @patch("main.urllib.request.urlopen")
    def test_connection_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Connection failed")

        with self.assertRaises(ValueError):
            get_remote_data(
                "https://registry.npmjs.org",
                "express"
            )

    # Проверка отсутствующего пакета
    @patch("main.urllib.request.urlopen")
    def test_package_not_found(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            "https://registry.npmjs.org/express",
            404,
            "Not Found",
            {},
            None
        )

        with self.assertRaises(ValueError):
            get_remote_data(
                "https://registry.npmjs.org",
                "express"
            )


if __name__ == "__main__":
    unittest.main()

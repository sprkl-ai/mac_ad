"""Проверка и поиск MAC-адресов в консоли."""

import re
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen


# Шесть пар шестнадцатеричных цифр с одинаковым разделителем.
MAC_RE = re.compile(
    r"(?<![\w:-])[0-9A-Fa-f]{2}([:-])(?:[0-9A-Fa-f]{2}\1){4}"
    r"[0-9A-Fa-f]{2}(?![\w:-])"
)


def is_mac(value):
    return MAC_RE.fullmatch(value.strip()) is not None


def find_macs(text):
    """Возвращает адреса по порядку появления, без повторов."""
    addresses = (match.group().replace("-", ":").upper()
                 for match in MAC_RE.finditer(text))
    return list(dict.fromkeys(addresses))


def save_macs(addresses, path):
    """Сохранить найденные адреса в текстовый файл (будущий этап)."""
    raise NotImplementedError("Сохранение адресов пока не реализовано")


def read_url(url):
    if urlsplit(url).scheme not in ("http", "https"):
        raise ValueError("Нужен URL с http:// или https://")
    with urlopen(url, timeout=10) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        data = response.read(1_000_001)
    if len(data) > 1_000_000:
        raise ValueError("Страница больше 1 МБ")
    return data.decode(charset, errors="replace")


def main():
    print("Поиск MAC-адресов. Пример: AA:BB:CC:DD:EE:FF")
    while True:
        print("\n1 — проверить адрес  2 — поиск в файле  3 — поиск по URL  0 — выход")
        choice = input("Выбор: ").strip()
        if choice == "0":
            return
        try:
            if choice == "1":
                value = input("MAC-адрес: ")
                print("Корректный" if is_mac(value) else "Некорректный")
                continue
            if choice == "2":
                text = Path(input("Путь к текстовому файлу: ").strip()).read_text(
                    encoding="utf-8-sig")
            elif choice == "3":
                text = read_url(input("URL страницы: ").strip())
            else:
                print("Нет такого пункта меню")
                continue
            addresses = find_macs(text)
            print("Найдено:", len(addresses))
            for address in addresses:
                print(address)
        except (OSError, UnicodeError, ValueError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()

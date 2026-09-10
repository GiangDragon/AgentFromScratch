from pathlib import Path


def read_file(path: str) -> str:
    try:
        return Path(path).expanduser().read_text(encoding="utf-8")
    except (OSError, UnicodeError) as e:
        return f"Error: {e}"


def write_file(path: str, content: str) -> str:
    try:
        file_path = Path(path).expanduser()
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Đã ghi file: {file_path}"
    except (OSError, UnicodeError) as e:
        return f"Error: {e}"

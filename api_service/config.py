import os


def _get_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    return int(value)


def _get_str(name: str, default: str) -> str:
    value = os.environ.get(name)
    if value is None:
        return default
    return value


REMBG_MODEL = _get_str("REMBG_MODEL", "u2net")
REMBG_MAX_UPLOAD_BYTES = _get_int("REMBG_MAX_UPLOAD_BYTES", 20 * 1024 * 1024)


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_service.main import app


def main() -> int:
    try:
        from fastapi.testclient import TestClient
    except Exception as e:
        print(f"missing test deps: {e}")
        return 2

    fixture = Path("tests/fixtures/car-1.jpg")
    if not fixture.exists():
        print("missing fixture tests/fixtures/car-1.jpg")
        return 2

    client = TestClient(app)
    with fixture.open("rb") as f:
        r = client.post("/api/rembg/remove", files={"file": ("car-1.jpg", f, "image/jpeg")})

    print("status", r.status_code)
    print("content-type", r.headers.get("content-type"))
    if r.status_code != 200:
        print(r.text)
        return 1

    if not r.content.startswith(b"\x89PNG\r\n\x1a\n"):
        print("response is not png")
        return 1

    out = Path("api_service/_smoke_output.png")
    out.write_bytes(r.content)
    print("wrote", str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

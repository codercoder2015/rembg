import rembg

try:
    import fastapi
    import uvicorn
except Exception as e:
    raise SystemExit(f"missing deps: {e}") from e

print("fastapi", fastapi.__version__)
print("uvicorn", uvicorn.__version__)
print("rembg", rembg.__version__)


from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from starlette.responses import Response

from rembg import __version__ as rembg_version

from .config import REMBG_MAX_UPLOAD_BYTES, REMBG_MODEL
from .rembg_service import RemoveParams, RembgService


app = FastAPI(title="rembg-api", version=rembg_version)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_service() -> RembgService:
    service: Optional[RembgService] = getattr(app.state, "rembg_service", None)
    if service is None:
        service = RembgService(default_model=REMBG_MODEL)
        app.state.rembg_service = service
    return service


async def read_upload_limited(upload: UploadFile, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    try:
        while True:
            chunk = await upload.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                raise HTTPException(status_code=413, detail="文件过大")
            chunks.append(chunk)
    finally:
        await upload.close()
    if total == 0:
        raise HTTPException(status_code=400, detail="空文件")
    return b"".join(chunks)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/rembg/remove")
async def remove_api(
    file: UploadFile = File(...),
    alpha_matting: bool = False,
    model: Optional[str] = None,
):
    content = await read_upload_limited(file, REMBG_MAX_UPLOAD_BYTES)
    service = get_service()

    try:
        out = await run_in_threadpool(
            service.remove_background,
            content,
            model=model,
            params=RemoveParams(alpha_matting=alpha_matting),
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="处理失败")

    return Response(out, media_type="image/png")


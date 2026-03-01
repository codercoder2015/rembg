# rembg API Service (FastAPI)

## 安装（CPU）

### Poetry

```bash
poetry install --extras "cpu cli"
```

### pip

```bash
pip install -e ".[cpu,cli]"
```

## 启动

在仓库根目录执行：

```bash
uvicorn api_service.main:app --host 0.0.0.0 --port 8000
```

## 接口

- `GET /health`
- `POST /api/rembg/remove`（multipart/form-data）
  - 字段：`file`（必填）
  - 参数：`alpha_matting`（可选，默认 false），`model`（可选）
  - 返回：`image/png`

## 配置（环境变量）

- `REMBG_MODEL`：默认模型名（默认 `u2net`）
- `REMBG_MAX_UPLOAD_BYTES`：上传大小限制（默认 `20971520`，20MB）
- `OMP_NUM_THREADS`：CPU 推理线程数（rembg 会读取并设置到 onnxruntime session）


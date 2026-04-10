#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. 安装 uv（若已安装则跳过）
if ! command -v uv &>/dev/null; then
  echo "[setup] 安装 uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # 让当前 shell 能找到 uv
  export PATH="$HOME/.local/bin:$PATH"
else
  echo "[setup] uv 已存在：$(uv --version)"
fi

# 2. 创建 Python venv
echo "[setup] 创建虚拟环境 venv/..."
uv venv venv

# 3. 安装依赖
echo "[setup] 安装 fastapi、uvicorn..."
uv pip install --python venv/bin/python fastapi "uvicorn[standard]"

echo "[setup] 完成。运行 ./start.sh 启动服务。"

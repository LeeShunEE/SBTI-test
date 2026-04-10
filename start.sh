#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 激活虚拟环境
source venv/bin/activate

# 用 nohup 后台启动，日志追加到 server.log
nohup python main.py >> server.log 2>&1 &
PID=$!

echo "[start] 服务已启动，PID: $PID，日志: $SCRIPT_DIR/server.log"
echo "$PID" > server.pid

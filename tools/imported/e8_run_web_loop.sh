#!/usr/bin/env bash
cd "$(dirname "$0")"
while true; do
  echo "[Web Unifier] starting..."
  npm run start || true
  echo "[Web Unifier] crashed or exited; restarting in 3s..."
  sleep 3
done

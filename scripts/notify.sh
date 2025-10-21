#!/usr/bin/env bash
set -euo pipefail
title="${1:-Warp AI}"
message="${2:-Turn complete}"
sound="${3:-Windows Notify System Generic.wav}"

# Call Windows host PowerShell from WSL; strip CR to keep logs clean
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe \
  -NoProfile -ExecutionPolicy Bypass \
  -File "C:\Users\Dawson\bin\warp-notify.ps1" \
  -Title "$title" -Message "$message" -Sound "$sound" | tr -d '\r'
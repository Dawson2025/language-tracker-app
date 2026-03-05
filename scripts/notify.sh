#!/usr/bin/env bash
# resource_id: d988da5a-fc5c-4fc2-918b-26bee7376df3
set -euo pipefail
title="${1:-Warp AI}"
message="${2:-Turn complete}"
sound="${3:-Windows Notify System Generic.wav}"

# Call Windows host PowerShell from WSL; strip CR to keep logs clean
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe \
  -NoProfile -ExecutionPolicy Bypass \
  -File "C:\Users\Dawson\bin\warp-notify.ps1" \
  -Title "$title" -Message "$message" -Sound "$sound" | tr -d '\r'
---
name: nuttx-lckfb-esp32s3
description: Use when working with the LCKFB ESP32S3 board including building, flashing, accessing interact terminal.
---

# LCKFB ESP32S3 Board Interaction Guide

This guide provides workflows for building, flashing, and interacting with the LCKFB SZPI ESP32S3 board in NuttX.

## Build Output Management

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output. Always append `| tail -n 100` when redirecting to files or viewing logs.

## 1. Build Firmware

```bash
# Configure for LCKFB ESP32S3 board using nxtool
python3 boards/tool/nxtool.py configure \
  ../boards/lckfb-szpi-esp32s3/configs/app \
  nuttx

# Apply configuration and build firmware (limit output)
make -C nuttx olddefconfig
make -C nuttx -j8 2>&1 | tail -n 100
```

## 2. Flash Firmware to Board

```bash
# Flash firmware using nxtool
python3 boards/tool/nxtool.py flash nuttx --port /dev/ttyACM0
```

## 3. Access Serial Console

```bash
# Create background tmux session with picocom for NSH console (runs continuously, use nsh for example session name)
tmux new-session -d -s nsh 'picocom -b 115200 /dev/ttyUSB0'

# Send commands to NSH shell
tmux send-keys -t nsh Enter
tmux send-keys -t nsh 'ps' Enter
tmux send-keys -t nsh 'ls /dev' Enter
tmux send-keys -t nsh 'free' Enter

# View serial output (capture last 100 lines)
tmux capture-pane -p -t nsh | tail -n 100

# View more lines
tmux capture-pane -p -t nsh | tail -n 500

# Send special keys
tmux send-keys -t nsh C-c   # Ctrl+C (interrupt)
tmux send-keys -t nsh C-d   # Ctrl+D (EOF)

# List all tmux sessions
tmux list-sessions

# Kill NSH console session when done
tmux kill-session -t nsh

# Common NSH commands
help                    # Show available commands
ps                      # List running tasks
free                    # Show memory usage
ls /dev                 # List device nodes
```

## 4. Reset Board

```bash
# Reset board
esptool --chip esp32s3 --port /dev/ttyACM0 run
```

## Critical Rules

1. Reuse the nsh session if it already exist
2. The nsh shell session only need to create once
3. Always send Enter to flush error input on nsh session create

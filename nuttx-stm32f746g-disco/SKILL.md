---
name: nuttx-stm32f746g-disco
description: Workflows and guides for building, flashing, running, and interacting with STM32F746G-DISCO board (for hardware or Renode emulator). Use when work with NuttX for STM32F746G-DISCO board.
---

## 1. Build Firmware

```bash
# Configure and build for NuttX builtin config
cmake -S nuttx -B build -G Ninja -DBOARD_CONFIG=stm32f746g-disco:nsh

# Or configure for user specified config, for this example,
# there have a path/to/config/apps/defconfig but only the dir path is necessary
cmake -S nuttx -B build -G Ninja -DBOARD_CONFIG=path/to/config/apps

# Available configurations: nsh, fb, lvgl, netnsh, audio, nxterm, nxdemo etc

# Build firmware (output limited to prevent terminal overflow)
cmake --build build | tail -n 100
```

The firmware ELF file is generated as `build/nuttx`.

**Rebuild after code changes**:
```bash
cmake --build build | tail -n 100
```

## 2. Start Renode Emulation

```bash
# Start Renode monitor in detached tmux session
tmux new-session -d -s renode "renode --console -e 'i @boards/stm32f746g-disco/stm32f746g-disco.resc'"
```

In the Renode monitor prompt:

```bash
# Clear history before starting to make it easier to detect startup
tmux clear-history -t renode
tmux send-keys -t renode "start" Enter
```

The Renode emulation is now running with a socket terminal on port 12345.

## 3. Wait for Emulation Ready

```bash
# Wait for Renode machine to start
sleep 3
tmux capture-pane -t renode -p
```

This ensures the Renode emulation is running before connecting to the terminal.

## 4. Access Serial Console

```bash
# Create serial console tmux session (detached from Renode)
tmux new-session -d -s renode-terminal "telnet localhost 12345"
```

You should see the NuttX boot sequence followed by the NSH prompt:

```
NuttShell (NSH) NuttX-12.12.0
nsh>
```

### Send Commands to Serial Console

```bash
# Send NSH commands without attaching
tmux send-keys -t renode-terminal "help" Enter
tmux send-keys -t renode-terminal "ls /dev" Enter
```

## 5. Reload Firmware

```bash
# 1. Rebuild firmware
cmake --build build | tail -n 100

# 2. Stop emulation
tmux send-keys -t renode "stop" Enter

# 3. Load new firmware, MUST add "@" as file prefix
tmux send-keys -t renode "sysbus LoadELF @build/nuttx" Enter

# 4. Clear history and start emulation
tmux clear-history -t renode
tmux send-keys -t renode "start" Enter

# 5. Wait for emulation to be ready
sleep 3
tmux capture-pane -t renode -p
```

## 6. Session Configuration

| Setting | Value |
|---------|-------|
| **Renode Monitor Session** | `renode` |
| **Terminal Session** | `renode-terminal` |
| **UART Device** | `sysbus.usart1` |
| **Baud Rate** | 115200 (8N1) |
| **Platform Script** | `@boards/stm32f746g-disco/stm32f746g-disco.resc` |

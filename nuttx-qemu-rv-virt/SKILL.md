---
name: nuttx-qemu-rv-virt
description: Workflows for building, running, and interacting with QEMU RISC-V Virt board for NuttX simulation and testing. Use when working with QEMU-based RV-Virt board for NuttX.
---

# QEMU RV-Virt Board Interaction Guide

This guide provides workflows for building, running, and interacting with the QEMU RISC-V Virt board in NuttX.

## Build Output Management

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output. Always append `| tail -n 100` when redirecting to files or viewing logs.

## 1. Build Firmware (CMake)

```bash
# Configure for rv-virt:nsh board using CMake
cmake -S nuttx -B build -DBOARD_CONFIG=rv-virt:nsh

# Build firmware (limit output)
cmake --build build -j32 2>&1 | tail -n 100
```

## 2. Determine Build Architecture (32-bit vs 64-bit)

```bash
# Check if built firmware is RV32 or RV64
file path/to/nuttx
```

## 3. Run QEMU

**Critical: QEMU must be restarted to load newly built ELF files.** Unlike hardware boards that can be flashed while running, QEMU does not support live reload.

**Use tmux for session management to enable output capture and session reuse.**

```bash
# Create background tmux session for QEMU with RV32
tmux new-session -d -s qemu 'qemu-system-riscv32 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv32 \
  -bios none \
  -kernel path/to/nuttx \
  -nographic'

# Create background tmux session for QEMU with RV64
tmux new-session -d -s qemu 'qemu-system-riscv64 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv64 \
  -bios none \
  -kernel path/to/nuttx \
  -nographic'
```

## 4. Access NSH Console

```bash
# View serial output (capture last 100 lines)
tmux capture-pane -p -t qemu | tail -n 100

# View more lines
tmux capture-pane -p -t qemu | tail -n 500

# Send commands to NSH shell
tmux send-keys -t qemu Enter
tmux send-keys -t qemu 'ps' Enter
tmux send-keys -t qemu 'ls /dev' Enter
tmux send-keys -t qemu 'free' Enter
tmux send-keys -t qemu 'uname -a' Enter

# Send special keys
tmux send-keys -t qemu C-c   # Ctrl+C (interrupt)

# List all tmux sessions
tmux list-sessions

# Common NSH commands
help                    # Show available commands
ps                      # List running tasks
free                    # Show memory usage
ls /dev                 # List device nodes
uname -a                # Show system information
```

## 5. (Optional) HostFS: Access Host Files from NSH

> This feature requires `CONFIG_FS_HOSTFS=y` in your kernel configuration.

Mount a host directory to access files from NuttX NSH:

```bash
# Mount host directory as /host (requires CONFIG_FS_HOSTFS=y in defconfig)
tmux send-keys -t qemu 'mount -t hostfs -o fs=/home/user /host' Enter

# Read host file
tmux send-keys -t qemu 'cat /host/etc/passwd' Enter

# Write to host file (overwrite)
tmux send-keys -t qemu 'echo "hello" > /host/test.txt' Enter

# Append to host file
tmux send-keys -t qemu 'echo "world" >> /host/test.txt' Enter

# Unmount when done
tmux send-keys -t qemu 'umount /host' Enter
```

> **Note:** Directory listing does not work with hostfs. Use direct file paths to access files.

## 7. Reload New Build

Since QEMU does not support live reload, follow this workflow:

```bash
# Step 1: Kill the running QEMU session
tmux kill-session -t qemu

# Step 2: Rebuild firmware
cmake --build build -j32 2>&1 | tail -n 100

# Step 3: Restart QEMU with the new ELF
tmux new-session -d -s qemu 'qemu-system-riscv32 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv32 \
  -bios none \
  -kernel path/to/nuttx \
  -nographic'
```

## 8. Exit QEMU

```bash
# Kill QEMU tmux session when done
tmux kill-session -t qemu
```

# Critical Rules
1. **Always restart QEMU after rebuilding** - QEMU does not support live reload

---
name: nuttx-qemu-rv-virt
description: Use when working with QEMU-based RV-Virt board for NuttX simulation and testing.
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

## 2. Run QEMU

**Critical: QEMU must be restarted to load newly built ELF files.** Unlike hardware boards that can be flashed while running, QEMU does not support live reload.

```bash
# Run QEMU with RV32 (uses build/nuttx)
qemu-system-riscv32 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv32 \
  -bios none \
  -kernel build/nuttx \
  -nographic

# Run QEMU with RV64 (uses nuttx/nuttx)
qemu-system-riscv64 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv64 \
  -bios none \
  -kernel nuttx/nuttx \
  -nographic
```

## 3. Reload New Build

Since QEMU does not support live reload, follow this workflow:

```bash
# Step 1: Kill the running QEMU process
# Press Ctrl+A, then X to exit QEMU, or find and kill the process
pkill -f qemu-system-riscv

# Step 2: Rebuild firmware
cmake --build build -j32 2>&1 | tail -n 100

# Step 3: Restart QEMU with the new ELF
qemu-system-riscv32 \
  -semihosting \
  -M virt,aclint=on \
  -cpu rv32 \
  -bios none \
  -kernel build/nuttx \
  -nographic
```

## 4. Access NSH Console

QEMU runs NSH directly in the terminal when started with `-nographic`.

```bash
# Common NSH commands (run in QEMU console)
help                    # Show available commands
ps                      # List running tasks
free                    # Show memory usage
ls /dev                 # List device nodes
uname -a                # Show system information
```

## 5. Exit QEMU

```bash
# Press Ctrl+A followed by X to exit QEMU
# Or send Ctrl+C to interrupt and then Ctrl+A, X
```

## Critical Rules

1. **Always restart QEMU after rebuilding** - QEMU does not support live reload
2. Kill existing QEMU process before rebuilding to avoid port conflicts
3. Use `-nographic` for terminal-based NSH access
4. Save important output before exiting QEMU (no persistent serial capture)
5. For rv32 builds, output is at `build/nuttx`; for rv64, it's at `nuttx/nuttx`

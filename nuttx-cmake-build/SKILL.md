---
name: nuttx-cmake-build
description: Builds NuttX with CMake for faster compilation and better dependency tracking. Use when building NuttX with CMake, managing multiple configurations simultaneously, or using out-of-tree board configurations.
---

# NuttX CMake Build

## BOARD_CONFIG Syntax

BOARD_CONFIG supports two formats:

| Format | Example | Use Case |
|--------|---------|----------|
| `<board>:<config>` | `rv-virt:nsh` | In-tree boards |
| Absolute path | `/path/to/configs/app` | Out-of-tree boards |

**Configuration examples:**
```bash
# Out-of-tree board (absolute path)
cmake -GNinja -DBOARD_CONFIG=/home/user/myboard/configs/nsh -B build nuttx

# Relative path from build dir
cmake -GNinja -DBOARD_CONFIG=../../myboard/configs/nsh -B build nuttx

# In-tree board (shorthand)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build nuttx
```

| Component | Description | Example |
|-----------|-------------|---------|
| `<board>` | Board directory name | `rv-virt`, `stm32f746g-disco` |
| `<config>` | Config directory name | `nsh`, `app`, `netnsh` |
| `<build-dir>` | Build output directory | `build/`, `../builds/nuttx` |
| `<nuttx-source>` | Path to NuttX source root | `nuttx/`, `/projects/nuttx` |

## 1. Configure and Build

```bash
# Configure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build nuttx

# Build
ninja -C build -j8 2>&1 | tail -n 100

# Check outputs
ls -lh build/nuttx*
```

## 2. Find Available Configs

```bash
ls nuttx/boards/<arch>/<vendor>/<board>/configs/
# Example: ls nuttx/boards/risc-v/qemu-rv/rv-virt/configs/
```

## 3. Rebuild After Changes

```bash
# Edit source, then rebuild
ninja -C build 2>&1 | tail -n 100
```

## 4. Change Configuration

```bash
# Modify .config (kconfig-tweak or menuconfig)
cmake -B build nuttx
ninja -C build -j8 2>&1 | tail -n 100
```

## 5. Clean Build

```bash
# Full clean: delete and recreate
rm -rf build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build nuttx
ninja -C build -j8 2>&1 | tail -n 100

# Soft clean: keep config
ninja -C build clean
cmake -B build nuttx
ninja -C build -j8 2>&1 | tail -n 100
```

## 6. Multiple Configurations

```bash
# Debug
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-debug nuttx
ninja -C build-debug -j4

# Release
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-release nuttx
ninja -C build-release -j4

# Different board
cmake -GNinja -DBOARD_CONFIG=stm32f4discovery:nsh -B build-stm32 nuttx
ninja -C build-stm32 -j4
```

## 7. Build Targets

```bash
ninja -C build              # All
ninja -C build nuttx        # Kernel only
ninja -C build apps         # Apps only
ninja -C build -v           # Verbose
```

## 8. View Configuration

```bash
grep CONFIG_EXAMPLES_HELLO build/.config
head -n 100 build/.config
```

## Troubleshooting

```bash
# More output
ninja -C build -j8 2>&1 | tail -n 200

# Clear cache
rm -rf build/CMakeCache.txt
cmake -B build nuttx

# Full reset
rm -rf build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build nuttx
ninja -C build -j8 2>&1 | tail -n 100
```

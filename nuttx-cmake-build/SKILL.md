---
name: nuttx-cmake-build
description: Build NuttX RTOS firmware using the modern CMake build system with Ninja backend. Use this when you want faster builds, better dependency tracking, multiple build configurations in parallel, out-of-tree builds, or modern development workflows.
---

# NuttX CMake Build Workflows

## Build Output Management

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output to the last 100 lines. Adjust as needed:
- `tail -n 50` - Minimal output
- `tail -n 100` - Balanced (recommended)
- `tail -n 200` - More context
- Remove `| tail -n N` for full output

## Configuration Syntax

```
cmake -GNinja -DBOARD_CONFIG=<board-name>:<config-name> -B <build-dir> <nuttx-source-dir>
```

- `<board-name>`: Board directory (e.g., `rv-virt`, `stm32f4discovery`)
- `<config-name>`: Configuration directory (e.g., `nsh`, `knsh`)
- `<build-dir>`: Build artifacts location (e.g., `build`, `../builds/nuttx`)
- `<nuttx-source-dir>`: Path to NuttX source code

**Note**: Some boards (ESP32S3, ESP32) use custom build systems. Use Makefile for these boards.

## Essential Workflows

### 1. Find Available Configurations

```bash
# List available configurations by directory structure
ls nuttx/boards/<arch>/<vendor>/<board>/configs/

# Example for RISC-V QEMU:
ls nuttx/boards/risc-v/qemu-rv/rv-virt/configs/
# Output: nsh, knsh, knsh64, netnsh, etc.
```

### 2. Initial Configuration and Build

```bash
# Configure and create build directory
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Apply config changes (requires nuttx-config-management skill)
cmake -B path/to/build path/to/nuttx

# Build
ninja -C path/to/build -j8 2>&1 | tail -n 100

# Check output
ls -lh path/to/build/nuttx
# nuttx       - Main ELF binary
# nuttx.hex   - Hex format
# nuttx.bin   - Raw binary
```

### 3. Incremental Build After Code Changes

```bash
# Make code changes
vim path/to/source/file.c

# Rebuild
ninja -C path/to/build 2>&1 | tail -n 100
```

### 4. Apply Configuration Changes

```bash
# Modify .config using kconfig-tweak (requires nuttx-config-management skill)
# kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO

# Apply changes to build system
cmake -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### 5. Multiple Build Configurations in Parallel

```bash
# Debug and release builds
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-debug path/to/nuttx
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-release path/to/nuttx

# Build both in parallel
ninja -C build-debug -j4 &
ninja -C build-release -j4 &
wait
```

### 6. Different Boards in Parallel

```bash
# Configure multiple boards
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-rv-virt path/to/nuttx
cmake -GNinja -DBOARD_CONFIG=stm32f4discovery:nsh -B build-stm32 path/to/nuttx

# Build both in parallel
ninja -C build-rv-virt -j4 &
ninja -C build-stm32 -j4 &
wait
```

### 7. Out-of-Tree Builds

```bash
# Build outside source tree (keeps source clean)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B ../builds/nuttx-debug path/to/nuttx
ninja -C ../builds/nuttx-debug

# Another configuration
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B ../builds/nuttx-release path/to/nuttx
ninja -C ../builds/nuttx-release
```

### 8. Clean and Full Rebuild

```bash
# Delete build directory
rm -rf path/to/build

# Reconfigure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### 9. Clean and Reconfigure

```bash
# Clean built files
ninja -C path/to/build clean

# Reconfigure
cmake -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### 10. Build Specific Targets

```bash
# Build all
ninja -C path/to/build all

# Build kernel only
ninja -C path/to/build nuttx

# Build apps only
ninja -C path/to/build apps

# Build specific application
ninja -C path/to/build hello

# Verbose build output
ninja -C path/to/build -v 2>&1 | tail -n 100
```

### 11. Save Current Configuration

```bash
# Copy current configuration for reuse
cp path/to/build/.config my-custom-defconfig

# Edit and use for future builds
```

## Configuration Management

```bash
# View specific option
grep CONFIG_EXAMPLES_HELLO path/to/build/.config

# View related options
grep "CONFIG_I2C" path/to/build/.config

# View first 100 lines
head -n 100 path/to/build/.config
```

## Advanced CMake Options

```bash
# Specify generator (Ninja is recommended)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx

# Enable verbose output
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx --verbose

# Specify toolchain file (cross-compilation)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx -DCMAKE_TOOLCHAIN_FILE=path/to/toolchain.cmake

# Enable ccache
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache

# Generate compile_commands.json for IDE integration
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

## Troubleshooting

```bash
# View more build output
ninja -C path/to/build -j8 2>&1 | tail -n 200

# Save full build log
ninja -C path/to/build -j8 2>&1 > build.log
tail -n 200 build.log

# Verify configuration
cmake -B path/to/build path/to/nuttx

# Check specific options
grep "CONFIG_YOUR_OPTION=y" path/to/build/.config

# Clear CMake cache
rm -rf path/to/build/CMakeCache.txt
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Force complete clean
rm -rf path/to/build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

## When to Use CMake

- Faster builds with Ninja backend
- Better dependency tracking
- Multiple build configurations (debug/release, multiple boards)
- Out-of-tree builds for clean source directories
- Modern development workflows and IDE integration

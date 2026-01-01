---
name: nuttx-makefile-build
description: Builds NuttX firmware using the traditional Makefile system for maximum board compatibility. Supports boards like ESP32S3 that require custom build systems and legacy projects. Use when building NuttX with Makefile system for maximum compatibility or working with boards requiring custom build systems.
---

# NuttX Makefile Build Workflows

## Build Output Management

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output to the last 100 lines. Adjust as needed:
- `tail -n 50` - Minimal output
- `tail -n 100` - Balanced (recommended)
- `tail -n 200` - More context
- Remove `| tail -n N` for full output

## Configuration Syntax

```
<board-name>:<config-name>
```

- `<board-name>`: Board directory (e.g., `rv-virt`, `stm32f4discovery`)
- `<config-name>`: Configuration directory (e.g., `nsh`, `knsh`)

## Essential Workflows

### 1. Find Available Configurations

```bash
cd path/to/nuttx

# List all configurations
./tools/configure.sh -L

# List for specific board (partial match)
./tools/configure.sh -L rv-virt

# Or list directory structure
ls nuttx/boards/<arch>/<vendor>/<board>/configs/
```

### 2. Initial Configuration and Build

```bash
cd path/to/nuttx

# Configure board
./tools/configure.sh rv-virt:nsh

# Build (requires nuttx-config-management skill for config changes)
make olddefconfig
make -j8 2>&1 | tail -n 100

# Check output
ls -lh path/to/nuttx
# nuttx       - Main ELF binary
# nuttx.hex   - Hex format
# nuttx.bin   - Raw binary
```

### 3. Incremental Build After Code Changes

```bash
cd path/to/nuttx

# Make code changes
vim path/to/source/file.c

# Rebuild
make -j$(nproc) 2>&1 | tail -n 100
```

### 4. Apply Configuration Changes

```bash
cd path/to/nuttx

# Modify .config using kconfig-tweak (requires nuttx-config-management skill)
# kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO

# Apply changes and rebuild
make olddefconfig
make -j8 2>&1 | tail -n 100
```

### 5. Switch Between Configurations

```bash
cd path/to/nuttx

# Clean previous build
make distclean

# Configure for new board/config
./tools/configure.sh stm32f4discovery:knsh

# Build
make -j8 2>&1 | tail -n 100
```

### 6. Clean and Full Rebuild

```bash
cd path/to/nuttx

# Full clean
make distclean

# Reconfigure
./tools/configure.sh rv-virt:nsh

# Rebuild
make olddefconfig
make -j8 2>&1 | tail -n 100
```

### 7. Save Current Configuration

```bash
cd path/to/nuttx

# Save as minimal defconfig
make savedefconfig

# Copy to board's configs directory
cp defconfig boards/<arch>/<vendor>/<board>/configs/myconfig/defconfig
```

### 8. Build Specific Targets

```bash
# Build all
make all

# Build kernel only
make kernel

# Build apps only
make apps

# Build specific application
make apps/examples/hello
```

## Configuration Management

```bash
# View specific option
grep CONFIG_EXAMPLES_HELLO .config

# View related options
grep "CONFIG_I2C" .config

# View first 100 lines
head -n 100 .config
```

## Advanced Configure.sh Options

```bash
# List all configurations
./tools/configure.sh -L

# Enforce distclean before configuration
./tools/configure.sh -E rv-virt:nsh

# Auto distclean if config changed
./tools/configure.sh -e rv-virt:nsh

# Specify custom apps directory
./tools/configure.sh -a path/to/my-apps rv-virt:nsh

# Out-of-tree custom boards
./tools/configure.sh path/to/mycustomboards/myboardname/config/nsh
```

## Troubleshooting

```bash
# View more build output
make -j8 2>&1 | tail -n 200

# Save full build log
make -j8 2>&1 > build.log
tail -n 200 build.log

# Verify configuration
make olddefconfig

# Force complete clean
make distclean
rm -rf .config

# Start fresh
./tools/configure.sh rv-virt:nsh
make -j8 2>&1 | tail -n 100
```

## When to Use Makefile

- Maximum compatibility with all boards
- Boards with custom build systems (ESP32S3, ESP32)
- Legacy projects using Makefile
- Simple builds without out-of-tree needs

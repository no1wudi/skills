---
name: nuttx-makefile-build
description: Builds NuttX using the traditional Makefile system for maximum board compatibility. Use when building NuttX with Makefile, working with custom build systems (ESP32S3), or legacy projects.
---

# NuttX Makefile Build

## Workflow

1. **Determine target board and config**:
   - **In-tree boards**: `<board>:<config>` format (e.g., `rv-virt:nsh`)
     - If user specifies a board, use that board
     - If user doesn't specify a board, default to `rv-virt`
     - If user specifies a config, use that config
     - If user doesn't specify a config, default to `nsh`
   - **Out-of-tree/custom boards**: Use absolute path or directory path
     - If user specifies a path, use that path directly
   - Result: `<board>:<config>`, absolute path, or directory path

2. **Configure**: `./tools/configure.sh <target>`

3. **Build**: `make -j$(nproc) 2>&1 | tail -n 100`

## BOARD_CONFIG Syntax

BOARD_CONFIG uses `<board>:<config>` format:

| Format | Example | Use Case |
|--------|---------|----------|
| `<board>:<config>` | `rv-virt:nsh` | In-tree boards |
| Absolute path | `/path/to/configs/app` | Out-of-tree boards |
| Directory | `path/to/myboard/config/nsh` | Custom boards |

**Configuration examples:**
```bash
# In-tree board
./tools/configure.sh rv-virt:nsh

# Out-of-tree/custom board
./tools/configure.sh path/to/myboard/config/nsh

# Force distclean
./tools/configure.sh -E rv-virt:nsh

# Auto distclean if config changed
./tools/configure.sh -e rv-virt:nsh
```

| Component | Description | Example |
|-----------|-------------|---------|
| `<board>` | Board directory name | `rv-virt`, `stm32f4discovery` |
| `<config>` | Config directory name | `nsh`, `knsh` |

## 1. Configure and Build

```bash
# Configure
./tools/configure.sh rv-virt:nsh

# Build
make -j8 2>&1 | tail -n 100

# Check outputs
ls -lh nuttx*
```

## 2. Find Available Configs

```bash
# List all
./tools/configure.sh -L

# List specific board
./tools/configure.sh -L rv-virt

# Browse directory
ls nuttx/boards/<arch>/<vendor>/<board>/configs/
```

## 3. Rebuild After Changes

```bash
# Edit source, then rebuild
make -j$(nproc) 2>&1 | tail -n 100
```

## 4. Change Configuration

```bash
# Modify .config (kconfig-tweak or menuconfig)
make olddefconfig
make -j8 2>&1 | tail -n 100
```

## 5. Clean Build

```bash
# Full clean
make distclean
./tools/configure.sh rv-virt:nsh
make -j8 2>&1 | tail -n 100
```

## 6. Switch Configurations

```bash
# Clean previous
make distclean

# Configure new
./tools/configure.sh stm32f4discovery:knsh

# Build
make -j8 2>&1 | tail -n 100
```

## 7. Save Configuration

```bash
# Save minimal defconfig
make savedefconfig
cp defconfig boards/<arch>/<vendor>/<board>/configs/myconfig/defconfig
```

## 8. Build Targets

```bash
make all              # All
make kernel           # Kernel only
make apps             # Apps only
make apps/examples/hello  # Specific app
```

## 9. View Configuration

```bash
grep CONFIG_EXAMPLES_HELLO .config
head -n 100 .config
```

## Troubleshooting

```bash
# More output
make -j8 2>&1 | tail -n 200

# Save full log
make -j8 2>&1 > build.log

# Full reset
make distclean
rm -rf .config
./tools/configure.sh rv-virt:nsh
make -j8 2>&1 | tail -n 100
```

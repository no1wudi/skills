---
name: nuttx-build
description: Configure and build NuttX RTOS for target board and config using CMake or Makefile. Use this when building NuttX firmware, configuring board-specific settings, switching between build systems, or performing incremental builds after code changes.
---

# Building NuttX

This guide provides instructions for building NuttX RTOS using either the traditional Makefile build system or the modern CMake build system.

## Build Output Management

**NuttX builds generate extensive output (1000+ lines)**. Throughout this guide, build commands use `tail -n 100` to limit output to the last 100 lines. This is a recommended starting point that balances:

- Seeing enough context to identify errors
- Avoiding overwhelming output

**Adjust the tail value based on your needs**:
- `tail -n 50` - Minimal output, good for clean builds
- `tail -n 100` - Balanced (recommended default)
- `tail -n 200` - More context for debugging
- `tail -n 1000` - Comprehensive for troubleshooting

To see full output, simply remove the `| tail -n N` portion.

## Build System Selection

NuttX supports two build systems:

- **Makefile**: Traditional build system, well-tested, works with all boards
- **CMake**: Modern build system with Ninja backend, faster builds, better dependency tracking

Choose based on your needs:
- Use Makefile for maximum compatibility and boards with custom build systems
- Use CMake for better performance and modern development workflows

## Basic Configuration

### Configuration Syntax

Both build systems use the `<board-name>:<config-name>` pattern:

```
<board-name>:<config-name>
```

Where:
- `<board-name>` is the board directory name (e.g., `rv-virt`, `stm32f4discovery`)
- `<config-name>` is the configuration directory name (e.g., `nsh`, `knsh`)

**Note**: The minimal configuration for most boards is named `nsh`.

**Important**: Some board families (e.g., ESP32S3) use their own build system and may only work with Makefile. Use Makefile for these boards.

### Finding Available Configurations

#### Using configure.sh (Makefile)

```bash
cd path/to/nuttx

# List all available configurations
./tools/configure.sh -L

# List configurations for a specific board (partial match)
./tools/configure.sh -L rv-virt
```

#### Using Directory Listing

```bash
# List available vendors for an architecture
ls nuttx/boards/<arch>/

# List available boards for a vendor
ls nuttx/boards/<arch>/<vendor>/

# List available configurations for a specific board
ls nuttx/boards/<arch>/<vendor>/<board>/configs/
```

Example for RISC-V QEMU:
```bash
ls nuttx/boards/risc-v/qemu-rv/rv-virt/configs/
# Output: nsh, knsh, knsh64, netnsh, etc.
```

## Makefile Build System

### Configuration Commands

#### Initial Configuration

```bash
cd path/to/nuttx
./tools/configure.sh rv-virt:nsh
```

Configures the board by copying the default configuration, setting up makefiles, and generating header files.

#### Using Different Configurations

```bash
# NSH configuration on rv-virt board
./tools/configure.sh rv-virt:nsh

# Kernel NSH on rv-virt board
./tools/configure.sh rv-virt:knsh

# STM32F4 Discovery
./tools/configure.sh stm32f4discovery:nsh
```

#### Interactive Configuration

```bash
make menuconfig
```

#### Configure.sh Options

```bash
# List available configurations
./tools/configure.sh -L

# Enforce distclean before configuration
./tools/configure.sh -E rv-virt:nsh

# Auto distclean if configuration changed
./tools/configure.sh -e rv-virt:nsh

# Specify custom apps directory
./tools/configure.sh -a path/to/my-apps rv-virt:nsh

# For out-of-tree custom boards
./tools/configure.sh path/to/mycustomboards/myboardname/config/nsh
```

### Building with Makefile

```bash
cd path/to/nuttx

# Configure (if not already done)
./tools/configure.sh rv-virt:nsh

# Apply any config changes
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO
make olddefconfig

# Build
make -j8 2>&1 | tail -n 100

# Incremental builds (after initial build)
make -j$(nproc) 2>&1 | tail -n 100
```

### Clean and Rebuild (Makefile)

```bash
cd path/to/nuttx

# Full clean (cleans both kernel and apps)
make distclean
./tools/configure.sh rv-virt:nsh
make -j8 2>&1 | tail -n 100

# Clean specific targets
make clean
make 2>&1 | tail -n 100
```

## CMake Build System

### Configuration Commands

#### Initial Configuration

```bash
# Configure and create build directory
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
```

#### Using Different Configurations

```bash
# NSH configuration on rv-virt board
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Kernel NSH on rv-virt board
cmake -GNinja -DBOARD_CONFIG=rv-virt:knsh -B path/to/build path/to/nuttx

# NSH with 64-bit kernel
cmake -GNinja -DBOARD_CONFIG=rv-virt:knsh64 -B path/to/build path/to/nuttx
```

#### Building with CMake

```bash
# Configure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Apply config changes
kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO
cmake -B path/to/build path/to/nuttx

# Build
ninja -C path/to/build -j8 2>&1 | tail -n 100

# Incremental builds
ninja -C path/to/build 2>&1 | tail -n 100
```

### Clean and Rebuild (CMake)

```bash
# Full clean
rm -rf path/to/build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
ninja -C path/to/build 2>&1 | tail -n 100

# Clean and reconfigure
ninja -C path/to/build clean
cmake -B path/to/build path/to/nuttx
```

## Configuration Management (Both Systems)

### Modifying Configuration Options

Use `kconfig-tweak` to enable/disable or set configuration options:

```bash
# Makefile build
kconfig-tweak --file path/to/nuttx/.config --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file path/to/nuttx/.config --disable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file path/to/nuttx/.config --set-str CONFIG_EXAMPLES_HELLO_PROGNAME "myhello"
kconfig-tweak --file path/to/nuttx/.config --set-val CONFIG_EXAMPLES_HELLO_PRIORITY 100

# CMake build
kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file path/to/build/.config --disable CONFIG_EXAMPLES_HELLO
```

### Applying Configuration Changes

```bash
# Makefile
cd path/to/nuttx
make olddefconfig

# CMake
cmake -B path/to/build path/to/nuttx
```

### View Current Configuration

```bash
# Makefile
grep CONFIG_YOUR_OPTION path/to/nuttx/.config

# CMake
grep CONFIG_YOUR_OPTION path/to/build/.config
```

### Saving Configuration

```bash
# Save current configuration as defconfig (Makefile only)
make savedefconfig
# Saved to path/to/nuttx/defconfig
```

## Comparison and Decision Guide

### When to Use Makefile

- Maximum compatibility with all boards
- Boards with custom build systems (ESP32S3, etc.)
- When you need `make menuconfig` for interactive configuration
- Legacy projects using Makefile

### When to Use CMake

- Faster builds with Ninja
- Better dependency tracking
- Multiple build configurations in parallel
- Out-of-tree builds (cleaner workspace)
- Modern development workflows

### Feature Comparison

| Feature | Makefile | CMake |
|---------|----------|-------|
| Out-of-tree builds | Limited | Yes |
| Multiple configs in parallel | No | Yes |
| Interactive config | `make menuconfig` | Requires `make menuconfig` in nuttx |
| Build speed | Standard | Faster (Ninja) |
| Board compatibility | All boards | Most boards |
| Clean workspace | Requires `make distclean` | Delete build dir |

## Common Workflows

### Quick Start - New Configuration (Makefile)

```bash
cd path/to/nuttx
./tools/configure.sh rv-virt:nsh
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO
make olddefconfig
make -j8 2>&1 | tail -n 100
ls -lh path/to/nuttx
```

### Quick Start - New Configuration (CMake)

```bash
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO
cmake -B path/to/build path/to/nuttx
ninja -C path/to/build -j8 2>&1 | tail -n 100
ls -lh path/to/build/nuttx
```

---
name: nuttx-makefile-build
description: Build NuttX RTOS firmware using the traditional Makefile build system. Use this when building for maximum board compatibility, working with custom build systems (like ESP32S3), using interactive menuconfig, or maintaining legacy projects.
---

# Building NuttX with Makefile

This guide provides instructions for building NuttX RTOS firmware using the traditional Makefile build system.

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

## Configuration Syntax

The Makefile build system uses the `<board-name>:<config-name>` pattern:

```
<board-name>:<config-name>
```

Where:
- `<board-name>` is the board directory name (e.g., `rv-virt`, `stm32f4discovery`)
- `<config-name>` is the configuration directory name (e.g., `nsh`, `knsh`)

**Note**: The minimal configuration for most boards is named `nsh`.

## Finding Available Configurations

### Using configure.sh

```bash
cd path/to/nuttx

# List all available configurations
./tools/configure.sh -L

# List configurations for a specific board (partial match)
./tools/configure.sh -L rv-virt
```

### Using Directory Listing

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

## Configuration Commands

### Initial Configuration

```bash
cd path/to/nuttx
./tools/configure.sh rv-virt:nsh
```

Configures the board by copying the default configuration, setting up makefiles, and generating header files.

### Using Different Configurations

```bash
# NSH configuration on rv-virt board
./tools/configure.sh rv-virt:nsh

# Kernel NSH on rv-virt board
./tools/configure.sh rv-virt:knsh

# STM32F4 Discovery
./tools/configure.sh stm32f4discovery:nsh
```

### Interactive Configuration

```bash
make menuconfig
```

This launches an interactive menu-based configuration editor. Use arrow keys to navigate, space to enable/disable options, and follow the on-screen instructions.

### Configure.sh Options

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

## Building with Makefile

### Standard Build

```bash
cd path/to/nuttx

# Configure (if not already done)
./tools/configure.sh rv-virt:nsh

# Apply any config changes (requires nuttx-kconfig skill)
make olddefconfig

# Build
make -j8 2>&1 | tail -n 100
```

### Incremental Builds

After the initial build, you can rebuild faster:

```bash
make -j$(nproc) 2>&1 | tail -n 100
```

### Building Specific Targets

```bash
# Build all
make all

# Build kernel only
make kernel

# Build apps only
make apps

# Build a specific application
make apps/examples/hello
```

## Clean and Rebuild

### Full Clean and Rebuild

```bash
cd path/to/nuttx

# Full clean (cleans both kernel and apps)
make distclean

# Reconfigure
./tools/configure.sh rv-virt:nsh

# Rebuild
make -j8 2>&1 | tail -n 100
```

### Clean Specific Targets

```bash
# Clean built files but keep configuration
make clean

# Continue building after clean
make 2>&1 | tail -n 100
```

## Configuration Management

### Applying Configuration Changes

After using kconfig-tweak to modify `.config` (requires nuttx-kconfig skill):

```bash
cd path/to/nuttx

# Update the build configuration
make olddefconfig

# Rebuild
make -j8 2>&1 | tail -n 100
```

### Viewing Current Configuration

```bash
# View specific option
grep CONFIG_EXAMPLES_HELLO .config

# View multiple related options
grep "CONFIG_I2C" .config

# View first 100 lines of configuration options
head -n 100 .config
```

### Saving Configuration

Save the current configuration as a minimal defconfig:

```bash
cd path/to/nuttx

# Save current configuration as minimal defconfig
make savedefconfig

# The defconfig is saved to nuttx/defconfig
# You can copy it to your board's configs directory
cp defconfig boards/<arch>/<vendor>/<board>/configs/myconfig/defconfig
```

## Build Output Location

When building with Makefile, the output files are placed directly in the nuttx directory:

```bash
# List generated files
ls -lh path/to/nuttx

# Common output files:
# nuttx       - The main ELF binary
# nuttx.hex   - Hex format for flashing
# nuttx.bin   - Raw binary image
# mapfile     - Memory map
```

## Common Workflows

### Quick Start - New Configuration

```bash
cd path/to/nuttx
./tools/configure.sh rv-virt:nsh

# Apply config changes using nuttx-kconfig skill
# kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO
make olddefconfig

# Build
make -j8 2>&1 | tail -n 100

# Check output
ls -lh path/to/nuttx
```

### Development Workflow

```bash
# Make code changes
vim path/to/source/file.c

# Incremental rebuild
make -j$(nproc) 2>&1 | tail -n 100
```

### Configuration Change Workflow

```bash
# Modify configuration
make menuconfig
# or use kconfig-tweak

# Apply changes
make olddefconfig

# Rebuild
make -j$(nproc) 2>&1 | tail -n 100
```

### Switch Between Configurations

```bash
# Clean previous build
make distclean

# Configure for new board/config
./tools/configure.sh stm32f4discovery:knsh

# Build
make -j8 2>&1 | tail -n 100
```

## When to Use Makefile

Use the Makefile build system when:

- **Maximum compatibility** - Works with all boards including those with custom build systems
- **Boards with custom build systems** - ESP32S3, ESP32, and other boards that use their own toolchain integration
- **Interactive configuration** - When you need `make menuconfig` for easy configuration editing
- **Legacy projects** - Existing projects already using Makefile
- **Simple builds** - When you don't need out-of-tree builds or multiple configurations in parallel

## Makefile Features

| Feature | Availability |
|---------|-------------|
| Out-of-tree builds | Limited |
| Multiple configs in parallel | No |
| Interactive config | Yes (`make menuconfig`) |
| Build speed | Standard |
| Board compatibility | All boards |
| Clean workspace | Requires `make distclean` |

## Troubleshooting

### Build Errors

```bash
# View more output
make -j8 2>&1 | tail -n 200

# View full output (saved to log file)
make -j8 2>&1 > build.log

# View last 200 lines of build log
tail -n 200 build.log
```

### Configuration Issues

```bash
# Verify configuration is applied correctly
make olddefconfig

# Check specific options
grep "CONFIG_YOUR_OPTION=y" .config

# Use menuconfig for interactive debugging
make menuconfig
```

### Clean State Issues

```bash
# Force complete clean
make distclean
rm -rf .config

# Start fresh
./tools/configure.sh rv-virt:nsh
make -j8 2>&1 | tail -n 100
```

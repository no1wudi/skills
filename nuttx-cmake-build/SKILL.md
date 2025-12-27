---
name: nuttx-cmake-build
description: Build NuttX RTOS firmware using the modern CMake build system with Ninja backend. Use this when you want faster builds, better dependency tracking, multiple build configurations in parallel, out-of-tree builds, or modern development workflows.
---

# Building NuttX with CMake

This guide provides instructions for building NuttX RTOS firmware using the modern CMake build system with Ninja backend.

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

The CMake build system uses the `-DBOARD_CONFIG=<board-name>:<config-name>` parameter:

```
cmake -DBOARD_CONFIG=<board-name>:<config-name> -B <build-dir> <nuttx-source-dir>
```

Where:
- `<board-name>` is the board directory name (e.g., `rv-virt`, `stm32f4discovery`)
- `<config-name>` is the configuration directory name (e.g., `nsh`, `knsh`)
- `<build-dir>` is the directory where build artifacts will be stored
- `<nuttx-source-dir>` is the path to the NuttX source code

**Note**: The minimal configuration for most boards is named `nsh`.

**Important**: Some board families (e.g., ESP32S3) use their own build system and may not work with CMake. Use Makefile for these boards.

## Finding Available Configurations

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
# Configure and create build directory
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
```

This creates a new build directory and generates Ninja build files for the specified board configuration.

### Using Different Configurations

```bash
# NSH configuration on rv-virt board
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Kernel NSH on rv-virt board
cmake -GNinja -DBOARD_CONFIG=rv-virt:knsh -B path/to/build path/to/nuttx

# NSH with 64-bit kernel
cmake -GNinja -DBOARD_CONFIG=rv-virt:knsh64 -B path/to/build path/to/nuttx

# STM32F4 Discovery
cmake -GNinja -DBOARD_CONFIG=stm32f4discovery:nsh -B path/to/build path/to/nuttx
```

### Multiple Build Configurations

One of the key advantages of CMake is the ability to maintain multiple build configurations in parallel:

```bash
# Debug configuration
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-debug path/to/nuttx

# Release configuration
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-release path/to/nuttx

# Different board configurations
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-rv-virt path/to/nuttx
cmake -GNinja -DBOARD_CONFIG=stm32f4discovery:nsh -B build-stm32 path/to/nuttx
```

### CMake Configuration Options

```bash
# Specify generator (Ninja is recommended)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx

# Enable verbose output
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx --verbose

# Specify toolchain file (for cross-compilation)
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build path/to/nuttx -DCMAKE_TOOLCHAIN_FILE=path/to/toolchain.cmake
```

## Building with CMake

### Standard Build

```bash
# Configure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Apply any config changes (requires nuttx-kconfig skill)
cmake -B path/to/build path/to/nuttx

# Build
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### Incremental Builds

After the initial build, you can rebuild faster:

```bash
ninja -C path/to/build 2>&1 | tail -n 100
```

### Building Specific Targets

```bash
# Build all
ninja -C path/to/build all

# Build kernel only
ninja -C path/to/build nuttx

# Build apps only
ninja -C path/to/build apps

# Build a specific application
ninja -C path/to/build hello
```

### Verbose Build Output

```bash
# Show detailed build commands
ninja -C path/to/build -v 2>&1 | tail -n 100
```

## Clean and Rebuild

### Full Clean and Rebuild

```bash
# Full clean - delete build directory
rm -rf path/to/build

# Reconfigure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### Clean Specific Targets

```bash
# Clean built files but keep configuration
ninja -C path/to/build clean

# Rebuild after clean
ninja -C path/to/build 2>&1 | tail -n 100
```

### Clean and Reconfigure

```bash
# Clean
ninja -C path/to/build clean

# Reconfigure
cmake -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

## Configuration Management

### Applying Configuration Changes

After using kconfig-tweak to modify `.config` (requires nuttx-kconfig skill):

```bash
# Apply config changes to build system
cmake -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### Viewing Current Configuration

```bash
# View specific option
grep CONFIG_EXAMPLES_HELLO path/to/build/.config

# View multiple related options
grep "CONFIG_I2C" path/to/build/.config

# View first 100 lines of configuration options
head -n 100 path/to/build/.config
```

### Saving Configuration

CMake builds don't have a direct `savedefconfig` equivalent. However, you can copy the .config file:

```bash
# Copy current configuration
cp path/to/build/.config my-custom-defconfig

# You can edit and use this for future builds
```

## Build Output Location

When building with CMake, all output files are placed in the build directory:

```bash
# List generated files
ls -lh path/to/build

# The main nuttx binary is typically in:
ls -lh path/to/build/nuttx

# Common output files:
# nuttx       - The main ELF binary
# nuttx.hex   - Hex format for flashing
# nuttx.bin   - Raw binary image
```

## Common Workflows

### Quick Start - New Configuration

```bash
# Configure
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx

# Apply config changes using nuttx-kconfig skill
# kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO
cmake -B path/to/build path/to/nuttx

# Build
ninja -C path/to/build -j8 2>&1 | tail -n 100

# Check output
ls -lh path/to/build/nuttx
```

### Development Workflow

```bash
# Make code changes
vim path/to/source/file.c

# Incremental rebuild
ninja -C path/to/build 2>&1 | tail -n 100
```

### Configuration Change Workflow

```bash
# Modify configuration (requires nuttx-kconfig skill)
# kconfig-tweak --file path/to/build/.config --enable CONFIG_NEW_FEATURE

# Apply changes
cmake -B path/to/build path/to/nuttx

# Rebuild
ninja -C path/to/build -j$(nproc) 2>&1 | tail -n 100
```

### Multiple Configurations in Parallel

```bash
# Build two different boards simultaneously
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B build-rv-virt path/to/nuttx
cmake -GNinja -DBOARD_CONFIG=stm32f4discovery:nsh -B build-stm32 path/to/nuttx

# Build both in parallel
ninja -C build-rv-virt -j4 &
ninja -C build-stm32 -j4 &
wait
```

### Out-of-Tree Builds

Keep your source directory clean by building in separate directories:

```bash
# Debug build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B ../builds/nuttx-debug path/to/nuttx
ninja -C ../builds/nuttx-debug

# Release build
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B ../builds/nuttx-release path/to/nuttx
ninja -C ../builds/nuttx-release
```

## When to Use CMake

Use the CMake build system when:

- **Faster builds** - Ninja backend provides faster compilation times
- **Better dependency tracking** - More accurate rebuild detection
- **Multiple build configurations** - Maintain debug/release or multiple board configs simultaneously
- **Out-of-tree builds** - Keep your source directory clean
- **Modern development workflows** - Better integration with IDEs and modern tooling
- **Incremental configuration changes** - Faster reconfiguration after config changes

## CMake Features

| Feature | Availability |
|---------|-------------|
| Out-of-tree builds | Yes |
| Multiple configs in parallel | Yes |
| Interactive config | Requires `make menuconfig` in nuttx source |
| Build speed | Faster (Ninja) |
| Board compatibility | Most boards (not ESP32S3, etc.) |
| Clean workspace | Delete build dir |

## CMake Advantages Over Makefile

1. **Speed**: Ninja builds are typically faster than GNU Make
2. **Parallelism**: Better parallel job scheduling
3. **Dependency tracking**: More accurate detection of what needs rebuilding
4. **Out-of-tree**: Clean separation of source and build artifacts
5. **Multiple configs**: Easy to maintain several build configurations
6. **IDE integration**: Better support from modern IDEs and editors

## Troubleshooting

### Build Errors

```bash
# View more output
ninja -C path/to/build -j8 2>&1 | tail -n 200

# View full output (saved to log file)
ninja -C path/to/build -j8 2>&1 > build.log

# View last 200 lines of build log
tail -n 200 build.log

# Show detailed build commands
ninja -C path/to/build -v 2>&1 | tail -n 100
```

### Configuration Issues

```bash
# Verify configuration is applied correctly
cmake -B path/to/build path/to/nuttx

# Check specific options
grep "CONFIG_YOUR_OPTION=y" path/to/build/.config

# Regenerate build files
rm -rf path/to/build/CMakeCache.txt
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
```

### Clean State Issues

```bash
# Force complete clean
rm -rf path/to/build

# Start fresh
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

### CMake Cache Problems

```bash
# Clear CMake cache
rm -rf path/to/build/CMakeCache.txt

# Regenerate configuration
cmake -B path/to/build path/to/nuttx
```

## Integration with Other Tools

### Using with ccache

```bash
# Enable ccache for faster rebuilds
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
ninja -C path/to/build
```

### Generating Compile Commands

```bash
# Generate compile_commands.json for IDE integration
cmake -GNinja -DBOARD_CONFIG=rv-virt:nsh -B path/to/build path/to/nuttx -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
ninja -C path/to/build
```

This generates `path/to/build/compile_commands.json` which can be used by language servers, linters, and other tools.

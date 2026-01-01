---
name: nuttx-config-management
description: Modifies NuttX kernel configuration options programmatically using kconfig-tweak tool. Enables or disables features without menuconfig and applies configuration changes via command-line. Use when modifying kernel configuration options programmatically or applying configuration changes during development.
---

# Managing NuttX Configuration with kconfig-tweak

This guide explains how to use the `kconfig-tweak` tool to modify NuttX kernel configuration options programmatically from the command line.

## What is kconfig-tweak?

`kconfig-tweak` is a command-line utility that allows you to modify Kconfig configuration files (`.config`) without using interactive menus. It's particularly useful for:

- Scripting configuration changes
- Applying known patches to configuration
- Quick toggling of specific options
- Batch modifications

## kconfig-tweak Basics

### Syntax

```bash
kconfig-tweak --file <path-to-.config> <operation> <option-name> [value]
```

### Common Operations

| Operation | Description | Example |
|-----------|-------------|---------|
| `--enable` | Enable a boolean option | `--enable CONFIG_EXAMPLES_HELLO` |
| `--disable` | Disable a boolean option | `--disable CONFIG_EXAMPLES_HELLO` |
| `--set-str` | Set a string option | `--set-str CONFIG_EXAMPLES_HELLO_PROGNAME "myhello"` |
| `--set-val` | Set an integer/hex option | `--set-val CONFIG_EXAMPLES_HELLO_PRIORITY 100` |
| `--module` | Set option as module | `--module CONFIG_FOO` |

## Usage by Build System

### Makefile Build System

When using the traditional Makefile build system, the configuration file is located at `nuttx/.config`.

```bash
cd path/to/nuttx

# Enable an option
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO

# Disable an option
kconfig-tweak --file .config --disable CONFIG_EXAMPLES_HELLO

# Set string value
kconfig-tweak --file .config --set-str CONFIG_SYSTEM_NUTTX_NAME "MyNuttX"

# Set integer value
kconfig-tweak --file .config --set-val CONFIG_IDLETHREAD_STACKSIZE 2048

# Apply changes to the build system
make olddefconfig
```

### CMake Build System

When using CMake, the configuration file is located in your build directory at `path/to/build/.config`.

```bash
# Enable an option
kconfig-tweak --file path/to/build/.config --enable CONFIG_EXAMPLES_HELLO

# Disable an option
kconfig-tweak --file path/to/build/.config --disable CONFIG_EXAMPLES_HELLO

# Set string value
kconfig-tweak --file path/to/build/.config --set-str CONFIG_SYSTEM_NUTTX_NAME "MyNuttX"

# Apply changes to the build system
cmake -B path/to/build path/to/nuttx
```

## Common Configuration Scenarios

### Enabling Examples

```bash
# Enable the hello world example
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO

# Enable multiple examples
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_POLL
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_TIMER
```

### Modifying Thread Settings

```bash
# Set stack size for idle thread
kconfig-tweak --file .config --set-val CONFIG_IDLETHREAD_STACKSIZE 2048

# Set thread stack default
kconfig-tweak --file .config --set-val CONFIG_THREAD_DEFAULT_STACKSIZE 1024
```

### System Configuration

```bash
# Set system hostname
kconfig-tweak --file .config --set-str CONFIG_SYSTEM_HOSTNAME "mynuttx"

# Set system name
kconfig-tweak --file .config --set-str CONFIG_SYSTEM_NUTTX_NAME "CustomNuttX"

# Enable task names
kconfig-tweak --file .config --enable CONFIG_TASK_NAME_SIZE 32
```

### Driver Configuration

```bash
# Enable I2C driver
kconfig-tweak --file .config --enable CONFIG_I2C

# Enable SPI driver
kconfig-tweak --file .config --enable CONFIG_SPI

# Enable UART driver
kconfig-tweak --file .config --enable CONFIG_SERIAL_TERMIOS
```

## Applying Configuration Changes

After modifying the `.config` file with `kconfig-tweak`, you must update the build system to apply the changes:

### Makefile System

```bash
# Update the build configuration
make olddefconfig

# Optional: Verify the changes took effect
grep CONFIG_EXAMPLES_HELLO .config

# Then build
make -j8 2>&1 | tail -n 100
```

### CMake System

```bash
# Update the build configuration
cmake -B path/to/build path/to/nuttx

# Optional: Verify the changes took effect
grep CONFIG_EXAMPLES_HELLO path/to/build/.config

# Then build
ninja -C path/to/build -j8 2>&1 | tail -n 100
```

## Viewing Current Configuration

### Check Specific Options

```bash
# Makefile system
grep CONFIG_EXAMPLES_HELLO .config

# CMake system
grep CONFIG_EXAMPLES_HELLO path/to/build/.config
```

### Check Multiple Related Options

```bash
# Search for all I2C related options
grep "CONFIG_I2C" .config

# Search for all task/thread options
grep "CONFIG_TASK\|CONFIG_THREAD" .config
```

### Check if Option is Set

```bash
# Check if option is enabled (returns 0 if found, 1 if not)
grep -q "CONFIG_EXAMPLES_HELLO=y" .config && echo "Enabled" || echo "Disabled"
```

## Saving Configuration (Makefile Only)

The `make savedefconfig` command creates a minimal defconfig file that contains only the non-default options:

```bash
cd path/to/nuttx

# Save current configuration as minimal defconfig
make savedefconfig

# The defconfig is saved to nuttx/defconfig
# You can copy it to your board's configs directory
cp defconfig boards/<arch>/<vendor>/<board>/configs/myconfig/defconfig
```

## Batch Configuration Scripts

You can create shell scripts to apply multiple configuration changes at once:

```bash
#!/bin/bash
# configure_my_board.sh

CONFIG_FILE=".config"

# Enable features
kconfig-tweak --file "$CONFIG_FILE" --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file "$CONFIG_FILE" --enable CONFIG_I2C
kconfig-tweak --file "$CONFIG_FILE" --enable CONFIG_SPI

# Set values
kconfig-tweak --file "$CONFIG_FILE" --set-str CONFIG_SYSTEM_HOSTNAME "myboard"
kconfig-tweak --file "$CONFIG_FILE" --set-val CONFIG_IDLETHREAD_STACKSIZE 2048

# Apply changes
make olddefconfig
```

## Workflow Integration

### Typical Development Workflow

```bash
# 1. Configure board
./tools/configure.sh rv-virt:nsh

# 2. Apply custom configuration tweaks
kconfig-tweak --file .config --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file .config --set-str CONFIG_SYSTEM_HOSTNAME "devboard"

# 3. Update configuration
make olddefconfig

# 4. Build
make -j8 2>&1 | tail -n 100

# 5. Save configuration for later
make savedefconfig
```

### Quick Configuration Test

```bash
# Configure
./tools/configure.sh rv-virt:nsh

# Add your option
kconfig-tweak --file .config --enable CONFIG_YOUR_FEATURE

# Verify
make olddefconfig
grep "CONFIG_YOUR_FEATURE=y" .config

# Build
make -j8 2>&1 | tail -n 100
```

## Troubleshooting

### Option Not Found

If `kconfig-tweak` can't find an option:

```bash
# Search for similar options
grep -i "feature" .config

# Check if it's available in the current board config
grep -r "CONFIG_YOUR_FEATURE" boards/
```

### Changes Not Applied

If changes don't seem to take effect:

1. Make sure you ran `make olddefconfig` or `cmake -B ...` after modifying `.config`
2. Check that the option isn't being overridden by other configuration files
3. Verify the option is actually present in the kernel configuration tree

### Configuration Conflicts

If you get warnings about conflicting options:

```bash
# Review the full configuration
make menuconfig

# Look for dependencies that might be missing
grep "CONFIG_YOUR_FEATURE" .config
grep "CONFIG_DEPENDENT_OPTION" .config
```

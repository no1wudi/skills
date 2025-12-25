---
name: nuttx-defconfig-generation
description: Generate normalized defconfig files for NuttX board configurations using savedefconfig to create clean, minimal configuration files.
---

# NuttX Defconfig Generation Guide

This guide covers how to generate normalized defconfig files for NuttX board configurations. Using `savedefconfig` ensures clean, minimal configuration files that only contain settings that differ from defaults.

## Out-of-Tree Board Support

NuttX supports out-of-tree board configurations using `tools/configure.sh` with a path-based syntax:

```bash
# For out-of-tree boards, use a path to the configuration directory
cd nuttx
./tools/configure.sh ../path/to/your-boards/<board-name>/configs/<config-name>

# Then build
make
```

### Out-of-Tree Board Examples

#### Relative Paths from Nuttx Directory

**Sibling directory (next to nuttx)**:
```bash
cd nuttx
./tools/configure.sh ../my-boards/stm32f7/my-board/configs/nsh
```

**Parent directory levels**:
```bash
cd nuttx
./tools/configure.sh ../../external-boards/stm32f7/my-board/configs/nsh
```

**Current directory structure**:
```bash
project/
├── nuttx/
├── nuttx-apps/
└── my-boards/
    └── stm32f7/
        └── my-board/
            └── configs/
                └── nsh/
                    └── defconfig

# From nuttx directory:
./tools/configure.sh ../my-boards/stm32f7/my-board/configs/nsh
```

#### Absolute Paths

**Full absolute path**:
```bash
cd nuttx
./tools/configure.sh /home/user/projects/nuttx/my-boards/stm32f7/my-board/configs/nsh
```

**Home directory expansion**:
```bash
cd nuttx
./tools/configure.sh ~/nuttx-projects/my-boards/esp32/devkit/configs/nsh
```

#### Common Project Structures

**Separate boards repository**:
```bash
project/
├── nuttx/                    # NuttX core
├── nuttx-apps/               # NuttX apps
└── nuttx-boards/             # Separate boards repo
    └── rv-virt/
        └── custom-nsh/
            └── configs/
                └── defconfig

# From nuttx directory:
./tools/configure.sh ../nuttx-boards/rv-virt/custom-nsh/configs/defconfig
```

**Embedded boards in application repo**:
```bash
application/
├── firmware/
│   └── nuttx/                # NuttX as submodule
└── boards/
    └── custom-board/
        └── configs/
            └── app/
                └── defconfig

# From nuttx directory (3 levels up):
./tools/configure.sh ../../../boards/custom-board/configs/app
```

#### Using Different Board Configurations

**rv-virt with different configs**:
```bash
cd nuttx
./tools/configure.sh ../my-boards/rv-virt/configs/nsh64        # 64-bit NSH
./tools/configure.sh ../my-boards/rv-virt/configs/netnsh64    # Networking NSH
./tools/configure.sh ../my-boards/rv-virt/configs/smp64       # SMP enabled
```

**Different architectures**:
```bash
cd nuttx
./tools/configure.sh ../my-boards/esp32/devkit/configs/nsh          # ESP32
./tools/configure.sh ../my-boards/stm32f7/disco/configs/nsh        # STM32F7
./tools/configure.sh ../my-boards/lpc43xx/mbed/configs/nsh         # LPC43xx
```

#### Creating New Configurations

**Start from existing config and save as new**:
```bash
cd nuttx
# Load existing configuration from out-of-tree board
./tools/configure.sh ../my-boards/my-board/configs/nsh

# Customize it
make menuconfig

# Save as new minimal defconfig
make savedefconfig

# Copy to your custom location
cp nuttx/defconfig ../my-boards/my-custom-configs/my-nsh/defconfig
```

**Version-controlled custom configs**:
```bash
cd nuttx
./tools/configure.sh ../company-boards/nxp/imxrt/configs/custom-demo

# Make changes
make menuconfig

# Save to version-controlled boards repo
make savedefconfig
cp nuttx/defconfig ../company-boards/nxp/imxrt/configs/custom-demo-v2/defconfig
```

#### Path Patterns Summary

| Location | Example Path |
|----------|--------------|
| Sibling boards dir | `../my-boards/<board>/configs/<config>` |
| Parent level | `../../external-boards/<board>/configs/<config>` |
| Two parents up | `../../../shared-boards/<board>/configs/<config>` |
| Absolute home | `~/projects/boards/<board>/configs/<config>` |
| Absolute path | `/opt/nuttx/boards/<board>/configs/<config>` |

#### Quick Reference

```bash
# Basic syntax
./tools/configure.sh <path-to-config-directory>

# Must point to directory containing defconfig file
# Path is relative to nuttx directory (where you run the command)
# Absolute paths also supported
# No spaces in paths (or escape them)

# Examples:
./tools/configure.sh ../my-boards/rv-virt/configs/nsh
./tools/configure.sh /home/user/boards/stm32f7/disco/configs/nsh
./tools/configure.sh ../../shared-boards/esp32/devkit/configs/nsh
```

### Out-of-Tree Board Directory Structure

Out-of-tree boards follow the same structure as in-tree boards:
```
<board-directory>/
├── configs/
│   └── <config-name>/
│       └── defconfig          # Board configuration file
└── scripts/
    └── Make.defs              # Build definitions (can delegate to in-tree board)
```

### Delegating to In-Tree Boards

Out-of-tree boards can delegate build logic to existing in-tree boards by including their Make.defs:

```make
# In <board-directory>/scripts/Make.defs
include $(TOPDIR)/boards/risc-v/qemu-rv/rv-virt/scripts/Make.defs
```

This allows out-of-tree configurations to use existing board support while maintaining custom configurations.

## Overview

The NuttX build system provides `make savedefconfig` command to generate minimal configuration files. This command creates a defconfig that contains only the options you've explicitly changed, making configuration files:

- **Smaller and cleaner** - No unnecessary default values
- **Easier to maintain** - Only track meaningful changes
- **Portable** - Work across different NuttX versions
- **Conflict-free** - Avoid issues from upstream default changes

## Why Use savedefconfig

When you modify a configuration using `menuconfig`, NuttX tracks all selected options in `.config`. However, this file contains both your changes AND all default values. The `savedefconfig` command extracts only your modified settings into a minimal defconfig file.

Benefits:
- Reduces file size significantly (often 10x smaller)
- Makes configuration changes easy to review
- Prevents carrying over unnecessary settings
- Ensures compatibility with future NuttX versions

## Step-by-Step Generation Guide

### Method 1: Generate Configuration from Scratch

```bash
# Step 1: Start with a minimal configuration from an existing in-tree board
cd nuttx
./tools/configure.sh risc-v/qemu-rv:rv-virt/nsh

# Or configure directly using your out-of-tree board:
# ./tools/configure.sh ../my-boards/<your-board>/configs/<config-name>

# Step 2: Configure for your custom board
make menuconfig

# Step 3: Set board-specific options:
#   - CONFIG_ARCH="<arch>" (e.g., "arm", "risc-v", "xtensa")
#   - CONFIG_ARCH_BOARD_CUSTOM=y
#   - CONFIG_ARCH_BOARD_CUSTOM_DIR="../boards/<your-board>"
#   - CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y
#   - CONFIG_ARCH_CHIP="<chip-family>"
#   - CONFIG_ARCH_CHIP_<CHIP>=y

# Step 4: Save the minimal defconfig
make savedefconfig

# Step 5: Copy to your out-of-tree board configuration
cp nuttx/defconfig ../boards/<your-board>/configs/<config-name>/defconfig
```

### Method 2: Generate from Existing Out-of-Tree Configuration

If you already have an out-of-tree board structure:

```bash
# Step 1: Configure using the out-of-tree board
cd nuttx
./tools/configure.sh ../path/to/your-board/configs/<config-name>

# Step 2: Modify as needed
make menuconfig

# Step 3: Save the minimal defconfig
make savedefconfig

# Step 4: Copy back to out-of-tree location (if needed)
cp nuttx/defconfig ../path/to/your-board/configs/<config-name>/defconfig
```

## Out-of-Tree Configuration Directory Structure

```
boards/
├── <board-name>/
│   ├── configs/
│   │   └── <config-name>/
│   │       └── defconfig          # Generated minimal config
│   └── scripts/
│       └── Make.defs              # Build definitions
```

## Best Practices

### 1. Always Use savedefconfig

Never manually edit defconfig files. Always:
1. Start with an existing defconfig or minimal config
2. Use `menuconfig` to make changes
3. Use `savedefconfig` to generate the final defconfig

This ensures your configuration is valid and minimal.

### 2. Version Control

Track defconfig files in version control:
```bash
git add boards/<board-name>/configs/<config-name>/defconfig
git commit -m "Add <config-name> configuration for <board-name>"
```

### 3. Document Configuration Changes

When updating configurations, document what changed:
```bash
# Before updating, save a reference
cp ../boards/<board-name>/configs/<config-name>/defconfig /tmp/old.defconfig

# After generating new defconfig, show differences
diff -u /tmp/old.defconfig ../boards/<board-name>/configs/<config-name>/defconfig
```

### 4. Test After Changes

Always rebuild and test after updating configurations:
```bash
cd nuttx
make -j$(nproc)
```

### 5. Use Descriptive Config Names

Name configurations descriptively:
- `nsh` - Basic NSH shell
- `nsh-usb` - NSH with USB console
- `netnsh` - NSH with networking
- `app` - Custom application configuration

### 6. Keep Configurations Minimal

Only include settings that differ from defaults:
- Architecture and board identification
- Chip-specific options
- Required feature enablement
- Peripheral configurations

Avoid:
- Debug symbols in production configs
- Unused feature enablement
- Architecture-specific defaults

## Troubleshooting

### Configuration Not Applied

**Problem**: Changes made in menuconfig don't appear in the build.

**Solution**:
1. Verify you're in the nuttx directory
2. Ensure `.config` was saved before running `savedefconfig`
3. Check that the correct defconfig is being used:
   ```bash
   cd nuttx
   cat .config | grep CONFIG_ARCH_BOARD
   ```

### Missing Board Options

**Problem**: Board-specific options don't appear in menuconfig.

**Solution**:
1. Verify `CONFIG_ARCH_BOARD_CUSTOM=y` is set
2. Check `CONFIG_ARCH_BOARD_CUSTOM_DIR` points to correct path
3. Ensure board's `Kconfig` file exists if custom options are defined

### Build Failures After Config Update

**Problem**: Build fails after updating defconfig.

**Solution**:
1. Check for missing required options:
   ```bash
   cd nuttx
   make olddefconfig
   ```
2. Verify architecture and chip settings match your hardware
3. Ensure all required drivers are enabled

### Configuration Too Large

**Problem**: Defconfig file is unexpectedly large.

**Solution**:
1. Run `make savedefconfig` again to ensure minimal output
2. Check for unintended debug options
3. Verify you're not including default values

### Path Issues with Custom Boards

**Problem**: Custom board not found during configuration.

**Solution**:
1. Use relative paths with `CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y`
2. Verify path is correct relative to nuttx directory:
   ```
   CONFIG_ARCH_BOARD_CUSTOM_DIR="../boards/my-custom-board"
   ```
3. Ensure boards directory is accessible from nuttx build

### Out-of-Tree Board Configuration Issues

**Problem**: Cannot configure using out-of-tree board with `tools/configure.sh`.

**Solution**:

1. **Verify** path syntax:
   ```bash
    # Correct: Path to config directory containing defconfig
    ./tools/configure.sh ../my-boards/my-board/configs/nsh

   # Incorrect: Path to defconfig file itself
   ./tools/configure.sh ../my-boards/rv-virt/configs/nsh/defconfig  # WRONG!
   ```

2. **Validate** path is correct:
   ```bash
   # Check from nuttx directory
   ls ../path/to/your-board/configs/<config-name>/
   # Should show: defconfig

   # Verify full path
   realpath ../path/to/your-board/configs/<config-name>/defconfig
   ```

3. **Test path** from nuttx directory:
   ```bash
   cd nuttx
   pwd                        # Should show: /path/to/nuttx

   # Try listing the config directory
   ls -la ../boards/rv-virt/configs/nsh/
   # Should show: defconfig

    # Then configure
    ./tools/configure.sh ../my-boards/my-board/configs/nsh
   ```

4. **Common path mistakes**:
   - ❌ Using absolute path when relative is expected
   - ❌ Pointing to defconfig file instead of config directory
   - ❌ Wrong number of `../` prefixes
   - ❌ Spaces in path (escape them: `../../my\ boards/`)
   - ❌ Case sensitivity on some systems

5. **Path debugging**:
   ```bash
   cd nuttx
   # Show current directory
   pwd

   # Show relative path to your config
   realpath --relative-to=. /path/to/your/config
   # OR
   realpath --relative-to=. ../../your/config

   # Test if path exists
   test -d ../path/to/config && echo "Path exists" || echo "Path not found"
   ```

6. **Ensure directory structure is correct**:
   ```
   <board-dir>/
   ├── configs/
   │   └── <config>/
   │       └── defconfig          # ← Must exist
   └── scripts/
       └── Make.defs              # Optional for delegation
   ```

7. **Use absolute path if relative fails**:
   ```bash
   cd nuttx
   # Get absolute path
   realpath ../path/to/your-board

   # Use absolute path
   ./tools/configure.sh /full/path/to/your-board/configs/<config-name>
   ```

## Integration with Existing Boards

### Referencing In-Tree Boards

When creating configurations for existing in-tree boards:

```bash
# Configure using in-tree board (use path syntax for consistency)
cd nuttx
./tools/configure.sh risc-v/qemu-rv:rv-virt/nsh

# Modify as needed
make menuconfig

# Generate minimal defconfig
make savedefconfig

# Copy to out-of-tree location (if maintaining custom config)
cp nuttx/defconfig ../my-custom-boards/my-board/configs/app/defconfig
```

### Referencing Out-of-Tree Boards

When working with out-of-tree boards, use path syntax:

```bash
# Configure using out-of-tree board
cd nuttx
./tools/configure.sh ../path/to/your-board/configs/<config-name>

# Modify as needed
make menuconfig

# Generate minimal defconfig
make savedefconfig

# Copy back to out-of-tree location (if needed)
cp nuttx/defconfig ../path/to/your-board/configs/<config-name>/defconfig
```

### Combining with Out-of-Tree Boards

For completely custom boards, combine with the `nuttx-out-of-tree-board-creation` skill:

1. Create board directory structure
2. Add `scripts/Make.defs` referencing existing chip/board
3. Generate and save minimal defconfig
4. Test build and functionality

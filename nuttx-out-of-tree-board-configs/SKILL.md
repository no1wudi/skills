---
name: nuttx-out-of-tree-board-configs
description: Creates custom configurations for existing in-tree boards without modifying upstream NuttX code. Maintains separate product-specific or development configurations in out-of-tree directories. Use when creating custom configurations for existing boards or maintaining separate product-specific configurations.
---

# NuttX Out-of-Tree Board Configurations

## Overview
NuttX supports creating custom configurations for existing in-tree boards without modifying of upstream board code. This allows you to maintain custom configurations separately while leveraging all of existing board support code.

## Directory Structure Pattern

### Out-of-Tree Board Structure
```
boards/<board-name>/
├── configs/<config-name>/
│   └── defconfig                    # Board configuration
├── scripts/
│   └── Make.defs                    # Build definitions
└── <board-name>.resc                # Renode simulation file (optional)
```

### In-Tree Board Structure (for reference)
```
nuttx/boards/arm/<arch>/<board-name>/
├── configs/                         # Multiple config options
│   ├── <config1>/defconfig
│   ├── <config2>/defconfig
│   └── ...
├── include/
│   └── board.h                      # Board-specific headers
├── src/                             # Board drivers & implementation
├── scripts/                         # Build scripts & linker files
├── kernel/                          # Kernel-specific files
├── CMakeLists.txt                   # CMake build file
└── Kconfig                          # Kconfig options
```

## Key Implementation Steps

### 1. Create Minimal Out-of-Tree Directory
```bash
mkdir -p boards/<board-name>/configs/<your-config>
mkdir -p boards/<board-name>/scripts
```

### 2. Configuration File (defconfig)
Copy an existing configuration from in-tree board or create a new one. The configuration should include:
- Board identification (`CONFIG_ARCH_BOARD`, `CONFIG_ARCH_BOARD_STM32F746G_DISCO`)
- Chip-specific settings (`CONFIG_ARCH_CHIP_STM32F746NG`)
- System configuration (NSH, memory regions, etc.)

### 3. Build System Integration
Create `scripts/Make.defs` that includes in-tree board's build definitions:

```makefile
include $(TOPDIR)/boards/arm/<arch>/<board-name>/scripts/Make.defs
```

This delegates all build logic to existing in-tree board while allowing custom configurations.

### 4. Optional Simulation Support
Add a `.resc` file for Renode simulation integration if needed.

## Example: STM32F746 Discovery

### Out-of-Tree Configuration
- **Location**: `boards/stm32f746g-disco/`
- **Config**: `configs/app/defconfig`
- **Build**: `scripts/Make.defs` (includes in-tree version)
- **Simulation**: `stm32f746g-disco.resc`

### Configuration Details
The out-of-tree `defconfig` includes essential settings:
- Architecture: ARM Cortex-M7
- Board: STM32F746G Discovery
- Chip: STM32F746NG
- System: NSH shell with C++ support
- Memory: 240KB RAM configuration
- Debug: Symbols enabled
- Peripherals: USART1 console, SPI support

## Benefits

1. **Minimal Overhead**: Only configuration files needed
2. **Reuse Existing Code**: Leverages all board drivers and support
3. **Clean Separation**: Custom configs separate from upstream
4. **Easy Updates**: Board updates don't affect custom configurations
5. **Build Integration**: Works with existing NuttX build system

## Build Usage

```bash
# Build with custom configuration
make -C nuttx boards/<board-name>/<config-name>
```

## Configuration Management

### Generating New Configurations
1. Copy existing defconfig
2. Modify using `make menuconfig`
3. Save with `make savedefconfig`

### Common Configuration Options
- Enable/disable features via Kconfig
- Memory region configuration
- Peripheral driver selection
- Debug and optimization settings
- Application-specific features

## Integration with Existing Boards

The out-of-tree approach works by:
1. **Configuration Override**: Custom defconfig overrides base settings
2. **Build Delegation**: Make.defs includes existing board build logic
3. **Driver Reuse**: All board drivers from in-tree implementation
4. **Linker Script**: Uses existing memory layout and startup code

This pattern is ideal for:
- Custom application configurations
- Development variations
- Product-specific builds
- Testing different feature combinations
- Maintaining stable upstream compatibility

## Best Practices

1. **Document Configuration**: Include comments explaining custom settings
2. **Version Control**: Track configuration changes separately
3. **Testing**: Verify configurations work across different toolchains
4. **Updates**: Monitor upstream board changes for compatibility
5. **Naming**: Use descriptive config names for clarity

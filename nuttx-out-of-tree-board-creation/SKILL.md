---
name: nuttx-out-of-tree-board-creation
description: Use when adding support for completely new hardware boards that don't exist in upstream NuttX, or when creating custom board BSP packages that leverage existing chip-level drivers while maintaining board-specific code separately in out-of-tree directories.
---

# NuttX Out-of-Tree Board Creation Guide

This guide covers how to create custom NuttX boards without modifying of upstream codebase. It provides architecture-independent patterns that work across all NuttX-supported architectures (ARM, RISC-V, xtensa, etc.).

## Board Creation Patterns

### Pattern 1: Out-of-Tree Board Creation
Create a completely new board directory that leverages existing chip-level drivers without duplicating code.

### Pattern 2: Out-of-Tree Configurations
Create custom configurations for existing boards without modifying upstream code.

## Directory Structure

### Out-of-Tree Board Structure
```
boards/
├── my-custom-board/
│   ├── configs/                 # Board-specific configurations
│   │   └── myconfig/
│   │       └── defconfig
│   ├── scripts/                 # Build scripts
│   │   └── Make.defs
│   ├── src/                     # Board-specific source (minimal)
│   │   ├── Make.defs
│   │   └── myboard_boot.c       # Optional board initialization
│   └── Kconfig                  # Optional board configuration options
```

### Out-of-Tree Configuration Structure
```
boards/
├── my-config/
│   ├── configs/
│   │   └── myconfig/
│   │       └── defconfig
│   └── scripts/
│       └── Make.defs
```

## Implementation Guide

### Step 1: Create Board Directory

```bash
# For out-of-tree board
mkdir -p boards/my-custom-board/configs/myconfig
mkdir -p boards/my-custom-board/scripts
mkdir -p boards/my-custom-board/src

# For out-of-tree configuration
mkdir -p boards/my-config/configs/myconfig
mkdir -p boards/my-config/scripts
```

### Step 2: Create Configuration File (defconfig)

#### Architecture-Independent Configuration Template
```bash
# Copy reference configuration from similar board
cp nuttx/boards/<arch>/<chip-family>/<reference-board>/configs/<config>/defconfig \
   boards/my-custom-board/configs/myconfig/defconfig

# Edit the configuration - replace with your specific values
CONFIG_ARCH="<your-architecture>"           # e.g., "arm", "risc-v", "xtensa"
CONFIG_ARCH_BOARD="my-custom-board"         # Your board name
CONFIG_ARCH_BOARD_CUSTOM=y                  # Enable custom board
CONFIG_ARCH_BOARD_CUSTOM_DIR="../boards/my-custom-board"
CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y
CONFIG_ARCH_CHIP="<your-chip>"              # Your chip family, e.g., "stm32f7", "esp32s3"
CONFIG_ARCH_CHIP_<YOUR-CHIP>=y              # Enable your specific chip
CONFIG_ARCH_CHIP_<YOUR-CHIP>CUSTOM=y        # Custom chip variant if needed
```

#### ARM Example (STM32)
```bash
cp nuttx/boards/arm/stm32f7/stm32f746g-disco/configs/nsh/defconfig \
   boards/my-stm32-board/configs/myconfig/defconfig

# Edit for your ARM board
CONFIG_ARCH="arm"
CONFIG_ARCH_BOARD="my-stm32-board"
CONFIG_ARCH_BOARD_CUSTOM=y
CONFIG_ARCH_BOARD_CUSTOM_DIR="../boards/my-stm32-board"
CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y
CONFIG_ARCH_CHIP="stm32f7"
CONFIG_ARCH_CHIP_STM32F7=y
CONFIG_ARCH_CHIP_STM32F7CUSTOM=y
```

#### RISC-V Example
```bash
cp nuttx/boards/risc-v/common/cores/configs/nsh/defconfig \
   boards/my-riscv-board/configs/myconfig/defconfig

# Edit for your RISC-V board
CONFIG_ARCH="risc-v"
CONFIG_ARCH_BOARD="my-riscv-board"
CONFIG_ARCH_BOARD_CUSTOM=y
CONFIG_ARCH_BOARD_CUSTOM_DIR="../boards/my-riscv-board"
CONFIG_ARCH_BOARD_CUSTOM_DIR_RELPATH=y
CONFIG_ARCH_CHIP="<your-riscv-chip>"
CONFIG_ARCH_CHIP_<YOUR-CHIP>=y
```

### Step 3: Create Build Scripts

#### scripts/Make.defs (Architecture-Independent)
```makefile
###########################################################################
# boards/my-custom-board/scripts/Make.defs
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.  The
# ASF licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
###########################################################################

# Reference existing similar board's build system
include $(TOPDIR)/boards/<arch>/<chip-family>/<reference-board>/scripts/Make.defs
```

#### scripts/Make.defs (Out-of-Tree Configuration)
```makefile
###########################################################################
# boards/my-config/scripts/Make.defs
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.  The
# ASF licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
###########################################################################

# Point to the existing board being configured
include $(TOPDIR)/boards/<arch>/<chip-family>/<reference-board>/scripts/Make.defs
```

### Step 4: Add Board-Specific Code (Optional)

#### src/Make.defs (For custom board with unique initialization)
```makefile
###########################################################################
# boards/my-custom-board/src/Make.defs
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.  The
# ASF licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
###########################################################################

include $(TOPDIR)/Make.defs

# Board-specific source files (keep minimal)
CSRCS = mycustom_boot.c mycustom_bringup.c

# Add conditional compilation based on config options
ifeq ($(CONFIG_BOARDCTL),y)
CSRCS += mycustom_appinit.c
endif

# Architecture-specific conditional compilation
ifeq ($(CONFIG_ARCH_CUSTOM),y)
CSRCS += mycustom_arch_init.c
endif

DEPPATH += --dep-path board
VPATH += :board
CFLAGS += ${INCDIR_PREFIX}$(TOPDIR)$(DELIM)arch$(DELIM)$(CONFIG_ARCH)$(DELIM)src$(DELIM)board$(DELIM)board
```

#### mycustom_boot.c (Generic board initialization template)
```c
/****************************************************************************
 * boards/my-custom-board/src/mycustom_boot.c
 *
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.  The
 * ASF licenses this file to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance with the
 * License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *
 *****************************************************************************/

/****************************************************************************
 * Included Files
 *****************************************************************************/

#include <nuttx/config.h>

#include <debug.h>

#include <nuttx/board.h>
#include <nuttx/mm/mm.h>

/* Architecture-specific includes */
#ifdef CONFIG_ARCH_ARM
#  include <arch/arm/src/chip.h>
#elif defined(CONFIG_ARCH_RISCV)
#  include <arch/risc-v/src/chip.h>
#elif defined(CONFIG_ARCH_XTENSA)
#  include <arch/xtensa/src/esp32s3/chip.h>
#endif

#include <arch/board/board.h>

/****************************************************************************
 * Pre-processor Definitions
 *****************************************************************************/

/* Board-specific definitions - customize for your hardware */
#ifndef BOARD_CUSTOM_CLOCK_FREQ
#  define BOARD_CUSTOM_CLOCK_FREQ 80000000  /* Default 80MHz */
#endif

#ifndef BOARD_CUSTOM_LED_PIN
#  define BOARD_CUSTOM_LED_PIN 13          /* Default LED pin */
#endif

/****************************************************************************
 * Public Functions
 *****************************************************************************/

/****************************************************************************
 * Name: board_initialize
 *
 * Description:
 *   All NuttX boards must provide this entry point.
 *   This entry point is called early in the initialization -- after all
 *   memory was configured but before any devices have been initialized.
 *
 *   This function must perform low level board initialization including:
 *     - Configure board-specific peripherals
 *     - Initialize pin configuration
 *     - Set up serial console (if needed)
 *     - Configure board-specific devices
 *     - etc.
 *
 * Input Parameters:
 *   None
 *
 * Returned Value:
 *   None
 *
 *****************************************************************************/

void board_initialize(void)
{
#ifdef CONFIG_DEBUG_FEATURES
  llinfo("Initializing board: %s\n", CONFIG_ARCH_BOARD_NAME);
#endif

  /* Perform architecture-specific board initialization */

#ifdef CONFIG_ARCH_IRQCUSTOM
  /* Configure any custom interrupt handling here */
#endif

#ifdef CONFIG_DEV_GPIO
  /* Configure board-specific GPIO pins */
  board_gpio_config(BOARD_CUSTOM_LED_PIN, false, false, false, 0);
#endif

#ifdef CONFIG_ARCH_CUSTOM_HARDWARE
  /* Initialize any custom hardware specific to your board */
  board_custom_hardware_init();
#endif

#ifdef CONFIG_BOARD_SPECIFIC_INIT
  /* Call architecture-specific board initialization */
  arch_board_init();
#endif
}

/****************************************************************************
 * Name: board_app_initialize
 *
 * Description:
 *   Perform board-specific application initialization.
 *
 *   This function is called once from board_app_init in the NuttX
 *   architecture-specific initialization sequence.
 *
 *   BOARD_APP_INITIALIZE is executed in the context of the work queue
 *   thread and is designed for configuration that requires
 *   interrupts enabled and driver/device initialization to complete.
 *
 * Input Parameters:
 *   None
 *
 * Returned Value:
 *   None
 *
 *****************************************************************************/

#if defined(CONFIG_BOARDCTL)
int board_app_initialize(void)
{
  int ret = OK;

#ifdef CONFIG_DEBUG_FEATURES
  llinfo("Application initialization for board: %s\n", CONFIG_ARCH_BOARD_NAME);
#endif

  /* Perform application-specific board initialization */

#ifdef CONFIG_ARCH_CUSTOM_DRIVERS
  /* Initialize any custom drivers */
  // ret = my_custom_driver_init();
  // if (ret < 0)
  //   {
  //     syslog(LOG_ERR, "ERROR: my_custom_driver_init failed: %d\n", ret);
  //   }
#endif

#ifdef CONFIG_DEV_GPIO
  /* Configure any additional GPIO pins needed by applications */
  board_app_gpio_init();
#endif

  return ret;
}
#endif

#ifdef CONFIG_ARCH_CUSTOM_HARDWARE
/****************************************************************************
 * Name: board_custom_hardware_init
 *
 * Description:
 *   Initialize any custom hardware specific to this board.
 *
 * Input Parameters:
 *   None
 *
 * Returned Value:
 *   None
 *
 *****************************************************************************/

static void board_custom_hardware_init(void)
{
  /* Implement your custom hardware initialization here */

#ifdef CONFIG_ARCH_ARM
  /* ARM-specific initialization */
  // stm32_configgpio(MY_CUSTOM_PIN, STM32GPIO_PULLUP | STM32GPIO_INPUT);

#elif defined(CONFIG_ARCH_RISCV)
  /* RISC-V-specific initialization */
  // riscv_configgpio(MY_CUSTOM_PIN, RISCVGPIO_INPUT);

#elif defined(CONFIG_ARCH_XTENSA)
  /* xtensa-specific initialization */
  // esp32s3_configgpio(MY_CUSTOM_PIN, INPUT);

#endif
}
#endif
```

### Step 5: Add Board Configuration (Optional)

#### Kconfig (Board-specific configuration options)
```kconfig
#
# For a description of the syntax of this configuration file,
# see the file kconfig-language.txt in the NuttX tools repository.
#

config BOARD_MY_CUSTOM_FEATURE
    bool "Enable my custom feature"

if BOARD_MY_CUSTOM_FEATURE

config BOARD_MY_CUSTOM_PIN
    int "My custom pin number"
    default 10

config BOARD_MY_CUSTOM_CLOCK
    int "Custom clock frequency in Hz"
    default 80000000

endif # BOARD_MY_CUSTOM_FEATURE

config BOARD_LED_PIN
    int "LED pin number"
    default 13

config BOARD_LCD_PIN
    int "LCD pin configuration"
    default 4

if LCD_MY_DISPLAY_DRIVER

config BOARD_LCD_CS_PIN
    int "LCD Chip Select pin"
    default 5

config BOARD_LCD_DC_PIN
    int "LCD Data/Command pin"
    default 6

endif # LCD_MY_DISPLAY_DRIVER

config BOARD_UART_CONSOLE
    int "Console UART number"
    default 0

config BOARD_CUSTOM_INIT
    bool "Enable custom board initialization"
    default y
```

## Architecture-Specific Patterns

### ARM Architecture (STM32, Kinetis, etc.)
```bash
# Configuration
CONFIG_ARCH="arm"
CONFIG_ARCH_CHIP="<your-arm-chip>"
CONFIG_ARCH_CHIP_<CHIP_NAME>=y

# Reference boards
nuttx/boards/arm/stm32f7/stm32f746g-disco/
nuttx/boards/arm/imxrt/imxrt1060-evk/
nuttx/boards/arm/stm32l4/stm32l476g-disco/
```

### RISC-V Architecture
```bash
# Configuration
CONFIG_ARCH="risc-v"
CONFIG_ARCH_CHIP="<your-riscv-chip>"
CONFIG_ARCH_CHIP_<CHIP_NAME>=y

# Reference boards
nuttx/boards/risc-v/common/cores/
nuttx/boards/risc-v/k210/kendryte-k210/
```

### xtensa Architecture (ESP32, ESP32-S3, etc.)
```bash
# Configuration
CONFIG_ARCH="xtensa"
CONFIG_ARCH_CHIP="<your-xtensa-chip>"
CONFIG_ARCH_CHIP_<CHIP_NAME>=y

# Reference boards
nuttx/boards/xtensa/esp32s3/esp32s3-devkit/
nuttx/boards/xtensa/esp32/esp32-devkitc/
```

### MIPS Architecture
```bash
# Configuration
CONFIG_ARCH="mips"
CONFIG_ARCH_CHIP="<your-mips-chip>"
CONFIG_ARCH_CHIP_<CHIP_NAME>=y

# Reference boards
nuttx/boards/mips/pic32mx/pic32mx-starter-kit/
```

## Reference Examples

### Successful Out-of-Tree Boards
- `/home/huang/Work/nx/boards/lckfb-szpi-esp32s3/` - xtensa custom board
- `/home/huang/Work/nx/boards/stm32f746g-disco/` - ARM custom board

### Successful Out-of-Tree Configurations
- `/home/huang/Work/nx/boards/esp32s3/` - xtensa configurations
- `/home/huang/Work/nx/boards/esp32/` - xtensa configurations
- `/home/huang/Work/nx/boards/esp32c3/` - RISC-V configurations

### In-Tree Reference Implementations (Choose based on your architecture)
- **ARM**: `/home/huang/Work/nx/nuttx/boards/arm/stm32f7/stm32f746g-disco/`
- **RISC-V**: `/home/huang/Work/nx/nuttx/boards/risc-v/common/cores/`
- **xtensa**: `/home/huang/Work/nx/nuttx/boards/xtensa/esp32s3/esp32s3-devkit/`
- **MIPS**: `/home/huang/Work/nx/nuttx/boards/mips/pic32mx/pic32mx-starter-kit/`

## Build and Test

### Build the Board
```bash
# From NuttX root directory
cd nuttx
make -j$(nproc) defconfig BOARDS_DIR=../boards/my-custom-board defconfig
make -j$(nproc)
```

### Flash and Test (Architecture-Specific)
```bash
# For ARM boards (using OpenOCD/J-Link)
openocd -f interface/jlink.cfg -f target/<your-chip>.cfg -c "program build/nuttx.bin verify reset exit"

# For xtensa boards
esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0x0 build/bootloader/bootloader.bin 0x10000 build/nuttx.bin

# For RISC-V boards (using OpenOCD)
openocd -f interface/ftdi.cfg -f target/<your-chip>.cfg -c "program build/nuttx.bin verify reset exit"
```

## Key Principles

1. **Architecture Independence**: Follow patterns that work across all architectures
2. **Leverage Existing Code**: Don't re-implement chip-level drivers
3. **Minimal Customization**: Only add board-specific initialization
4. **Clean Separation**: Keep custom code separate from upstream
5. **Consistent Patterns**: Follow existing board directory structures
6. **Documentation**: Document any custom configurations or features

## Common Architecture Patterns

### ARM-Specific Patterns
```c
/* Configure ARM-specific peripherals */
#ifdef CONFIG_ARCH_ARM
  /* STM32 example */
  stm32_configgpio(BOARD_CUSTOM_PIN, STM32GPIO_PULLUP | STM32GPIO_OUTPUT);
  stm32_gpiowrite(BOARD_CUSTOM_PIN, true);
#endif
```

### RISC-V-Specific Patterns
```c
/* Configure RISC-V-specific peripherals */
#ifdef CONFIG_ARCH_RISCV
  /* Your RISC-V chip specific GPIO configuration */
  riscv_configgpio(BOARD_CUSTOM_PIN, RISCVGPIO_OUTPUT);
  riscv_gpiowrite(BOARD_CUSTOM_PIN, true);
#endif
```

### xtensa-Specific Patterns
```c
/* Configure xtensa-specific peripherals */
#ifdef CONFIG_ARCH_XTENSA
  /* ESP32-S3 example */
  esp32s3_configgpio(BOARD_CUSTOM_PIN, OUTPUT);
  esp32s3_gpiowrite(BOARD_CUSTOM_PIN, true);
#endif
```

### Generic Board Initialization
```c
/* Architecture-agnostic board initialization */
void board_specific_init(void)
{
#ifdef CONFIG_DEV_GPIO
  /* Use board-specific pin definitions */
  board_gpio_config(BOARD_CUSTOM_PIN, false, false, false, 0);
  board_gpio_write(BOARD_CUSTOM_PIN, true);
#endif

#ifdef CONFIG_BOARD_CUSTOM_CLOCK
  /* Configure board-specific clock if needed */
  board_clock_config(BOARD_CUSTOM_CLOCK_FREQ);
#endif
}
```

## Troubleshooting

### Architecture-Specific Issues

#### Configuration Issues
- Verify `CONFIG_ARCH` matches your target architecture
- Ensure `CONFIG_ARCH_CHIP` points to correct chip family
- Check that required chip features are enabled for your architecture

#### Build Issues
- Verify `Make.defs` includes correct reference board for your architecture
- Check for architecture-specific toolchain requirements
- Ensure linker scripts are compatible with your architecture

#### Runtime Issues
- Verify pin configurations match hardware wiring
- Check serial console configuration for your architecture
- Validate memory configuration for your specific chip
- Verify interrupt vector table configuration

### Common Architecture Mismatches
- **Wrong ARCH value**: Use "arm", "risc-v", "xtensa", "mips", etc.
- **Missing chip support**: Ensure your specific chip variant exists
- **Toolchain issues**: Use architecture-specific toolchains
- **Memory layout**: Each architecture has different memory requirements

This guide provides a foundation for creating custom NuttX boards across all supported architectures while maintaining compatibility with upstream codebase.

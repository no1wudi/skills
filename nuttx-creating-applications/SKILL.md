---
name: nuttx-creating-applications
description: Creates user applications, examples, and system utilities for NuttX following proper file structure and build conventions. Provides comprehensive instructions for adding code to the nuttx-apps repository. Use when developing new applications, examples, or system utilities for NuttX.
---

# Creating NuttX Applications Guide

This guide provides comprehensive instructions for creating applications for the NuttX RTOS, following established conventions and best practices.

## Application Structure

A NuttX application requires the following essential files:

```
your_app/
├── your_app_main.c    # Main application source code
├── Makefile           # Build configuration
├── Make.defs          # Integration with build system
├── Kconfig            # Configuration options
└── CMakeLists.txt     # CMake build support (optional)
```

## File Templates and Conventions

### 1. Main Source File (`your_app_main.c`)

```c
/****************************************************************************
 * path/to/your_app/your_app_main.c
 *
 * SPDX-License-Identifier: Apache-2.0
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
 ****************************************************************************/

/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <stdio.h>

/****************************************************************************
 * Pre-processor Definitions
 ****************************************************************************/

/* Add your macros and constants here */

/****************************************************************************
 * Private Types
 ****************************************************************************/

/* Add your private type definitions here */

/****************************************************************************
 * Private Function Prototypes
 ****************************************************************************/

/* Add your private function prototypes here */

/****************************************************************************
 * Private Data
 ****************************************************************************/

/* Add your private data here */

/****************************************************************************
 * Public Functions
 ****************************************************************************/

/****************************************************************************
 * your_app_main
 ****************************************************************************/

int main(int argc, FAR char *argv[])
{
  /* Your application code here */

  printf("Your application started!\n");

  return 0;
}
```

### 2. Makefile

```makefile
###########################################################################
# path/to/your_app/Makefile
#
# SPDX-License-Identifier: Apache-2.0
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

include $(APPDIR)/Make.defs

# Your application built-in application info

PROGNAME  = $(CONFIG_EXAMPLES_YOUR_APP_PROGNAME)
PRIORITY  = $(CONFIG_EXAMPLES_YOUR_APP_PRIORITY)
STACKSIZE = $(CONFIG_EXAMPLES_YOUR_APP_STACKSIZE)
MODULE    = $(CONFIG_EXAMPLES_YOUR_APP)

# Your Application Example

MAINSRC = your_app_main.c

include $(APPDIR)/Application.mk
```

### 3. Make.defs

```makefile
###########################################################################
# path/to/your_app/Make.defs
#
# SPDX-License-Identifier: Apache-2.0
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

ifneq ($(CONFIG_EXAMPLES_YOUR_APP),)
CONFIGURED_APPS += $(APPDIR)/examples/your_app
endif
```

### 4. Kconfig

```kconfig
#
# For a description of the syntax of this configuration file,
# see the file kconfig-language.txt in the NuttX tools repository.
#

config EXAMPLES_YOUR_APP
	tristate "Your App Example"
	default n
	---help---
		Enable the Your App example

if EXAMPLES_YOUR_APP

config EXAMPLES_YOUR_APP_PROGNAME
	string "Program name"
	default "your_app"
	---help---
		This is the name of the program that will be used when the NSH ELF
		program is installed.

config EXAMPLES_YOUR_APP_PRIORITY
	int "Your App task priority"
	default 100

config EXAMPLES_YOUR_APP_STACKSIZE
	int "Your App stack size"
	default DEFAULT_TASK_STACKSIZE

config EXAMPLES_YOUR_APP_USE_GPIO
	bool "Enable GPIO support"
	default n
	---help---
		Enable GPIO access in your application

endif
```

### 5. CMakeLists.txt

```cmake
# ##############################################################################
# path/to/your_app/CMakeLists.txt
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed to the Apache Software Foundation (ASF) under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  The ASF licenses this
# file to you under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
#
# ##############################################################################

if(CONFIG_EXAMPLES_YOUR_APP)
  nuttx_add_application(
    NAME
    ${CONFIG_EXAMPLES_YOUR_APP_PROGNAME}
    SRCS
    your_app_main.c
    STACKSIZE
    ${CONFIG_EXAMPLES_YOUR_APP_STACKSIZE}
    PRIORITY
    ${CONFIG_EXAMPLES_YOUR_APP_PRIORITY})
endif()
```

## Code Conventions

### Header Format
- Use Apache 2.0 license header
- Include file path in comment
- Maintain consistent spacing and indentation

### Includes
- Always include `<nuttx/config.h>` first
- Group standard C headers, then NuttX-specific headers
- Use alphabetical order within groups

### Naming Conventions
- Functions: `snake_case` with module prefix (e.g., `your_app_init()`)
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Types: `snake_case` with `_t` suffix for typedefs

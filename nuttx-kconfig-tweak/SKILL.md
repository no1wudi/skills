---
name: nuttx-kconfig-tweak
description: Performs kconfig tweaking for NuttX kernel configuration via kconfig-tweak CLI tool. Enables/disables features and sets option values. Use for scripted configuration changes.
---

# NuttX kconfig-tweak

## Syntax

```bash
kconfig-tweak --file <config> --enable|disable|set-str|set-val <option> [value]
```

## Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| `--enable` | Boolean on | `--enable CONFIG_EXAMPLES_HELLO` |
| `--disable` | Boolean off | `--disable CONFIG_EXAMPLES_HELLO` |
| `--set-str` | String value | `--set-str CONFIG_SYSTEM_HOSTNAME "myboard"` |
| `--set-val` | Number value | `--set-val CONFIG_IDLETHREAD_STACKSIZE 2048` |

---

## Workflow

### Step 1: Detect Build System from .config Path

```bash
# Path determines build system:
# - nuttx/.config    → Makefile
# - build/.config    → CMake
PATH_OF_CONFIG_FILE="${1:-$(find . -name .config -type f 2>/dev/null | head -1)}"
```

### Step 2: Apply Tweaks Based on Build System

#### Makefile Workflow
```bash
kconfig-tweak --file <PATH_OF_CONFIG_FILE> --enable CONFIG_EXAMPLES_HELLO
kconfig-tweak --file <$PATH_OF_CONFIG_FILE> --set-str CONFIG_SYSTEM_HOSTNAME "devboard"

# Update build system
make olddefconfig
```

#### CMake Workflow
```bash
kconfig-tweak --file <PATH_OF_CONFIG_FILE> --enable CONFIG_EXAMPLES_HELLO

# Reconfigure and build
cmake -B build nuttx
ninja -C build
```

---

## Common Tweaks

```bash
# Enable drivers
kconfig-tweak --file .config --enable CONFIG_I2C
kconfig-tweak --file .config --enable CONFIG_SPI

# Adjust stacks
kconfig-tweak --file .config --set-val CONFIG_IDLETHREAD_STACKSIZE 2048
kconfig-tweak --file .config --set-val CONFIG_THREAD_DEFAULT_STACKSIZE 1024

# Set names
kconfig-tweak --file .config --set-str CONFIG_SYSTEM_HOSTNAME "mynuttx"
```

---

## Verification

```bash
# Check option exists
grep CONFIG_EXAMPLES_HELLO .config

# Check if enabled
grep -q "CONFIG_EXAMPLES_HELLO=y" .config && echo "Enabled" || echo "Disabled"
```

---
name: nuttx-kconfig-tweak
description: Performs kconfig tweaking for NuttX kernel configuration via kconfig-tweak.py wrapper script. Enables/disables features and sets option values. Use for scripted configuration changes. Auto-detects build system and directories from CMake or Makefile layouts.
---

# NuttX kconfig-tweak

## Syntax

```bash
python3 kconfig-tweak.py --file <config> --enable|disable|set-str|set-val|set <option> [value]
```

The script `kconfig-tweak.py` is located alongside this skill file.

## Operations

| Operation | Purpose | Example |
|-----------|---------|---------|
| `--enable` | Boolean on | `--enable EXAMPLES_HELLO` |
| `--disable` | Boolean off | `--disable EXAMPLES_HELLO` |
| `--set-str` | String value | `--set-str CONFIG_SYSTEM_HOSTNAME "myboard"` |
| `--set-val` | Number value | `--set-val CONFIG_IDLETHREAD_STACKSIZE 2048` |
| `--set` | Set any value | `--set EXAMPLES_HELLO_PRIORITY=500` |

## Auto-Detection

The script automatically detects directories when not explicitly provided:
- Config file: Searches `.config`, `build/.config`, `nuttx/.config`
- NuttX source: From CMakeCache.txt or parent directories
- Apps directory: From generated Kconfig files
- Build directory: From config file location or CMakeCache.txt

---

## Workflow

The script automatically detects build system from the config file location.

### Apply Tweaks

```bash
python3 kconfig-tweak.py --enable EXAMPLES_HELLO
python3 kconfig-tweak.py --set-str CONFIG_SYSTEM_HOSTNAME "devboard"

# Combine multiple operations
python3 kconfig-tweak.py \
  --enable EXAMPLES_HELLO \
  --set-val EXAMPLES_HELLO_PRIORITY 700
```

### Update Build System

#### Makefile Workflow
```bash
make olddefconfig
make
```

#### CMake Workflow
```bash
cmake -B build nuttx
ninja -C build
```

---

## Common Tweaks

```bash
# Enable drivers
python3 kconfig-tweak.py --enable I2C
python3 kconfig-tweak.py --enable SPI

# Adjust stacks
python3 kconfig-tweak.py --set-val IDLETHREAD_STACKSIZE 2048
python3 kconfig-tweak.py --set-val THREAD_DEFAULT_STACKSIZE 1024

# Set names
python3 kconfig-tweak.py --set-str CONFIG_SYSTEM_HOSTNAME "mynuttx"

# Using CONFIG_ prefix (optional)
python3 kconfig-tweak.py --enable CONFIG_I2C
```

---

## Requirements

```bash
# Install kconfiglib (provides setconfig command)
pip install kconfiglib
```

## Verification

```bash
# Check option exists
grep CONFIG_EXAMPLES_HELLO .config

# Check if enabled
grep -q "CONFIG_EXAMPLES_HELLO=y" .config && echo "Enabled" || echo "Disabled"
```

# Skills

Skills are directories containing domain-specific knowledge and guides for performing particular tasks. Each skill is organized by directory path and uses markdown files to describe detailed instructions and usage patterns.

The directory structure and file names indicate the specific domain and purpose of each skill, making it easy to locate relevant guidance for specialized tasks.

## Directory Structure

```
skills/
├── nuttx/
│   ├── applications/
│   │   └── creating-applications.md
│   ├── drivers/
│   │   ├── sensors/
│   │   │   └── creating-sensor-drivers.md
│   │   └── gpio-expanders/
│   │       └── esp32s3-lckfb-pca9557-gpio.md
│   └── boards/
│       ├── out-of-tree-board-creation.md
│       └── out-of-tree-board-configs.md
├── wamr/
│   └── compilation/
│       └── wamrc-aot-compilation.md
├── LICENSE
└── README.md
```

## Naming Conventions

All directories and files under `skills/` follow consistent naming rules:

### Directory Names
- Use **kebab-case** (lowercase letters with hyphens separating words)
- First-level directory: domain name (e.g., `nuttx`, `wamr`)
- Subdirectories: category or subcategory names (e.g., `applications`, `drivers`, `sensors`, `compilation`)

### File Names
- Use **kebab-case** with `.md` extension
- Descriptive and self-explanatory (e.g., `creating-applications.md`, `out-of-tree-board-creation.md`)
- Use action verbs when appropriate (e.g., `creating-`, `compiling-`)

### Path Structure Pattern
```
skills/{domain}/{category}/{subcategory}/{descriptive-name}.md
```
- `{domain}`: Top-level category (e.g., `nuttx`, `wamr`)
- `{category}`: Primary topic area (e.g., `applications`, `drivers`, `boards`, `compilation`)
- `{subcategory}`: Optional nested category for grouping (e.g., `sensors`, `gpio-expanders`)
- `{descriptive-name}.md`: Concise, hyphenated description of the guide's content

## Available Skills

### NuttX Domain

#### Applications

- **[Creating NuttX Applications Guide](nuttx/applications/creating-applications.md)** - Comprehensive guide for creating NuttX applications including file templates, build system integration, and coding conventions.

#### Drivers

- **[Creating NuttX Sensor Drivers Guide](nuttx/drivers/sensors/creating-sensor-drivers.md)** - Complete guide for creating sensor drivers in NuttX, covering both character device and uORB implementations with I2C communication patterns.

- **[ESP32S3-LCKFB PCA9557 GPIO Expander Guide](nuttx/drivers/gpio-expanders/esp32s3-lckfb-pca9557-gpio.md)** - Complete usage patterns for the PCA9557 I2C GPIO expander on ESP32S3-LCKFB board, including GPIO control examples, pin mapping, and best practices for GPIO expander integration.

#### Boards

- **[NuttX Out-of-Tree Board Creation Guide](nuttx/boards/out-of-tree-board-creation.md)** - Comprehensive guide for creating completely new custom NuttX boards from scratch, covering both board creation and configuration patterns with practical examples and code templates.

- **[NuttX Out-of-Tree Configurations Guide](nuttx/boards/out-of-tree-board-configs.md)** - Complete guide for creating custom configurations for existing NuttX boards without modifying upstream code, including directory patterns, build system integration, and best practices.

### WAMR Domain

#### Compilation

- **[WAMR AOT Compilation Guide with wamrc](wamr/compilation/wamrc-aot-compilation.md)** - Complete guide for using wamrc to produce optimal AOT files for common CPU targets, including ARM and RISC-V architectures, with support for both XIP and non-XIP scenarios, featuring practical examples and optimization strategies.

# Skills

Skills are directories containing domain-specific knowledge and guides for performing particular tasks. Each skill is organized by directory path and uses markdown files to describe detailed instructions and usage patterns.

The directory structure and file names indicate the specific domain and purpose of each skill, making it easy to locate relevant guidance for specialized tasks.

## Available Skills

### NuttX Domain

- **[Creating NuttX Applications Guide](nuttx/creating-applications.md)** - Comprehensive guide for creating NuttX applications including file templates, build system integration, and coding conventions.

- **[Creating NuttX Sensor Drivers Guide](nuttx/creating-sensor-drivers.md)** - Complete guide for creating sensor drivers in NuttX, covering both character device and uORB implementations with I2C communication patterns.

- **[ESP32S3-LCKFB PCA9557 GPIO Expander Guide](nuttx/esp32s3-lckfb-pca9557-gpio.md)** - Complete usage patterns for the PCA9557 I2C GPIO expander on ESP32S3-LCKFB board, including GPIO control examples, pin mapping, and best practices for GPIO expander integration.

- **[NuttX Out-of-Tree Configurations Guide](nuttx/out-of-tree-board-configs.md)** - Complete guide for creating custom configurations for existing NuttX boards without modifying upstream code, including directory patterns, build system integration, and best practices.

- **[NuttX Out-of-Tree Board Creation Guide](nuttx/out-of-tree-board-creation.md)** - Comprehensive guide for creating completely new custom NuttX boards from scratch, covering both board creation and configuration patterns with practical examples and code templates.

### WAMR Domain

- **[WAMR AOT Compilation Guide with wamrc](wamr/wamrc-aot-compilation.md)** - Complete guide for using wamrc to produce optimal AOT files for common CPU targets, including ARM and RISC-V architectures, with support for both XIP and non-XIP scenarios, featuring practical examples and optimization strategies.

---
name: wamr-aot-compilation
description: Perform ahead-of-time (AOT) compilation of WebAssembly modules using wamrc for improved performance in WAMR runtime.
---

# WAMR AOT Compilation Guide with wamrc

This guide provides comprehensive instructions for using wamrc to produce optimal AOT (Ahead-of-Time) compiled files for common CPU targets, including ARM and RISC-V architectures, with support for both XIP (Execute In Place) and non-XIP scenarios.

## Overview

WAMR (WebAssembly Micro Runtime) provides the `wamrc` compiler to convert WebAssembly bytecode (.wasm) into native AOT files (.aot) for improved performance and reduced runtime overhead. This guide covers optimal compilation strategies for different CPU architectures and deployment scenarios.

## Basic Usage

```bash
# Basic compilation
wamrc -o output.aot input.wasm

# View all available options
wamrc --help

# List supported targets
wamrc --target=help

# List supported CPUs for a target
wamrc --target=armv7 --cpu=help
```

## ARM Architecture Targets

### ARM 32-bit Targets

#### ARM Cortex-M Series (Microcontrollers)

**Cortex-M3 (No FPU)**
```bash
# Standard compilation
wamrc --target=thumbv7m --cpu=cortex-m3 \
      --target-abi=eabi -o output.aot input.wasm

# XIP compilation (for flash execution)
wamrc --target=thumbv7m --cpu=cortex-m3 \
      --target-abi=eabi --xip \
      --enable-builtin-intrinsics=i64.common,fp.common,fpxint \
      -o output.aot input.wasm
```

**Cortex-M4 (Single Precision FPU)**
```bash
# Standard compilation
wamrc --target=thumbv7em --cpu=cortex-m4 \
      --target-abi=eabihf -o output.aot input.wasm

# XIP compilation
wamrc --target=thumbv7em --cpu=cortex-m4 \
      --target-abi=eabihf --xip \
      --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

**Cortex-M7 (Single/Double Precision FPU)**
```bash
# Standard compilation with single precision
wamrc --target=thumbv7em --cpu=cortex-m7 \
      --target-abi=eabihf -o output.aot input.wasm

# XIP compilation
wamrc --target=thumbv7em --cpu=cortex-m7 \
      --target-abi=eabihf --xip \
      --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

#### ARM Cortex-A Series (Application Processors)

**Cortex-A7 (32-bit)**
```bash
# Standard compilation
wamrc --target=armv7 --cpu=cortex-a7 \
      --target-abi=gnueabihf -o output.aot input.wasm

# With NEON SIMD
wamrc --target=armv7 --cpu=cortex-a7 \
      --target-abi=gnueabihf --cpu-features=+neon \
      -o output.aot input.wasm

# XIP compilation
wamrc --target=armv7 --cpu=cortex-a7 \
      --target-abi=gnueabihf --xip \
      -o output.aot input.wasm
```

**Cortex-A53 (ARMv8 32-bit mode)**
```bash
# Standard compilation
wamrc --target=armv8 --cpu=cortex-a53 \
      --target-abi=gnueabihf -o output.aot input.wasm

# Optimized for size
wamrc --target=armv8 --cpu=cortex-a53 \
      --target-abi=gnueabihf --size-level=2 \
      -o output.aot input.wasm
```

### ARM 64-bit Targets

**Cortex-A53 (AArch64)**
```bash
# Standard compilation
wamrc --target=aarch64 --cpu=cortex-a53 \
      --target-abi=gnu -o output.aot input.wasm

# Optimized for performance
wamrc --target=aarch64 --cpu=cortex-a53 \
      --target-abi=gnu --opt-level=3 \
      --cpu-features=+neon -o output.aot input.wasm

# XIP compilation
wamrc --target=aarch64 --cpu=cortex-a53 \
      --target-abi=gnu --xip \
      -o output.aot input.wasm
```

**Cortex-A72/73**
```bash
# High-performance compilation
wamrc --target=aarch64 --cpu=cortex-a72 \
      --target-abi=gnu --opt-level=3 \
      --cpu-features=+neon,+crc -o output.aot input.wasm
```

## RISC-V Architecture Targets

### RISC-V 32-bit Targets

**Basic RISC-V 32-bit (Integer only)**
```bash
# Minimal configuration
wamrc --target=riscv32 --target-abi=ilp32 \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c \
      -o output.aot input.wasm

# XIP compilation
wamrc --target=riscv32 --target-abi=ilp32 \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c \
      --xip --enable-builtin-intrinsics=i64.common,fp.common,fpxint \
      -o output.aot input.wasm
```

**RISC-V 32-bit with Single Precision FPU**
```bash
# With floating point support
wamrc --target=riscv32 --target-abi=ilp32f \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c,+f \
      -o output.aot input.wasm

# XIP compilation
wamrc --target=riscv32 --target-abi=ilp32f \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c,+f \
      --xip --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

**RISC-V 32-bit with Double Precision FPU**
```bash
# Full floating point support
wamrc --target=riscv32 --target-abi=ilp32d \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c,+f,+d \
      -o output.aot input.wasm

# XIP compilation
wamrc --target=riscv32 --target-abi=ilp32d \
      --cpu=generic-rv32 --cpu-features=+m,+a,+c,+f,+d \
      --xip --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

### RISC-V 64-bit Targets

**Basic RISC-V 64-bit**
```bash
# Standard 64-bit compilation
wamrc --target=riscv64 --target-abi=lp64 \
      --cpu=generic-rv64 --cpu-features=+m,+a,+c \
      --size-level=1 -o output.aot input.wasm

# XIP compilation
wamrc --target=riscv64 --target-abi=lp64 \
      --cpu=generic-rv64 --cpu-features=+m,+a,+c \
      --xip --size-level=1 -o output.aot input.wasm
```

**RISC-V 64-bit with Single Precision FPU**
```bash
wamrc --target=riscv64 --target-abi=lp64f \
      --cpu=generic-rv64 --cpu-features=+m,+a,+c,+f \
      --size-level=1 -o output.aot input.wasm
```

**RISC-V 64-bit with Double Precision FPU**
```bash
wamrc --target=riscv64 --target-abi=lp64d \
      --cpu=generic-rv64 --cpu-features=+m,+a,+c,+f,+d \
      --size-level=1 -o output.aot input.wasm
```

## XIP (Execute In Place) Compilation

XIP is essential for devices with limited RAM or when executing from flash/ROM. Use the `--xip` flag which is a shorthand for `--enable-indirect-mode --disable-llvm-intrinsics`.

### XIP Optimization Guidelines

**For targets without hardware floating point:**
```bash
wamrc --target=<target> --xip \
      --enable-builtin-intrinsics=i64.common,fp.common,fpxint \
      -o output.aot input.wasm
```

**For targets with single precision FPU only:**
```bash
wamrc --target=<target> --xip \
      --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

**For targets with double precision FPU:**
```bash
wamrc --target=<target> --xip \
      --enable-builtin-intrinsics=i64.common \
      -o output.aot input.wasm
```

### Available Builtin Intrinsics for XIP

**Combined options:**
- `all` - All intrinsic functions
- `i32.common` - i32.div_s, i32.div_u, i32.rem_s, i32.rem_u
- `i64.common` - i64.div_s, i64.div_u, i64.rem_s, i64.rem_u, i64.or, i64.and
- `f32.common` - All f32 operations
- `f64.common` - All f64 operations
- `fp.common` - Both f32.common and f64.common
- `fpxint` - Float to integer conversions
- `constop` - Constant operations

## Optimization Levels

### Performance Optimization
```bash
# Maximum performance
wamrc --target=<target> --opt-level=3 --size-level=0 \
      -o output.aot input.wasm
```

### Size Optimization
```bash
# Minimum size
wamrc --target=<target> --opt-level=2 --size-level=3 \
      -o output.aot input.wasm

# Balanced approach (default)
wamrc --target=<target> --opt-level=3 --size-level=3 \
      -o output.aot input.wasm
```

### Memory-Constrained Optimization
```bash
# For embedded systems with limited memory
wamrc --target=<target> --size-level=2 \
      --bounds-checks=0 -o output.aot input.wasm
```

## Special Features

### Bounds Checking
```bash
# Enable bounds checking (default on 32-bit)
wamrc --target=<target> --bounds-checks=1 \
      -o output.aot input.wasm

# Disable bounds checking (default on 64-bit)
wamrc --target=<target> --bounds-checks=0 \
      -o output.aot input.wasm
```

### SIMD Support
```bash
# Enable SIMD (where supported)
wamrc --target=<target> --enable-simd \
      -o output.aot input.wasm

# Disable SIMD
wamrc --target=<target> --disable-simd \
      -o output.aot input.wasm
```

### Multi-threading Support
```bash
# Enable multi-threading
wamrc --target=<target> --enable-multi-thread \
      -o output.aot input.wasm
```

### Stack Trace Support
```bash
# Enable stack traces for debugging
wamrc --target=<target> --enable-dump-call-stack \
      -o output.aot input.wasm
```

## Practical Examples

### Example 1: ARM Cortex-M4 with XIP
```bash
# For a microcontroller with 256KB flash, 64KB RAM
wamrc --target=thumbv7em --cpu=cortex-m4 \
      --target-abi=eabihf --xip \
      --enable-builtin-intrinsics=i64.common \
      --size-level=2 --opt-level=2 \
      -o firmware.aot app.wasm
```

### Example 2: RISC-V 64-bit Linux
```bash
# For a RISC-V 64-bit Linux system
wamrc --target=riscv64 --target-abi=lp64d \
      --cpu=generic-rv64 --cpu-features=+m,+a,+c,+f,+d \
      --opt-level=3 --size-level=1 \
      -o app.aot app.wasm
```

### Example 3: ARM Cortex-A53 with SIMD
```bash
# For an ARM64 system with SIMD requirements
wamrc --target=aarch64 --cpu=cortex-a53 \
      --target-abi=gnu --enable-simd \
      --cpu-features=+neon --opt-level=3 \
      -o optimized.aot compute.wasm
```

## Best Practices

1. **Choose the right target**: Always specify the exact CPU model for optimal performance
2. **Use XIP for flash-based systems**: Reduces RAM usage significantly
3. **Optimize intrinsic functions**: Only enable what your hardware supports
4. **Consider size vs performance**: Use `--size-level` and `--opt-level` appropriately
5. **Test on target hardware**: Always validate AOT files on the actual target device
6. **Version compatibility**: Use matching wamrc and WAMR runtime versions for best compatibility

## Troubleshooting

### Common Issues

**Relocation errors in XIP mode:**
- Ensure all necessary intrinsic functions are enabled
- Check that the target supports the selected CPU features

**Performance issues:**
- Verify the correct CPU and ABI are specified
- Consider enabling/disabling bounds checks based on your platform
- Check if SIMD is properly enabled for supported targets

**Memory constraints:**
- Use higher `--size-level` values (2-3) for smaller code
- Consider XIP mode for flash-based systems
- Disable unnecessary features like SIMD or multi-threading

This guide provides the foundation for producing optimal AOT files with wamrc across various ARM and RISC-V targets. Adjust the parameters based on your specific hardware constraints and performance requirements.

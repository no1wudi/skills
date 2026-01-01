---
name: nuttx-pr-description
description: Creates well-structured pull request descriptions for NuttX projects following Apache NuttX contribution guidelines. Use when preparing to submit pull requests for nuttx, nuttx-apps, or related repositories.
---

# NuttX Pull Request Description

## PR Template

```bash
cat > PR.md <<'EOF'
## Summary

[Why change is necessary, what it does and how]

## Impact

- Impact on user: YES/NO
- Impact on build: YES/NO
- Impact on hardware: YES/NO
- Impact on documentation: YES/NO
- Impact on security: YES/NO
- Impact on compatibility: YES/NO

## Testing

Build Host: [OS, arch, toolchain]
Target: [board:config]

[Testing description and logs]

EOF
${EDITOR:-vim} PR.md
```

## Sample: Bug Fix

```bash
cat > PR.md <<'EOF'
## Summary

Fix memory leak in UART driver. DMA buffers were not freed when closing the device.

## Impact

- Impact on user: YES - Reduced memory usage
- Impact on build: NO
- Impact on hardware: NO
- Impact on documentation: NO
- Impact on security: YES - Prevents DoS from memory exhaustion
- Impact on compatibility: NO

## Testing

Build Host: Ubuntu 22.04, x86_64, GCC 11.3.0
Target: ARM stm32f4discovery:nsh

Verified with test_uart (100 open/close cycles), heapinfo shows no memory loss.

Build output:
```
CC: drivers/serial/uart_dma.c
LD: nuttx
```

Runtime output:
```
nsh> test_uart
Completed 100 iterations
nsh> heapinfo
Free memory: 104576 bytes
```
EOF
```

## Step-by-Step Workflow

### Step 1: Review Last Commit

```bash
# View last commit
git show HEAD --stat
```

### Step 2: Create PR Description

```bash
cat > PR.md <<'EOF'
## Summary

[Describe why the change is necessary, what it does, and how]

## Impact

- Impact on user: YES/NO
- Impact on build: YES/NO
- Impact on hardware: YES/NO
- Impact on documentation: YES/NO
- Impact on security: YES/NO
- Impact on compatibility: YES/NO

## Testing

Build Host: [OS, arch, toolchain]
Target: [board:config]

[Describe testing approach and include logs]

EOF
```

### Step 3: Fill in Details

1. **Summary**: Explain why the change is needed, what it does, and how
2. **Impact**: Check each item (YES/NO) and add brief explanations
3. **Testing**: Include build host, target board, testing steps, and logs

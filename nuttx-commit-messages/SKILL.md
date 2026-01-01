---
name: nuttx-commit-messages
description: Creates properly formatted NuttX git commit messages following Apache NuttX contribution guidelines. Use when writing commit messages for nuttx, nuttx-apps, or related repositories.
---

# NuttX Commit Messages

## 1. Write Standard Commit Message

```bash
# Use git commit with -s flag to add Signed-off-by
git commit -s -m "area/subsystem: Add brief description.

Add detailed description of what changed and why.
* you can also use bullet points
* to note different things briefly"
```

## 2. Commit Message Structure

```
area/subsystem: Add brief description.

Add detailed description of what changed, how, and why.
* bullet points can be used
* to note different things briefly

Signed-off-by: AuthorName <Valid@EmailAddress>
```

## Required Format

Per [CONTRIBUTING.md](../../nuttx/CONTRIBUTING.md) Section 1.5:

1. **Topic** - Functional area prefix, colon, brief description with period
2. **Blank line**
3. **Description** - What changed, how, and why (may use bullet points)
4. **Blank line**
5. **Signature** - Created with `git commit -s`

## Mandatory Fields

Per [CONTRIBUTING.md](../../nuttx/CONTRIBUTING.md) Section 1.6:

1. **topic** - Area/subsystem prefix with description
2. **description** - Detailed explanation
3. **signature** - `Signed-off-by:` line

## Special Tags

Per [CONTRIBUTING.md](../../nuttx/CONTRIBUTING.md):

- `[BREAKING]` - Prefix for breaking changes (Section 1.12, 1.13)

## Example Area Prefixes

### Architecture Prefixes

- `arch/` - Architecture-specific code
- `arch/arm/` - ARM architecture code
- `arch/armv8-m/` - ARMv8-M specific code
- `arch/arm64/` - ARM64/Aarch64 code
- `arch/risc-v/` - RISC-V architecture code
- `arch/xtensa/` - Xtensa architecture code
- `arch/tricore/` - TriCore architecture code

### Driver Prefixes

- `drivers/` - Hardware drivers
- `drivers/sensors/` - Sensor drivers
- `drivers/timers/` - Timer drivers
- `drivers/ptp/` - PTP clock drivers
- `drivers/ptp_clock/` - PTP clock core

### Network Prefixes

- `net/` - Networking code
- `net/can/` - CAN networking
- `net/tcp/` - TCP protocol
- `net/arp/` - ARP protocol
- `net/ipv4/` - IPv4 protocol
- `net/ipv6/` - IPv6 protocol
- `net/udp/` - UDP protocol
- `net/icmp/` - ICMP protocol
- `net/ethernet/` - Ethernet
- `net/local/` - Local sockets
- `net/rpmsg/` - RPMsg networking
- `net/neighbor/` - Neighbor discovery
- `net/netdev/` - Network device interface

### Other Prefixes

- `fs/` - File system code
- `fs/epoll/` - Epoll event notification
- `fs/mqueue/` - Message queue
- `mm/` - Memory management
- `sched/` - Scheduler code
- `sched/clock/` - Clock/time management
- `libc/` - C library functions
- `boards/` - Board-specific code
- `board/` - Specific board prefix
- `Documentation/` - Documentation changes
- `tools/` - Build tools and scripts
- `syscall/` - System calls
- `virtio/` - VirtIO framework

## When to Use This Skill

- Writing commit messages for NuttX kernel changes
- Writing commit messages for NuttX Applications (nuttx-apps)

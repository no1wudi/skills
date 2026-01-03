---
name: nuttx-lckfb-esp32s3
description: Workflows and guides for developing, building, flashing, and interacting with LCKFB SZPI ESP32S3 board. Use this when working on the LCKFB ESP32S3 board with NuttX.
---

# LCKFB ESP32S3 Board Interaction Guide

This guide provides workflows for building, flashing, and interacting with the LCKFB SZPI ESP32S3 board in NuttX.

## Build Output Management

**NuttX builds generate 1000+ lines of output**. Commands use `| tail -n 100` to limit output. Always append `| tail -n 100` when redirecting to files or viewing logs.

## 1. Build Firmware

```bash
# Configure for LCKFB ESP32S3 board using nxtool
python3 boards/tool/nxtool.py configure \
  ../boards/lckfb-szpi-esp32s3/configs/app \
  nuttx

# Apply configuration and build firmware (limit output)
make -C nuttx olddefconfig
make -C nuttx -j8 2>&1 | tail -n 100
```

## 2. Flash Firmware to Board

```bash
# Flash firmware using nxtool
python3 boards/tool/nxtool.py flash nuttx --port /dev/ttyACM0
```

## 3. Access Serial Console

```bash
# Create background tmux session with picocom for NSH console (runs continuously, use nsh for example session name)
tmux new-session -d -s nsh 'picocom -b 115200 /dev/ttyUSB0'

# Send commands to NSH shell
tmux send-keys -t nsh Enter
tmux send-keys -t nsh 'ps' Enter
tmux send-keys -t nsh 'ls /dev' Enter
tmux send-keys -t nsh 'free' Enter

# View serial output (capture last 100 lines)
tmux capture-pane -p -t nsh | tail -n 100

# View more lines
tmux capture-pane -p -t nsh | tail -n 500

# List all tmux sessions
tmux list-sessions

# Kill NSH console session when done
tmux kill-session -t nsh

# Common NSH commands
help                    # Show available commands
ps                      # List running tasks
free                    # Show memory usage
ls /dev                 # List device nodes
```

## 4. Reset Board

```bash
# Reset board
esptool --chip esp32s3 --port /dev/ttyACM0 run
```

# Critical Rules
1. Use /dev/ttyACM0 for flashing firmware and resetting the board
2. Use /dev/ttyUSB0 for serial console access (NSH shell)

---

# Additional Info: PCA9557 GPIO Expander Control

This section provides information about controlling external GPIO pins on ESP32S3-LCKFB boards via PCA9557 I2C GPIO expander.

## Hardware Configuration

**Board**: ESP32S3-LCKFB
**Device**: PCA9557 8-bit I2C GPIO Expander
**Interface**: I2C (SCL=IO2, SDA=IO1, Address=0x19)
**Device Nodes**: `/dev/gpio0` through `/dev/gpio7` (8 pins total)
**Current Usage**: Only pins 0-2 are actively used
- IO0 → LCD_CS (LCD chip select)
- IO1 → PA_EN (Power amplifier enable)
- IO2 → DVP_PWDN (Digital video port power down)

## GPIO Usage Pattern

### Basic GPIO Control

```c
#include <fcntl.h>
#include <unistd.h>
#include <nuttx/fs/fs.h>

/* Define of GPIO device path */
#define SZPI_MY_PIN_PATH "/dev/gpio3"  // IO3

/* Example: Set GPIO pin HIGH */
int gpio_set_high(void)
{
  struct file f;
  int ret;

  /* Open of GPIO device */
  ret = file_open(&f, SZPI_MY_PIN_PATH, O_RDWR);
  if (ret < 0)
    {
        return ret;
      }

  /* Set pin HIGH ("1" = HIGH, "0" = LOW) */
  ret = file_write(&f, "1",1);
  if (ret < 0)
    {
        file_close(&f);
        return ret;
      }

  file_close(&f);
  return OK;
}

/* Example: Set GPIO pin LOW */
int gpio_set_low(void)
{
  struct file f;
  int ret;

  ret = file_open(&f, SZPI_MY_PIN_PATH, O_RDWR);
  if (ret < 0)
    {
        return ret;
      }

  /* Set pin LOW */
  ret = file_write(&f, "0",1);
  if (ret < 0)
    {
        file_close(&f);
        return ret;
      }

  file_close(&f);
  return OK;
}
```

### GPIO Read Operations

```c
/* Example: Read GPIO pin state */
int gpio_read_state(void)
{
  struct file f;
  char buffer[2];
  int ret;

  ret = file_open(&f, SZPI_MY_PIN_PATH, O_RDONLY);
  if (ret < 0)
    {
        return ret;
      }

  /* Read current pin state */
  ret = file_read(&f, buffer, 1);
  if (ret < 0)
    {
        file_close(&f);
        return ret;
      }

  file_close(&f);

  /* buffer[0] contains '0' or '1' */
  return (buffer[0] == '1') ?1 : 0;
}
```

## Pin Mapping Reference

| Device Node | Physical Pin | Current Usage | Description |
|-------------|--------------|----------------|-------------|
| `/dev/gpio0` | IO0 | LCD_CS | LCD chip select control |
| `/dev/gpio1` | IO1 | PA_EN | Power amplifier enable |
| `/dev/gpio2` | IO2 | DVP_PWDN | Digital video port power down |
| `/dev/gpio3` | IO3 | Available | Free for custom use |
| `/dev/gpio4` | IO4 | Available | Free for custom use |
| `/dev/gpio5` | IO5 | Available | Free for custom use |
| `/dev/gpio6` | IO6 | Available | Free for custom use |
| `/dev/gpio7` | IO7 | Available | Free for custom use |

## Best Practices

1. **Error Handling**: Always check return values from file operations
2. **Resource Management**: Always close file handles after use
3. **Pin Availability**: Verify pin usage before implementing new features
4. **Thread Safety**: Use mutex protection if accessing GPIO from multiple threads
5. **Initialization**: Configure GPIO directions during system startup if needed

## Integration Example

```c
/* System initialization example */
int board_gpio_expander_init(void)
{
  /* Configure unused pins as outputs with known states */

  /* Set IO3-IO7 to LOW by default (prevent floating inputs) */
  of const char *unused_pins[] = {
    "/dev/gpio3", "/dev/gpio4", "/dev/gpio5",
    "/dev/gpio6", "/dev/gpio7"
  };

  for (int i = 0; i < 5; i++)
    {
        struct file f;
        if (file_open(&f, unused_pins[i], O_RDWR) == OK)
          {
                file_write(&f, "0",1);  /* Set LOW */
                file_close(&f);
              }
      }

  return OK;
}
```

## Troubleshooting

- **Device not found**: Verify I2C connection and address (0x19)
- **Permission denied**: Check file permissions on `/dev/gpio*` nodes
- **No response**: Ensure I2C bus is properly initialized
- **Incorrect state**: Verify pin is configured as output

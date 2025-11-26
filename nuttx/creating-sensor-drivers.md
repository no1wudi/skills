# Writing NuttX Sensor Drivers Guide (uORB)

This guide provides instructions for creating uORB-based sensor drivers in NuttX.

## Overview

NuttX sensor drivers using the uORB (Micro Object Request Broker) framework provide:
- Publish/subscribe pattern for sensor data
- Automatic character device creation at `/dev/uorb/sensor_XXX`
- Ring buffer management and multi-subscriber support
- Standardized sensor data structures

## Driver Structure

A uORB sensor driver requires only 2 files:

```
nuttx/drivers/sensors/
├── your_device_uorb.c          # Complete uORB sensor driver
└── Make.defs                   # Build configuration (update existing)

nuttx/include/nuttx/sensors/
└── your_device.h               # Public API header

nuttx/drivers/sensors/
└── Kconfig                     # Configuration options (update existing)
```

## Implementation

### 1. Public API Header (`include/nuttx/sensors/your_device.h`)

```c
/****************************************************************************
 * include/nuttx/sensors/your_device.h
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

#ifndef __INCLUDE_NUTTX_SENSORS_YOUR_DEVICE_H
#define __INCLUDE_NUTTX_SENSORS_YOUR_DEVICE_H

#if defined(CONFIG_I2C) && defined(CONFIG_SENSORS_YOUR_DEVICE)

/****************************************************************************
 * Included Files
 ****************************************************************************/

#include <nuttx/config.h>

/****************************************************************************
 * Public Types
 ****************************************************************************/

struct i2c_master_s;

/****************************************************************************
 * Public Function Prototypes
 ****************************************************************************/

#ifdef __cplusplus
extern "C"
{
#endif

/****************************************************************************
 * Name: your_device_register_uorb
 *
 * Description:
 *   Register the sensor as uORB device, creates /dev/uorb/sensor_accelX
 *
 * Input Parameters:
 *   devno   - Sensor device instance number (0 = sensor_accel0)
 *   i2c     - I2C interface to communicate with sensor
 *
 * Returned Value:
 *   Zero (OK) on success; a negated errno value on failure.
 ****************************************************************************/

int your_device_register_uorb(int devno, FAR struct i2c_master_s *i2c);

#ifdef __cplusplus
}
#endif

#endif /* CONFIG_I2C && CONFIG_SENSORS_YOUR_DEVICE */
#endif /* __INCLUDE_NUTTX_SENSORS_YOUR_DEVICE_H */
```

### 2. uORB Driver (`drivers/sensors/your_device_uorb.c`)

```c
/****************************************************************************
 * drivers/sensors/your_device_uorb.c
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

#include <nuttx/config.h>
#include <nuttx/i2c/i2c_master.h>
#include <nuttx/kmalloc.h>
#include <nuttx/mutex.h>
#include <nuttx/wqueue.h>
#include <nuttx/sensors/sensor.h>
#include <nuttx/sensors/your_device.h>
#include <debug.h>
#include <errno.h>

#if defined(CONFIG_I2C) && defined(CONFIG_SENSORS_YOUR_DEVICE)

/****************************************************************************
 * Pre-processor Definitions
 ****************************************************************************/

/* Device I2C configuration */

#ifndef CONFIG_YOUR_DEVICE_I2C_FREQUENCY
#  define CONFIG_YOUR_DEVICE_I2C_FREQUENCY 400000
#endif

#define YOUR_DEVICE_ADDR         0x6a  /* I2C address */
#define YOUR_DEVICE_FREQ         CONFIG_YOUR_DEVICE_I2C_FREQUENCY
#define YOUR_DEVICE_DEVID        0x55  /* Device ID */

/* Register addresses */

#define YOUR_DEVICE_REG_WHO_AM_I 0x0f
#define YOUR_DEVICE_REG_CTRL1    0x20
#define YOUR_DEVICE_REG_STATUS   0x27
#define YOUR_DEVICE_REG_OUT_X_L  0x28

/* Configuration */

#define YOUR_DEVICE_MIN_INTERVAL 10000  /* 10ms minimum interval */

/****************************************************************************
 * Private Types
 ****************************************************************************/

struct your_device_sensor_s
{
  struct sensor_lowerhalf_s lower;     /* Must be first! */
  FAR struct i2c_master_s *i2c;        /* I2C interface */
  struct work_s work;                  /* Work queue for polling */
  mutex_t dev_lock;                    /* Device access mutex */
  uint32_t interval;                   /* Polling interval (us) */
  uint8_t addr;                        /* I2C address */
  int freq;                            /* I2C frequency */
  bool enabled;                        /* Sensor enabled */
};

/****************************************************************************
 * Private Function Prototypes
 ****************************************************************************/

/* I2C helpers */

static uint8_t your_device_getreg8(FAR struct your_device_sensor_s *priv,
                                   uint8_t regaddr);
static void your_device_putreg8(FAR struct your_device_sensor_s *priv,
                                uint8_t regaddr, uint8_t regval);
static int your_device_readregs(FAR struct your_device_sensor_s *priv,
                                uint8_t regaddr, FAR uint8_t *buffer,
                                uint8_t len);

/* Device operations */

static int your_device_checkid(FAR struct your_device_sensor_s *priv);
static int your_device_init(FAR struct your_device_sensor_s *priv);

/* Sensor operations */

static int your_device_activate(FAR struct sensor_lowerhalf_s *lower,
                                FAR struct file *filep, bool enable);
static int your_device_set_interval(FAR struct sensor_lowerhalf_s *lower,
                                    FAR struct file *filep,
                                    FAR uint32_t *period_us);
static void your_device_worker(FAR void *arg);

/****************************************************************************
 * Private Data
 ****************************************************************************/

static const struct sensor_ops_s g_sensor_ops =
{
  .activate     = your_device_activate,
  .set_interval = your_device_set_interval,
};

/****************************************************************************
 * Private Functions
 ****************************************************************************/

/****************************************************************************
 * Name: your_device_getreg8
 ****************************************************************************/

static uint8_t your_device_getreg8(FAR struct your_device_sensor_s *priv,
                                   uint8_t regaddr)
{
  struct i2c_msg_s msg[2];
  uint8_t regval = 0;

  msg[0].frequency = priv->freq;
  msg[0].addr      = priv->addr;
  msg[0].flags     = 0;
  msg[0].buffer    = &regaddr;
  msg[0].length    = 1;

  msg[1].frequency = priv->freq;
  msg[1].addr      = priv->addr;
  msg[1].flags     = I2C_M_READ;
  msg[1].buffer    = &regval;
  msg[1].length    = 1;

  if (I2C_TRANSFER(priv->i2c, msg, 2) < 0)
    {
      return 0;
    }

  return regval;
}

/****************************************************************************
 * Name: your_device_putreg8
 ****************************************************************************/

static void your_device_putreg8(FAR struct your_device_sensor_s *priv,
                                uint8_t regaddr, uint8_t regval)
{
  struct i2c_msg_s msg;
  uint8_t data[2];

  data[0] = regaddr;
  data[1] = regval;

  msg.frequency = priv->freq;
  msg.addr      = priv->addr;
  msg.flags     = 0;
  msg.buffer    = data;
  msg.length    = 2;

  I2C_TRANSFER(priv->i2c, &msg, 1);
}

/****************************************************************************
 * Name: your_device_readregs
 ****************************************************************************/

static int your_device_readregs(FAR struct your_device_sensor_s *priv,
                                uint8_t regaddr, FAR uint8_t *buffer,
                                uint8_t len)
{
  struct i2c_msg_s msg[2];

  msg[0].frequency = priv->freq;
  msg[0].addr      = priv->addr;
  msg[0].flags     = 0;
  msg[0].buffer    = &regaddr;
  msg[0].length    = 1;

  msg[1].frequency = priv->freq;
  msg[1].addr      = priv->addr;
  msg[1].flags     = I2C_M_READ;
  msg[1].buffer    = buffer;
  msg[1].length    = len;

  return I2C_TRANSFER(priv->i2c, msg, 2);
}

/****************************************************************************
 * Name: your_device_checkid
 ****************************************************************************/

static int your_device_checkid(FAR struct your_device_sensor_s *priv)
{
  uint8_t devid;

  devid = your_device_getreg8(priv, YOUR_DEVICE_REG_WHO_AM_I);
  if (devid != YOUR_DEVICE_DEVID)
    {
      snerr("Wrong device ID: 0x%02x, expected: 0x%02x\n",
            devid, YOUR_DEVICE_DEVID);
      return -ENODEV;
    }

  return OK;
}

/****************************************************************************
 * Name: your_device_init
 ****************************************************************************/

static int your_device_init(FAR struct your_device_sensor_s *priv)
{
  int ret;

  /* Initialize mutex */

  nxmutex_init(&priv->dev_lock);

  /* Check device ID */

  ret = your_device_checkid(priv);
  if (ret < 0)
    {
      snerr("Device check failed: %d\n", ret);
      nxmutex_destroy(&priv->dev_lock);
      return ret;
    }

  /* Configure device (example: enable sensor, set ODR to 100Hz) */

  your_device_putreg8(priv, YOUR_DEVICE_REG_CTRL1, 0x57);

  sninfo("Device initialized successfully\n");
  return OK;
}

/****************************************************************************
 * Name: your_device_activate
 ****************************************************************************/

static int your_device_activate(FAR struct sensor_lowerhalf_s *lower,
                                FAR struct file *filep, bool enable)
{
  FAR struct your_device_sensor_s *priv =
    (FAR struct your_device_sensor_s *)lower;

  priv->enabled = enable;

  if (enable)
    {
      /* Start polling worker */

      work_queue(HPWORK, &priv->work, your_device_worker, priv, 0);
    }
  else
    {
      /* Stop polling worker */

      work_cancel(HPWORK, &priv->work);
    }

  return OK;
}

/****************************************************************************
 * Name: your_device_set_interval
 ****************************************************************************/

static int your_device_set_interval(FAR struct sensor_lowerhalf_s *lower,
                                    FAR struct file *filep,
                                    FAR uint32_t *period_us)
{
  FAR struct your_device_sensor_s *priv =
    (FAR struct your_device_sensor_s *)lower;

  /* Enforce minimum interval */

  if (*period_us < YOUR_DEVICE_MIN_INTERVAL)
    {
      *period_us = YOUR_DEVICE_MIN_INTERVAL;
    }

  priv->interval = *period_us;
  return OK;
}

/****************************************************************************
 * Name: your_device_worker
 ****************************************************************************/

static void your_device_worker(FAR void *arg)
{
  FAR struct your_device_sensor_s *priv =
    (FAR struct your_device_sensor_s *)arg;
  struct sensor_accel data;
  uint8_t buffer[6];
  int ret;

  if (!priv->enabled)
    {
      return;
    }

  /* Acquire device lock */

  ret = nxmutex_lock(&priv->dev_lock);
  if (ret < 0)
    {
      goto reschedule;
    }

  /* Read accelerometer data (6 bytes: X_L, X_H, Y_L, Y_H, Z_L, Z_H) */

  ret = your_device_readregs(priv, YOUR_DEVICE_REG_OUT_X_L, buffer, 6);
  if (ret < 0)
    {
      snerr("Failed to read data: %d\n", ret);
      nxmutex_unlock(&priv->dev_lock);
      goto reschedule;
    }

  /* Convert to sensor_accel structure
   * Adjust scale factor based on your sensor's range and resolution
   * Example: ±2g range, 16-bit resolution = 2*2*9.81/32768 = 0.000598 m/s²
   */

  data.timestamp = sensor_get_timestamp();
  data.x = (int16_t)(buffer[0] | (buffer[1] << 8)) * 0.000598f;  /* m/s² */
  data.y = (int16_t)(buffer[2] | (buffer[3] << 8)) * 0.000598f;
  data.z = (int16_t)(buffer[4] | (buffer[5] << 8)) * 0.000598f;
  data.temperature = NAN;  /* Set if temperature is available */

  /* Push data to upper half */

  priv->lower.push_event(priv->lower.priv, &data, sizeof(data));

  nxmutex_unlock(&priv->dev_lock);

reschedule:

  /* Schedule next reading */

  if (priv->enabled)
    {
      work_queue(HPWORK, &priv->work, your_device_worker, priv,
                 USEC2TICK(priv->interval));
    }
}

/****************************************************************************
 * Public Functions
 ****************************************************************************/

/****************************************************************************
 * Name: your_device_register_uorb
 *
 * Description:
 *   Register the sensor as uORB device, creates /dev/uorb/sensor_accelX
 *
 ****************************************************************************/

int your_device_register_uorb(int devno, FAR struct i2c_master_s *i2c)
{
  FAR struct your_device_sensor_s *priv;
  int ret;

  /* Allocate device structure */

  priv = kmm_zalloc(sizeof(struct your_device_sensor_s));
  if (!priv)
    {
      snerr("Failed to allocate memory\n");
      return -ENOMEM;
    }

  /* Initialize device */

  priv->i2c = i2c;
  priv->addr = YOUR_DEVICE_ADDR;
  priv->freq = YOUR_DEVICE_FREQ;
  priv->enabled = false;
  priv->interval = 1000000;  /* Default 1 second */

  ret = your_device_init(priv);
  if (ret < 0)
    {
      snerr("Failed to initialize device: %d\n", ret);
      kmm_free(priv);
      return ret;
    }

  /* Initialize sensor interface */

  priv->lower.type = SENSOR_TYPE_ACCELEROMETER;
  priv->lower.nbuffer = 1;
  priv->lower.ops = &g_sensor_ops;

  /* Register with sensor framework - creates /dev/uorb/sensor_accelX */

  ret = sensor_register(&priv->lower, devno);
  if (ret < 0)
    {
      snerr("Failed to register sensor: %d\n", ret);
      nxmutex_destroy(&priv->dev_lock);
      kmm_free(priv);
      return ret;
    }

  sninfo("Sensor registered as sensor_accel%d\n", devno);
  return OK;
}

#endif /* CONFIG_I2C && CONFIG_SENSORS_YOUR_DEVICE */
```

## Build System Files

### 3. Make.defs Integration

Add to `drivers/sensors/Make.defs`:

```makefile
# Your sensor driver
ifeq ($(CONFIG_SENSORS_YOUR_DEVICE),y)
  CSRCS += your_device_uorb.c
endif
```

### 4. Kconfig Configuration

Add to `drivers/sensors/Kconfig`:

```kconfig
config SENSORS_YOUR_DEVICE
	bool "Your Sensor Device Driver"
	depends on I2C
	---help---
		Enable uORB driver for your sensor device.

if SENSORS_YOUR_DEVICE

config YOUR_DEVICE_I2C_FREQUENCY
	int "I2C frequency"
	default 400000
	---help---
		I2C frequency for communication with sensor.

endif # SENSORS_YOUR_DEVICE
```

## Usage Example

### Application Code

```c
/****************************************************************************
 * Example application using uORB sensor interface
 ****************************************************************************/

#include <fcntl.h>
#include <poll.h>
#include <sensor/accel.h>

int main(int argc, char *argv[])
{
  struct sensor_accel data;
  struct pollfd fds[1];
  int fd;
  int ret;

  /* Subscribe to accelerometer (opens /dev/uorb/sensor_accel0) */

  fd = orb_subscribe(ORB_ID(sensor_accel));
  if (fd < 0)
    {
      printf("Failed to subscribe\n");
      return -1;
    }

  /* Set sampling interval to 100Hz (10ms = 10000us) */

  orb_set_interval(fd, 10000);

  /* Setup poll */

  fds[0].fd = fd;
  fds[0].events = POLLIN;

  /* Read sensor data */

  while (1)
    {
      ret = poll(fds, 1, 1000);
      if (ret > 0 && (fds[0].revents & POLLIN))
        {
          orb_copy(ORB_ID(sensor_accel), fd, &data);
          printf("Accel: x=%.3f y=%.3f z=%.3f m/s²\n",
                 data.x, data.y, data.z);
        }
    }

  orb_unsubscribe(fd);
  return 0;
}
```

### Board Integration

Add to your board's initialization file (e.g., `boards/*/src/*_bringup.c`):

```c
#include <nuttx/sensors/your_device.h>

int board_sensor_initialize(void)
{
  struct i2c_master_s *i2c;
  int ret;

  /* Initialize I2C bus */

  i2c = esp32s3_i2cbus_initialize(0);  /* Adjust for your platform */
  if (!i2c)
    {
      return -ENODEV;
    }

  /* Register sensor - creates /dev/uorb/sensor_accel0 */

  ret = your_device_register_uorb(0, i2c);
  if (ret < 0)
    {
      syslog(LOG_ERR, "Failed to register sensor: %d\n", ret);
      return ret;
    }

  return OK;
}
```

## Key Concepts

### Sensor Types

Use standard sensor types from `<nuttx/sensors/sensor.h>`:

- `SENSOR_TYPE_ACCELEROMETER` → `/dev/uorb/sensor_accelX`
- `SENSOR_TYPE_GYROSCOPE` → `/dev/uorb/sensor_gyroX`
- `SENSOR_TYPE_MAGNETIC_FIELD` → `/dev/uorb/sensor_magX`
- `SENSOR_TYPE_BAROMETER` → `/dev/uorb/sensor_baroX`
- `SENSOR_TYPE_TEMPERATURE` → `/dev/uorb/sensor_tempX`

### Data Structures

Use standard sensor data structures from `<nuttx/sensors/sensor.h>`:

```c
struct sensor_accel
{
  uint64_t timestamp;   /* Microseconds */
  float x;              /* m/s² */
  float y;              /* m/s² */
  float z;              /* m/s² */
  float temperature;    /* °C (or NAN if not available) */
};

struct sensor_gyro
{
  uint64_t timestamp;   /* Microseconds */
  float x;              /* rad/s */
  float y;              /* rad/s */
  float z;              /* rad/s */
  float temperature;    /* °C (or NAN if not available) */
};

struct sensor_mag
{
  uint64_t timestamp;   /* Microseconds */
  float x;              /* µT */
  float y;              /* µT */
  float z;              /* µT */
  float temperature;    /* °C (or NAN if not available) */
  int32_t status;       /* Calibration status */
};
```

### Data Acquisition Modes

**Polling Mode** (shown in example above):
```c
static void your_device_worker(FAR void *arg)
{
  /* Periodically read sensor data */
  /* Push to upper half with push_event() */
  /* Reschedule work */
}
```
- Uses work queue to periodically read sensor
- Suitable for most sensors
- Adjustable interval via `set_interval()`

**Interrupt Mode**:
```c
static int your_device_interrupt(int irq, FAR void *context, FAR void *arg)
{
  FAR struct your_device_sensor_s *priv = arg;
  
  /* Schedule bottom half worker */
  work_queue(HPWORK, &priv->work, your_device_worker, priv, 0);
  return OK;
}
```
- Triggered by hardware interrupt
- Lower latency, more efficient
- Configure interrupt pin during init

**Fetch Mode** (on-demand):
```c
static int your_device_fetch(FAR struct sensor_lowerhalf_s *lower,
                             FAR struct file *filep,
                             FAR char *buffer, size_t buflen)
{
  /* Read data directly when user calls read() */
  /* No internal buffering, no worker thread */
  /* Return data immediately */
}
```
- Use `.fetch` instead of `.activate` and `.set_interval`
- Data read on-demand when application calls `read()`
- No background polling

### Sensor Operations Callbacks

The `struct sensor_ops_s` defines 12 callback functions for different sensor operations:

#### **Essential Callbacks (Required for Basic Functionality)**

**`activate`** ✅ **REQUIRED**
- Enable/disable sensor hardware (power management)
- Start/stop data conversion and measurement
- **Example**: Power on sensor, configure measurement mode
- **Must implement**: This is the primary on/off control

#### **Data Rate Control (Recommended)**

**`set_interval`** ⚪ **OPTIONAL**
- Set sensor output data rate (sampling period in microseconds)
- Driver can adjust requested period to nearest supported value
- **Best for**: Sensors with configurable data rates
- **Example**: Set accelerometer to 100Hz (10000μs period)

#### **Data Acquisition Mode Callbacks (Choose One Approach)**

**`fetch`** ⚪ **OPTIONAL** (Alternative to polling)
- Direct register read when application calls `read()`
- No background polling, no worker thread
- **Best for**: Low-ODR sensors, memory-constrained systems
- **Use instead of**: `activate` + `set_interval` + worker

**`batch`** ⚪ **OPTIONAL** (Advanced FIFO support)
- Configure hardware FIFO for accumulating multiple samples
- Reduces CPU load by batching data
- **Best for**: High-ODR sensors with FIFO capability
- **Requires**: Hardware FIFO support

**`flush`** ⚪ **OPTIONAL** (Companion to batch)
- Force immediate delivery of accumulated FIFO data
- Asynchronous operation with completion notification
- **Use with**: `batch` callback when FIFO management needed

#### **Per-User Management (Advanced)**

**`open`** ⚪ **OPTIONAL**
- Initialize resources for each user of the sensor
- Called every time device is opened
- **Use when**: Sensor needs per-user setup or resource allocation

**`close`** ⚪ **OPTIONAL**
- Cleanup resources when user closes the device
- Called every time device is closed
- **Use with**: `open` callback for proper cleanup

#### **Hardware Features (Sensor-Dependent)**

**`selftest`** ⚪ **OPTIONAL**
- Test sensor mechanical and electrical functionality
- Compare output against expected min/max values
- **Use when**: Sensor provides built-in self-test capability

**`set_calibvalue`** ⚪ **OPTIONAL**
- Write calibration data to persistent storage
- Store factory or user calibration parameters
- **Use when**: Sensor supports persistent calibration storage

**`calibrate`** ⚪ **OPTIONAL**
- Perform runtime calibration procedures
- May return calibration results immediately
- **Use when**: Sensor supports runtime calibration

**`get_info`** ⚪ **OPTIONAL** (But Recommended)
- Return device name, vendor, version, capabilities
- **Should implement**: For device identification and debugging

**`control`** ⚪ **OPTIONAL**
- Handle device-specific ioctl commands
- Custom modes, special configurations, reset operations
- **Use when**: Sensor has unique features beyond standard operations

#### **Implementation Strategy Guide**

**Minimal Polling Implementation** (Most Common):
```c
static const struct sensor_ops_s g_sensor_ops = {
  .activate = my_sensor_activate,      // ✅ REQUIRED
  .set_interval = my_sensor_set_interval,  // ⚪ Optional but recommended
};
```

**Fetch Mode Implementation** (Memory Efficient):
```c
static const struct sensor_ops_s g_sensor_ops = {
  .fetch = my_sensor_fetch,  // ⚪ Use instead of activate+set_interval
};
```

**Full-Featured Implementation** (All Capabilities):
```c
static const struct sensor_ops_s g_sensor_ops = {
  .open = my_sensor_open,
  .close = my_sensor_close,
  .activate = my_sensor_activate,      // ✅ REQUIRED
  .set_interval = my_sensor_set_interval,
  .batch = my_sensor_batch,
  .fetch = my_sensor_fetch,
  .flush = my_sensor_flush,
  .selftest = my_sensor_selftest,
  .set_calibvalue = my_sensor_set_calibvalue,
  .calibrate = my_sensor_calibrate,
  .get_info = my_sensor_get_info,
  .control = my_sensor_control,
};
```

#### **Callback Selection Guide**

| Sensor Type | Recommended Callbacks | Notes |
|-------------|----------------------|-------|
| Simple sensor | `activate` + `set_interval` | Standard polling mode |
| Low-ODR sensor | `fetch` | Direct read, no polling |
| High-ODR with FIFO | `activate` + `set_interval` + `batch` + `flush` | Hardware batching |
| Multi-user sensor | `open` + `close` + `activate` | Per-user management |
| Factory-calibrated | `get_info` + `selftest` | Verification only |
| Field-calibratable | `calibrate` + `set_calibvalue` | Runtime calibration |
| Custom features | `control` | Device-specific commands |

### Multi-Sensor Devices

For devices with multiple sensor types (e.g., IMU with accel + gyro):

```c
struct your_device_sensor_s
{
  struct sensor_lowerhalf_s accel_lower;  /* Accel interface */
  struct sensor_lowerhalf_s gyro_lower;   /* Gyro interface */
  /* ... shared I2C and config ... */
};

int your_device_register_uorb(int devno, FAR struct i2c_master_s *i2c)
{
  /* ... initialize device ... */
  
  /* Register accelerometer */
  priv->accel_lower.type = SENSOR_TYPE_ACCELEROMETER;
  sensor_register(&priv->accel_lower, devno);
  
  /* Register gyroscope */
  priv->gyro_lower.type = SENSOR_TYPE_GYROSCOPE;
  sensor_register(&priv->gyro_lower, devno);
}
```

This creates:
- `/dev/uorb/sensor_accel0`
- `/dev/uorb/sensor_gyro0`

## Best Practices

1. **Thread Safety**: Always protect I2C access with mutex
2. **Error Handling**: Check all I2C transaction return values
3. **Memory**: Use `kmm_zalloc()` and check for NULL
4. **Timestamps**: Use `sensor_get_timestamp()` for consistency
5. **Units**: Follow SI units (m/s² for accel, rad/s for gyro, µT for mag)
6. **Device ID**: Always verify device ID during initialization
7. **Resource Cleanup**: Free allocated memory and destroy mutex on error paths
8. **Scale Factors**: Calculate accurate conversion from raw ADC to physical units
9. **NAN Values**: Use `NAN` for unavailable fields (e.g., temperature)

## Testing

Enable the listener tool to test your driver:

```bash
NuttShell (NSH) NuttX-12.0.0
nsh> uorb_listener sensor_accel0
  timestamp: 123456789
  x: 0.123
  y: -0.456
  z: 9.789
  temperature: 25.3
```

Or use the sensor command:

```bash
nsh> sensor accel0 10
```

This will print 10 samples from sensor_accel0.

## Common Sensor Types Reference

| Sensor Type | Device Path | Data Structure | Units |
|------------|-------------|----------------|-------|
| Accelerometer | `/dev/uorb/sensor_accelX` | `struct sensor_accel` | m/s² |
| Gyroscope | `/dev/uorb/sensor_gyroX` | `struct sensor_gyro` | rad/s |
| Magnetometer | `/dev/uorb/sensor_magX` | `struct sensor_mag` | µT |
| Barometer | `/dev/uorb/sensor_baroX` | `struct sensor_baro` | hPa |
| Temperature | `/dev/uorb/sensor_tempX` | `struct sensor_temp` | °C |
| Light | `/dev/uorb/sensor_lightX` | `struct sensor_light` | lux |
| Proximity | `/dev/uorb/sensor_proxX` | `struct sensor_prox` | cm |
| Humidity | `/dev/uorb/sensor_humiX` | `struct sensor_humi` | % |

## Real-World Example Reference

For a complete working example, see:
- `nuttx/drivers/sensors/bmp180_uorb.c` - Simple barometer (polling mode)
- `nuttx/drivers/sensors/bmi088_uorb.c` - Multi-sensor IMU (accel + gyro)
- `nuttx/drivers/sensors/lsm9ds1_uorb.c` - 9-DOF IMU (accel + gyro + mag)

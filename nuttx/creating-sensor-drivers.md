# Writing NuttX Sensor Drivers Guide

This guide provides comprehensive instructions for creating sensor drivers in NuttX, covering both character device and uORB (Micro Object Request Broker) implementations.

## Overview

NuttX supports two main paradigms for sensor drivers:

1. **Character Device Drivers** - Direct device interface through `/dev/*`
2. **uORB Drivers** - Message-based interface for publish/subscribe patterns

## Driver Structure

A NuttX sensor driver requires the following essential files:

```
nuttx/drivers/sensors/
├── your_device_base.h          # Hardware abstraction header (private)
├── your_device_base.c          # Hardware abstraction implementation
├── your_device.c               # Character device implementation
├── your_device_uorb.c          # uORB implementation (optional)
└── Make.defs                   # Added to drivers/sensors/Make.defs

nuttx/include/nuttx/sensors/
└── your_device.h               # Public API header

nuttx/drivers/sensors/
└── Kconfig                     # Configuration options (added to existing file)
```

## Architecture Pattern

### 1. Three-Layer Architecture

**Base Layer** (`*_base.h/c`):
- Hardware abstraction (I2C communication)
- Device-specific operations (calibration, data reading)
- Shared between character and uORB implementations

**Interface Layer** (`*.c`):
- Character device: File operations (`read`, `write`, `ioctl`)
- uORB device: Sensor framework operations (`activate`, `set_interval`)

**API Layer** (`*.h`):
- Public registration functions
- Configuration-dependent interface selection
- Board integration entry points

## Character Device Implementation

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
 *****************************************************************************/

#include <nuttx/config.h>

/****************************************************************************
 * Pre-processor Definitions
 *****************************************************************************/

/* Configuration ************************************************************/

/* Prerequisites:
 *
 * CONFIG_SENSORS_YOUR_DEVICE
 *   Enables support for the Your Device driver
 */

/****************************************************************************
 * Public Types
 *****************************************************************************/

struct i2c_master_s;

/****************************************************************************
 * Public Function Prototypes
 *****************************************************************************/

#ifdef __cplusplus
#define EXTERN extern "C"
extern "C"
{
#else
#define EXTERN extern
#endif

/****************************************************************************
 * Name: your_device_register
 *
 * Description:
 *   Register the Your Device character device as 'devpath'
 *
 * Input Parameters:
 *   path/no - The full path (or number) to the driver to register.
 *             E.g.:("/dev/sensor0", i2c) or (0, i2c)
 *   i2c     - An instance of the I2C interface to use to communicate with
 *             Your Device
 *
 * Returned Value:
 *   Zero (OK) on success; a negated errno value on failure.
 *
 ****************************************************************************/

#ifndef CONFIG_SENSORS_YOUR_DEVICE_UORB
int your_device_register(FAR const char *devpath, FAR struct i2c_master_s *i2c);
#else
int your_device_register_uorb(int devno, FAR struct i2c_master_s *i2c);
#endif /* CONFIG_SENSORS_YOUR_DEVICE_UORB */

#undef EXTERN
#ifdef __cplusplus
}
#endif

#endif /* CONFIG_I2C && CONFIG_SENSORS_YOUR_DEVICE */
#endif /* __INCLUDE_NUTTX_SENSORS_YOUR_DEVICE_H */
```

### 2. Hardware Abstraction Header (`drivers/sensors/your_device_base.h`)

```c
/****************************************************************************
 * drivers/sensors/your_device_base.h
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

#include <inttypes.h>
#include <stdlib.h>
#include <errno.h>
#include <debug.h>

#include <nuttx/kmalloc.h>
#include <nuttx/signal.h>
#include <nuttx/fs/fs.h>
#include <nuttx/i2c/i2c_master.h>
#include <nuttx/sensors/your_device.h>

#if defined(CONFIG_I2C) && defined(CONFIG_SENSORS_YOUR_DEVICE)

/****************************************************************************
 * Pre-processor Definitions
 *****************************************************************************/

/* Your sensor I2C address */
#define YOUR_DEVICE_ADDR         0x19
#define YOUR_DEVICE_FREQ         400000
#define YOUR_DEVICE_DEVID        0x55

/* Register addresses */
#define YOUR_DEVICE_REG_STATUS   0x00
#define YOUR_DEVICE_REG_DATA     0x01
#define YOUR_DEVICE_REG_CONFIG   0x02
#define YOUR_DEVICE_REG_ID       0x0f

/* Configuration flags */
#define YOUR_DEVICE_ENABLE       0x01
#define YOUR_DEVICE_DISABLE      0x00

/****************************************************************************
 * Private Type
 ****************************************************************************/

struct your_device_dev_s
{
  FAR struct i2c_master_s *i2c;      /* I2C interface */
  uint8_t addr;                      /* Your Device I2C address */
  int freq;                          /* Your Device Frequency */
  mutex_t dev_lock;                  /* Mutex for device access */
  
  /* Add your sensor-specific configuration fields here */
  uint8_t acc_range;
  uint8_t gyro_range;
  uint8_t sample_mode;
};

/****************************************************************************
 * Public Function Prototypes
 ****************************************************************************/

/* I2C communication helpers */
uint8_t your_device_getreg8(FAR struct your_device_dev_s *priv, uint8_t regaddr);
uint16_t your_device_getreg16(FAR struct your_device_dev_s *priv, uint8_t regaddr);
void your_device_putreg8(FAR struct your_device_dev_s *priv, uint8_t regaddr,
                        uint8_t regval);

/* Device operations */
int your_device_checkid(FAR struct your_device_dev_s *priv);
int your_device_reset(FAR struct your_device_dev_s *priv);
int your_device_init(FAR struct your_device_dev_s *dev);

/* Data structures */
struct your_device_data_s
{
  int16_t x;        /* X-axis raw value */
  int16_t y;        /* Y-axis raw value */
  int16_t z;        /* Z-axis raw value */
  uint32_t timestamp; /* Timestamp in milliseconds */
};

/* Data reading functions */
int your_device_read_data(FAR struct your_device_dev_s *priv,
                         FAR struct your_device_data_s *data);
int your_device_readregs(FAR struct your_device_dev_s *priv, uint8_t regaddr,
                         FAR uint8_t *buffer, uint8_t len);

#endif /* CONFIG_I2C && CONFIG_SENSORS_YOUR_DEVICE */
```

### 3. Character Device Driver (`drivers/sensors/your_device.c`)

```c
/****************************************************************************
 * drivers/sensors/your_device.c
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
#include <nuttx/arch.h>
#include <nuttx/kmalloc.h>
#include <nuttx/fs/fs.h>
#include <nuttx/i2c/i2c_master.h>
#include <nuttx/mutex.h>
#include <nuttx/signal.h>
#include <debug.h>
#include <errno.h>
#include <string.h>

#include "your_device_base.h"

/****************************************************************************
 * Pre-processor Definitions
 *****************************************************************************/

#ifndef CONFIG_YOUR_DEVICE_I2C_FREQUENCY
#  define CONFIG_YOUR_DEVICE_I2C_FREQUENCY 400000 /* 400 KHz */
#endif

/* Debug features */
#ifdef CONFIG_DEBUG_SENSORS
#  define snerr(format, ...)    _err(format, ##__VA_ARGS__)
#  define sninfo(format, ...)   _info(format, ##__VA_ARGS__)
#else
#  define snerr(format, ...)
#  define sninfo(format, ...)
#endif

/****************************************************************************
 * Private Function Prototypes
 *****************************************************************************/

/* Character device file operations */
static int your_device_open(FAR struct file *filep);
static int your_device_close(FAR struct file *filep);
static ssize_t your_device_read(FAR struct file *filep, FAR char *buffer, size_t buflen);
static int your_device_ioctl(FAR struct file *filep, int cmd, unsigned long arg);

/****************************************************************************
 * Private Data
 *****************************************************************************/

static const struct file_operations g_your_device_fops =
{
  your_device_open,                   /* open */
  your_device_close,                  /* close */
  your_device_read,                   /* read */
  NULL,                               /* write */
  NULL,                               /* seek */
  your_device_ioctl,                  /* ioctl */
};

/****************************************************************************
 * Public Functions
 *****************************************************************************/

/****************************************************************************
 * your_device_register
 ****************************************************************************/

int your_device_register(FAR const char *devpath, FAR struct i2c_master_s *i2c)
{
  FAR struct your_device_dev_s *priv;
  int ret;

  DEBUGASSERT(devpath != NULL && i2c != NULL);

  priv = (FAR struct your_device_dev_s *)
          kmm_malloc(sizeof(struct your_device_dev_s));
  if (priv == NULL)
    {
      snerr("Failed to allocate instance\n");
      return -ENOMEM;
    }

  priv->i2c = i2c;
  priv->addr = YOUR_DEVICE_ADDR;
  priv->freq = CONFIG_YOUR_DEVICE_I2C_FREQUENCY;

  ret = register_driver(devpath, &g_your_device_fops, 0666, priv);
  if (ret < 0)
    {
      snerr("Failed to register driver: %d\n", ret);
      kmm_free(priv);
      return ret;
    }

  ret = your_device_init(priv);
  if (ret < 0)
    {
      snerr("Failed to initialize your_device: %d\n", ret);
      unregister_driver(devpath);
      kmm_free(priv);
      return ret;
    }

  sninfo("your_device registered at %s\n", devpath);
  return OK;
}

/****************************************************************************
 * Private Functions
 ****************************************************************************/

/****************************************************************************
 * your_device_open
 ****************************************************************************/

static int your_device_open(FAR struct file *filep)
{
  return OK;
}

/****************************************************************************
 * your_device_close
 ****************************************************************************/

static int your_device_close(FAR struct file *filep)
{
  return OK;
}

/****************************************************************************
 * your_device_read
 ****************************************************************************/

static ssize_t your_device_read(FAR struct file *filep, FAR char *buffer, size_t buflen)
{
  FAR struct inode *inode = filep->f_inode;
  FAR struct your_device_dev_s *priv = inode->i_private;
  struct your_device_data_s data;
  int ret;

  if (!priv || !buffer)
    {
      return -EINVAL;
    }

  if (buflen < sizeof(struct your_device_data_s))
    {
      return -EOVERFLOW;
    }

  /* Acquire device lock */
  ret = nxmutex_lock(&priv->dev_lock);
  if (ret < 0)
    {
      return ret;
    }

  /* Read sensor data */
  ret = your_device_read_data(priv, &data);
  if (ret < 0)
    {
      nxmutex_unlock(&priv->dev_lock);
      return ret;
    }

  /* Copy data to user buffer */
  memcpy(buffer, &data, sizeof(struct your_device_data_s));

  nxmutex_unlock(&priv->dev_lock);
  return sizeof(struct your_device_data_s);
}

/****************************************************************************
 * your_device_ioctl
 ****************************************************************************/

static int your_device_ioctl(FAR struct file *filep, int cmd, unsigned long arg)
{
  FAR struct inode *inode = filep->f_inode;
  FAR struct your_device_dev_s *priv = inode->i_private;
  int ret = OK;

  if (!priv)
    {
      return -ENODEV;
    }

  /* Acquire device lock */
  ret = nxmutex_lock(&priv->dev_lock);
  if (ret < 0)
    {
      return ret;
    }

  switch (cmd)
    {
    /* Add your sensor-specific ioctl commands here */

    default:
      sninfo("Unknown IOCTL command: 0x%04x\n", cmd);
      ret = -ENOTTY;
      break;
    }

  nxmutex_unlock(&priv->dev_lock);
  return ret;
}
```

### 4. Hardware Abstraction Implementation (`drivers/sensors/your_device_base.c`)

```c
/****************************************************************************
 * drivers/sensors/your_device_base.c
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
#include <debug.h>
#include <errno.h>

#include "your_device_base.h"

/****************************************************************************
 * Private Functions
 ****************************************************************************/

/****************************************************************************
 * your_device_getreg8
 ****************************************************************************/

uint8_t your_device_getreg8(FAR struct your_device_dev_s *priv, uint8_t regaddr)
{
  struct i2c_msg_s msg[2];
  uint8_t regval = 0;
  int ret;

  /* Setup read transaction */
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

  ret = I2C_TRANSFER(priv->i2c, msg, 2);
  return (ret < 0) ? 0 : regval;
}

/****************************************************************************
 * your_device_getreg16
 ****************************************************************************/

uint16_t your_device_getreg16(FAR struct your_device_dev_s *priv, uint8_t regaddr)
{
  struct i2c_msg_s msg[2];
  uint8_t buffer[2];
  int ret;

  /* Setup read transaction */
  msg[0].frequency = priv->freq;
  msg[0].addr      = priv->addr;
  msg[0].flags     = 0;
  msg[0].buffer    = &regaddr;
  msg[0].length    = 1;

  msg[1].frequency = priv->freq;
  msg[1].addr      = priv->addr;
  msg[1].flags     = I2C_M_READ;
  msg[1].buffer    = buffer;
  msg[1].length    = 2;

  ret = I2C_TRANSFER(priv->i2c, msg, 2);
  return (ret < 0) ? 0 : (uint16_t)(buffer[0] | (buffer[1] << 8));
}

/****************************************************************************
 * your_device_putreg8
 ****************************************************************************/

void your_device_putreg8(FAR struct your_device_dev_s *priv, uint8_t regaddr,
                        uint8_t regval)
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
 * your_device_checkid
 ****************************************************************************/

int your_device_checkid(FAR struct your_device_dev_s *priv)
{
  uint8_t devid = your_device_getreg8(priv, YOUR_DEVICE_REG_ID);
  
  if (devid != YOUR_DEVICE_DEVID)
    {
      snerr("Wrong device ID: %02x, expected: %02x\n", 
            devid, YOUR_DEVICE_DEVID);
      return -ENODEV;
    }

  return OK;
}

/****************************************************************************
 * your_device_reset
 ****************************************************************************/

int your_device_reset(FAR struct your_device_dev_s *priv)
{
  /* Add reset sequence if needed */
  return OK;
}

/****************************************************************************
 * your_device_init
 ****************************************************************************/

int your_device_init(FAR struct your_device_dev_s *dev)
{
  int ret;

  if (!dev)
    {
      return -EINVAL;
    }

  /* Initialize mutex for thread safety */
  nxmutex_init(&dev->dev_lock);

  /* Check device identification */
  ret = your_device_checkid(dev);
  if (ret < 0)
    {
      snerr("Device identification failed: %d\n", ret);
      nxmutex_destroy(&dev->dev_lock);
      return ret;
    }

  /* Reset device */
  ret = your_device_reset(dev);
  if (ret < 0)
    {
      snerr("Device reset failed: %d\n", ret);
      nxmutex_destroy(&dev->dev_lock);
      return ret;
    }

  /* Configure device for your sensor requirements */
  /* Add your sensor-specific configuration here */

  return OK;
}

/****************************************************************************
 * your_device_read_data
 ****************************************************************************/

int your_device_read_data(FAR struct your_device_dev_s *priv,
                         FAR struct your_device_data_s *data)
{
  uint8_t buffer[6];
  int ret;

  if (!priv || !data)
    {
      return -EINVAL;
    }

  /* Read sensor data registers */
  ret = your_device_readregs(priv, YOUR_DEVICE_REG_DATA, buffer, 6);
  if (ret < 0)
    {
      return ret;
    }

  /* Parse data (adjust based on your sensor's protocol) */
  data->x = (int16_t)(buffer[0] | (buffer[1] << 8));
  data->y = (int16_t)(buffer[2] | (buffer[3] << 8));
  data->z = (int16_t)(buffer[4] | (buffer[5] << 8));

  return OK;
}

/****************************************************************************
 * your_device_readregs
 ****************************************************************************/

int your_device_readregs(FAR struct your_device_dev_s *priv, uint8_t regaddr,
                         FAR uint8_t *buffer, uint8_t len)
{
  struct i2c_msg_s msg[2];
  int ret;

  if (!priv || !buffer || len == 0)
    {
      return -EINVAL;
    }

  /* Setup read transaction */
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

  ret = I2C_TRANSFER(priv->i2c, msg, 2);
  return (ret < 0) ? ret : OK;
}
```

## uORB Implementation

### 5. uORB Driver (`drivers/sensors/your_device_uorb.c`)

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
#include <nuttx/arch.h>
#include <nuttx/kmalloc.h>
#include <nuttx/mutex.h>
#include <nuttx/wqueue.h>
#include <nuttx/i2c/i2c_master.h>
#include <nuttx/sensors/sensor.h>
#include <debug.h>
#include <errno.h>
#include <string.h>

#include "your_device_base.h"

/* Include standard sensor data structures */
#include <nuttx/sensors/sensor.h>

/****************************************************************************
 * Pre-processor Definitions
 *****************************************************************************/

#ifndef CONFIG_YOUR_DEVICE_I2C_FREQUENCY
#  define CONFIG_YOUR_DEVICE_I2C_FREQUENCY 400000 /* 400 KHz */
#endif

#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
#  ifndef CONFIG_SENSORS_YOUR_DEVICE_POLL_INTERVAL
#    define CONFIG_SENSORS_YOUR_DEVICE_POLL_INTERVAL 1000000 /* 1 second */
#  endif
#endif

/* Debug features */
#ifdef CONFIG_DEBUG_SENSORS
#  define snerr(format, ...)    _err(format, ##__VA_ARGS__)
#  define sninfo(format, ...)   _info(format, ##__VA_ARGS__)
#else
#  define snerr(format, ...)
#  define sninfo(format, ...)
#endif

/****************************************************************************
 * Private Types
 *****************************************************************************/

/* Sensor lower half structure */
struct your_device_sensor_s
{
  struct sensor_lowerhalf_s lower;     /* Sensor lower half interface */
#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
  struct work_s work;                  /* Work queue for polling mode */
  uint64_t last_update;                /* Last update timestamp */
  uint32_t interval;                   /* Polling interval in microseconds */
#endif
  FAR struct your_device_dev_s *dev;   /* Pointer to base device */
  float scale;                         /* Scale factor for data conversion */
  bool enabled;                        /* Sensor enabled flag */
};

/* Complete uORB device structure */
struct your_device_uorb_dev_s
{
  struct your_device_dev_s base;       /* Base device structure */
  struct your_device_sensor_s sensor;  /* Sensor interface */
};

/****************************************************************************
 * Private Function Prototypes
 *****************************************************************************/

/* Sensor methods */
static int your_device_activate(FAR struct sensor_lowerhalf_s *lower,
                                FAR struct file *filep, bool enable);
#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
static int your_device_set_interval(FAR struct sensor_lowerhalf_s *lower,
                                   FAR struct file *filep,
                                   FAR uint32_t *period_us);
static void your_device_worker(FAR void *arg);
#else
static int your_device_fetch(FAR struct sensor_lowerhalf_s *lower,
                            FAR struct file *filep,
                            FAR char *buffer, size_t buflen);
#endif

/* Sensor operations */
static int your_device_read_data(FAR struct your_device_dev_s *dev,
                                FAR struct sensor_accel *data);

/****************************************************************************
 * Private Data
 *****************************************************************************/

/* Sensor operation table */
static const struct sensor_ops_s g_sensor_ops =
{
  .activate     = your_device_activate,     /* Enable/disable sensor */
#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
  .set_interval = your_device_set_interval, /* Set polling interval */
#else
  .fetch        = your_device_fetch,        /* Fetch sensor data */
#endif
};

/****************************************************************************
 * Public Functions
 *****************************************************************************/

/****************************************************************************
 * your_device_register_uorb
 ****************************************************************************/

int your_device_register_uorb(int devno, FAR struct i2c_master_s *i2c)
{
  FAR struct your_device_uorb_dev_s *dev;
  struct sensor_lowerhalf_s *lower;
  int ret = OK;

  if (!i2c)
    {
      return -EINVAL;
    }

  dev = (FAR struct your_device_uorb_dev_s *)
        kmm_zalloc(sizeof(struct your_device_uorb_dev_s));
  if (!dev)
    {
      return -ENOMEM;
    }

  /* Initialize base device */
  dev->base.i2c = i2c;
  dev->base.addr = YOUR_DEVICE_ADDR;
  dev->base.freq = CONFIG_YOUR_DEVICE_I2C_FREQUENCY;

  /* Initialize sensor interface */
  lower = &dev->sensor.lower;
  lower->type = SENSOR_TYPE_ACCELEROMETER;  /* Adjust based on your sensor type */
  lower->nbuffer = 2;                       /* Buffer size for sensor data */
  lower->ops = &g_sensor_ops;

  dev->sensor.dev = &dev->base;
  dev->sensor.enabled = false;
#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
  dev->sensor.interval = CONFIG_SENSORS_YOUR_DEVICE_POLL_INTERVAL;
  dev->sensor.last_update = 0;
  memset(&dev->sensor.work, 0, sizeof(dev->sensor.work));
  dev->sensor.scale = 1.0f;  /* Adjust based on your sensor */
#endif

  /* Initialize base device */
  ret = your_device_init(&dev->base);
  if (ret < 0)
    {
      snerr("Failed to initialize your_device: %d\n", ret);
      goto errout;
    }

  /* Register sensor with the sensor framework */
  ret = sensor_register(lower, devno);
  if (ret < 0)
    {
      snerr("Failed to register your_device: %d\n", ret);
      goto errout;
    }

  return ret;

errout:
  kmm_free(dev);
  return ret;
}

/****************************************************************************
 * Private Functions
 ****************************************************************************/

/****************************************************************************
 * your_device_activate
 ****************************************************************************/

static int your_device_activate(FAR struct sensor_lowerhalf_s *lower,
                                FAR struct file *filep, bool enable)
{
  FAR struct your_device_sensor_s *sensor = (FAR struct your_device_sensor_s *)lower;
  FAR struct your_device_dev_s *dev = sensor->dev;
  int ret = OK;

  /* Acquire device lock */
  ret = nxmutex_lock(&dev->dev_lock);
  if (ret < 0)
    {
      return ret;
    }

  sensor->enabled = enable;

#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
  if (enable)
    {
      /* Start polling work */
      work_queue(HPWORK, &sensor->work, your_device_worker, sensor, 0);
    }
  else
    {
      /* Stop polling work */
      work_cancel(HPWORK, &sensor->work);
    }
#endif

  nxmutex_unlock(&dev->dev_lock);
  return ret;
}

#ifdef CONFIG_SENSORS_YOUR_DEVICE_POLL
/****************************************************************************
 * your_device_set_interval
 ****************************************************************************/

static int your_device_set_interval(FAR struct sensor_lowerhalf_s *lower,
                                   FAR struct file *filep,
                                   FAR uint32_t *period_us)
{
  FAR struct your_device_sensor_s *sensor = (FAR struct your_device_sensor_s *)lower;

  if (period_us)
    {
      sensor->interval = *period_us;
    }

  return OK;
}

/****************************************************************************
 * your_device_worker
 ****************************************************************************/

static void your_device_worker(FAR void *arg)
{
  FAR struct your_device_sensor_s *sensor = (FAR struct your_device_sensor_s *)arg;
  struct sensor_accel data;
  uint64_t timestamp;
  int ret;

  if (!sensor || !sensor->enabled)
    {
      return;
    }

  timestamp = clock_systime_ticks64();

  /* Acquire device lock */
  ret = nxmutex_lock(&sensor->dev->dev_lock);
  if (ret < 0)
    {
      goto reschedule;
    }

  /* Read sensor data */
  ret = your_device_read_data(sensor->dev, &data);
  if (ret < 0)
    {
      nxmutex_unlock(&sensor->dev->dev_lock);
      goto reschedule;
    }

  /* Update timestamp */
  data.timestamp = timestamp;

  /* Report sensor data to the upper half */
  sensor->lower.push_data(sensor->lower, &data, sizeof(data));

  nxmutex_unlock(&sensor->dev->dev_lock);

reschedule:
  /* Schedule next reading */
  if (sensor->enabled)
    {
      work_queue(HPWORK, &sensor->work, your_device_worker, sensor, 
                 USEC2TICK(sensor->interval));
    }
}
#else
/****************************************************************************
 * your_device_fetch
 ****************************************************************************/

static int your_device_fetch(FAR struct sensor_lowerhalf_s *lower,
                            FAR struct file *filep,
                            FAR char *buffer, size_t buflen)
{
  FAR struct your_device_sensor_s *sensor = (FAR struct your_device_sensor_s *)lower;
  struct sensor_accel data;
  uint64_t timestamp;
  int ret;

  if (buflen < sizeof(struct sensor_accel))
    {
      return -EOVERFLOW;
    }

  timestamp = clock_systime_ticks64();

  /* Acquire device lock */
  ret = nxmutex_lock(&sensor->dev->dev_lock);
  if (ret < 0)
    {
      return ret;
    }

  /* Read sensor data */
  ret = your_device_read_data(sensor->dev, &data);
  if (ret < 0)
    {
      nxmutex_unlock(&sensor->dev->dev_lock);
      return ret;
    }

  /* Update timestamp */
  data.timestamp = timestamp;

  /* Copy data to user buffer */
  memcpy(buffer, &data, sizeof(struct sensor_accel));

  nxmutex_unlock(&sensor->dev->dev_lock);
  return sizeof(struct sensor_accel);
}
#endif

/****************************************************************************
 * your_device_read_data
 ****************************************************************************/

static int your_device_read_data(FAR struct your_device_dev_s *dev,
                                FAR struct sensor_accel *data)
{
  uint8_t buffer[6];
  int ret;

  if (!dev || !data)
    {
      return -EINVAL;
    }

  /* Read accelerometer data registers */
  ret = your_device_readregs(dev, YOUR_DEVICE_REG_DATA, buffer, 6);
  if (ret < 0)
    {
      return ret;
    }

  /* Parse data (adjust based on your sensor's protocol) */
  data->x = ((int16_t)(buffer[0] | (buffer[1] << 8))) * ((FAR struct your_device_sensor_s *)lower)->scale;
  data->y = ((int16_t)(buffer[2] | (buffer[3] << 8))) * ((FAR struct your_device_sensor_s *)lower)->scale;
  data->z = ((int16_t)(buffer[4] | (buffer[5] << 8))) * ((FAR struct your_device_sensor_s *)lower)->scale;
  data->temperature = 25.0f;  /* Add temperature reading if available */

  sninfo("Accel data: x=%.3f, y=%.3f, z=%.3f\n", data->x, data->y, data->z);

  return OK;
}
```

## Build System Files

### 6. Make.defs Integration

Add the following to `drivers/sensors/Make.defs`:

```makefile
# Your sensor driver
ifeq ($(CONFIG_SENSORS_YOUR_DEVICE),y)
  CSRCS += your_device.c your_device_base.c
  ifeq ($(CONFIG_SENSORS_YOUR_DEVICE_UORB),y)
    CSRCS += your_device_uorb.c
  endif
endif
```

### 7. Kconfig Configuration

Add the following to `drivers/sensors/Kconfig`:

```kconfig
#
# For a description of the syntax of this configuration file,
# see the file kconfig-language.txt in the NuttX tools repository.
#

config SENSORS_YOUR_DEVICE
	bool "Your Sensor Device Driver"
	depends on CONFIG_I2C
	---help---
		Enable driver support for your sensor device.

if SENSORS_YOUR_DEVICE

config SENSORS_YOUR_DEVICE_UORB
	bool "Your Device uORB Interface"
	default n
	---help---
		Enable uORB-based sensor interface for your device.

if SENSORS_YOUR_DEVICE_UORB

config SENSORS_YOUR_DEVICE_POLL
	bool "Enables polling sensor data"
	default n
	---help---
		Enables polling of sensor data.

config SENSORS_YOUR_DEVICE_POLL_INTERVAL
	int "Polling interval in microseconds, default 1s"
	depends on SENSORS_YOUR_DEVICE_POLL
	default 1000000
	range 0 4294967295
	---help---
		The interval until a new sensor measurement will be triggered.

endif

config YOUR_DEVICE_I2C_FREQUENCY
	int "Your Device I2C frequency"
	default 400000
	---help---
		I2C frequency used to communicate with your device.

endif
```

## Usage Examples

### Character Device Interface

```c
/* Example usage of character device interface */
#include <nuttx/sensors/your_device.h>
#include <nuttx/i2c/i2c_master.h>

int sensor_example(void)
{
  struct i2c_master_s *i2c;
  char buffer[sizeof(struct your_device_data_s)];
  int fd;

  /* Initialize I2C bus */
  i2c = esp32s3_i2cbus_initialize(0); /* ESP32 example - adjust for your platform */
  if (!i2c)
    {
      printf("Failed to initialize I2C bus\n");
      return -1;
    }

  /* Register your sensor device */
  if (your_device_register("/dev/your_sensor0", i2c) < 0)
    {
      printf("Failed to register sensor device\n");
      return -1;
    }

  /* Open device for reading */
  fd = open("/dev/your_sensor0", O_RDONLY);
  if (fd < 0)
    {
      printf("Failed to open sensor device\n");
      return -1;
    }

  /* Read sensor data */
  while (1)
    {
      ssize_t n = read(fd, buffer, sizeof(buffer));
      if (n == sizeof(buffer))
        {
          struct your_device_data_s *data = (struct your_device_data_s *)buffer;
          printf("Sensor: x=%d, y=%d, z=%d\n", data->x, data->y, data->z);
        }
      
      nxsig_usleep(100000); /* 100ms */
    }

  close(fd);
  return 0;
}
```

### uORB Interface

```c
/* Example usage of uORB interface */
#include <uORB/uORB.h>
#include <sensor/accel.h>  /* Standard accelerometer data structure */
#include <poll.h>

int uorb_sensor_example(void)
{
  struct sensor_accel data;
  int sub_fd;
  struct pollfd fds[1];

  /* Subscribe to accelerometer data topic */
  sub_fd = orb_subscribe_multi(ORB_ID(sensor_accel), 0);
  if (sub_fd < 0)
    {
      printf("Failed to subscribe to accelerometer data\n");
      return -1;
    }

  /* Setup poll for data availability */
  fds[0].fd = sub_fd;
  fds[0].events = POLLIN;

  /* Wait for data updates */
  while (1)
    {
      int ret = poll(fds, 1, 1000); /* 1 second timeout */
      if (ret > 0 && (fds[0].revents & POLLIN))
        {
          /* Copy latest data */
          orb_copy(ORB_ID(sensor_accel), sub_fd, &data);
          printf("uORB Accel: x=%.3f, y=%.3f, z=%.3f, temp=%.1f\n",
                 data.x, data.y, data.z, data.temperature);
        }
      
      if (ret == 0)
        {
          printf("Timeout waiting for sensor data\n");
        }
    }

  close(sub_fd);
  return 0;
}
```

## Code Conventions

### Driver Development Best Practices

1. **Include Structure**
   - Always include `<nuttx/config.h>` first
   - Group standard C headers, then NuttX-specific headers
   - Use alphabetical order within groups

2. **Memory Management**
   - Use `kmm_zalloc()` for driver structure allocation
   - Always check for NULL pointers
   - Free allocated memory in error paths

3. **Thread Safety**
   - Use semaphores for device access synchronization
   - Protect critical sections in I2C operations
   - Handle interruption by signals properly

4. **Error Handling**
   - Always check return values of system calls
   - Use appropriate error codes (-EINVAL, -ENOMEM, etc.)
   - Log errors for debugging with appropriate levels

5. **I2C Communication**
   - Use `I2C_TRANSFER()` for multi-message transactions
   - Handle device address and frequency properly
   - Implement read-modify-write operations correctly

6. **Data Handling**
   - Convert raw sensor values to engineering units
   - Include timestamps for time-sensitive data
   - Validate data ranges and sanity check readings

### Platform Integration

1. **Board Configuration**
   - Configure I2C buses in board-specific files
   - Define pin assignments and peripheral configuration
   - Include driver in system's configuration system

2. **Board Initialization Pattern**
   ```c
   int board_your_device_initialize(int devno, int busno)
   {
     struct i2c_master_s *i2c;
     
     /* Initialize I2C bus */
     i2c = stm32_i2cbus_initialize(busno); /* Adjust for your platform */
     
   #ifdef CONFIG_SENSORS_YOUR_DEVICE_UORB
     return your_device_register_uorb(devno, i2c);
   #else
     char devpath[12];
     snprintf(devpath, sizeof(devpath), "/dev/sensor%d", devno);
     return your_device_register(devpath, i2c);
   #endif
   }
   ```

3. **Testing Strategy**
   - Use character device interface for basic testing
   - Test uORB publish/subscribe functionality
   - Validate data conversion and sensor calibration
   - Test error conditions and recovery scenarios

This guide provides a comprehensive foundation for creating sensor drivers in NuttX, supporting both traditional character device interfaces and modern uORB message-based communication patterns.
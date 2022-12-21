Filename: ADXL345.py
import machine
import utime
import ustruct
import sys
# ADXL345常量
# ADXL345寄存器常量
REG_DEVID = 0x00  #0x00-器件ID寄存器, 用于获得器件ID
REG_POWER_CTL = 0x2D  #0x2D-节电控制寄存器
#0x32-X轴数据0寄存器，0x33-X轴数据1寄存器,...
REG_DATAX0 = 0x32
# 其它常量
DEVID = 0xE5  #0xE5-ADXL345器件ID
SENSITIVITY_2G = 1.0/256    # (g/LSB)
EARTH_GRAVITY = 9.80665     # 重力加速度[m/(s*s)]

# 指定PIO17口线为程控从机片选CS
cs = machine.Pin(17, machine.Pin.OUT)

# 初始化SPI
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))

# 函数定义
def reg_write(spi, cs, reg, data):
    """
    写入字节到指定的寄存器
    """
    msg = bytearray()
    msg.append(0x00|reg)
    msg.append(data)
    cs.value(0)
    spi.write(msg)
    cs.value(1)

def reg_read(spi, cs, reg, nbytes=1):
    """
    从指定的寄存器中读取字节; 如果nbytes>1, 则从连续的寄存器中读取。
    """
    if nbytes < 1:
        return bytearray()
    elif nbytes == 1:
        mb = 0
    else:
        mb = 1
    msg = bytearray()
    msg.append(0x80|(mb<<6)|reg)
    cs.value(0)
    spi.write(msg)
    data = spi.read(nbytes)
    cs.value(1)
    return data

# 主程序
cs.value(1)
reg_read(spi, cs, REG_DEVID)
# 读取器件ID以判断是否能与ADXL345进行SPI通信
data = reg_read(spi, cs, REG_DEVID)

test=bytearray((DEVID,))
if (data != bytearray((DEVID,))):
    print("出错: Pico不能与ADXL345进行SPI通信！")
    sys.exit()
data = reg_read(spi, cs, REG_POWER_CTL)
print(data)
data = int.from_bytes(data, "big")|(1<<3)
reg_write(spi, cs, REG_POWER_CTL, data)
data = reg_read(spi, cs, REG_POWER_CTL)
print(data)
utime.sleep(2.0)
while True:
    data = reg_read(spi, cs, REG_DATAX0, 6)
    acc_x = ustruct.unpack_from("<h", data, 0)[0]
    acc_y = ustruct.unpack_from("<h", data, 2)[0]
    acc_z = ustruct.unpack_from("<h", data, 4)[0]
    acc_x = acc_x * SENSITIVITY_2G * EARTH_GRAVITY
    acc_y = acc_y * SENSITIVITY_2G * EARTH_GRAVITY
    acc_z = acc_z * SENSITIVITY_2G * EARTH_GRAVITY
    print("X=", "{:.2f}".format(acc_x), \
          ", Y=", "{:.2f}".format(acc_y), \
          ", Z=", "{:.2f}".format(acc_z))
    utime.sleep(0.1)

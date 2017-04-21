## Sensor Nodes with NUCLEO-L053R8 Powered by FreeRTOS

### STM32 toolchain

#### STLINK

Setting up a GCC/Eclipse toolchain for STM32Nucleo [here](http://www.carminenoviello.com/2014/12/28/setting-gcceclipse-toolchain-stm32nucleo-part-1/)     
stlink linux driver [here](https://github.com/texane/stlink)   
The J-Link debugging Eclipse plug-in [here](http://gnuarmeclipse.github.io/debug/jlink/)   
Tutorial: Using Eclipse + ST-LINK/v2 + OpenOCD to debug [here](https://community.particle.io/t/tutorial-using-eclipse-st-link-v2-openocd-to-debug/10042)   
How to install the OpenOCD binaries [here](http://gnuarmeclipse.github.io/openocd/install/)   

STM32F0Discovery Under Linux Tutorial Part 1 – Setting up the GCC ARM Toolchain, OpenOCD and stlink [here](http://www.hertaville.com/stm32f0discovery-part-1-linux.html)   
   
(work)   
The GNU ARM Eclipse plug-ins [here](https://github.com/gnuarmeclipse/plug-ins)
openocd + st-link setup [here](https://github.com/LieBtrau/Aiakos/wiki/STM32L053-Nucleo-toolchain-setup)   
gnuarmeclipse/openocd/releases [here](https://github.com/gnuarmeclipse/openocd/releases)   
mbed-os [here](https://github.com/ARMmbed/mbed-os)   
mbed_NucleoL053R8 [here](https://github.com/Hotboards/mbed_NucleoL053R8)   
GNU ARM Embedded Toolchain [here](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads)   


Nucleo Boards [here](http://wiki.robolabo.etsit.upm.es/index.php/Nucleo_Boards)   



ST LINK Under linux problems
For info the original ST-LINK enumerates using the mass storage usb class; however, its
implementation is completely broken. The result is this causes issues under Linux. The
simplest solution is to get Linux to ignore the ST-LINK using one of the following methods:
- modprobe -r usb-storage && modprobe usb-storage quirks=483:3744:i
- add "options usb-storage quirks=483:3744:i" to /etc/modprobe.conf   

http://www.simplymodbus.ca/FC03.htm

MODBOS ASCII Mode

Request   11  03   00 6B    00 03
          id CMD  startArr  length

Response  11 03    06     AE41 5652 4340  49AD
          id CMD length   |-- value  --|  CRC

ASCII Mode

11  03  00 6B 00 03 ========> 17 3 0 107 0 3
                     decimal

sum              = 130 (0x82)
two's complement = -130 (0x7E) ====> 7E
                                LRC

Compleat ASCII request
: 1 1  0 3  0 0  6 B  0 0  0 3  7 E  CR LF  (ASCII)
or
3A 3131 3033 3030 3642 3030 3033 3745 0D 0A (raw value)


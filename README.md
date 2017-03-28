# temp

1. Install JDK
```sh
sudo apt-get install default-jdk
```

2. Installl Eclipse Neon 3 (download [here](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads)) using C/C++ for default workspace.   
   
3. Install the GNU ARM plug-ins for Eclipse (via Eclipse Marketplace [here](https://marketplace.eclipse.org/content/gnu-arm-eclipse))   

4. Install GCC for ARM here (here)[https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads]   

5. Setup openOCD v0.10.0, Use pre-build binary from [here](https://github.com/gnuarmeclipse/openocd/releases)   
Test and make sure you can connect to gdb server on STM32 board via openOCD!!!   

6. Setup Eclipse + GCC + FreeRTOS for STM32
https://sourceforge.net/projects/freertos/?source=typ_redirect   
https://www.embarcados.com.br/gnu-arm-cross-toolchain-eclipse-freertos-gcc-parte-1/   
http://www.carminenoviello.com/2015/06/22/running-freertos-stm32nucleo-free-gcceclipse-toolchain/   



### Line bot
https://github.com/line/line-bot-sdk-python
https://kittinanx.blogspot.com/2016/10/line-bot.html
https://huamong.blogspot.com/2015/07/line-bot.html
http://line-bot-sdk-python.readthedocs.io/en/latest/

### firebase
http://deanhume.com/home/blogpost/a-basic-guide-to-firebase-for-the-web/10142
https://react.rocks/tag/Firebase
https://www.airpair.com/firebase/posts/firebase-building-realtime-app

### PYTHON+REST
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
https://realpython.com/blog/python/api-integration-in-python/
http://python-eve.org/

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



 


# temp

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
Update ST Link firmware [here](http://www.st.com/en/embedded-software/stsw-link007.html)   
stlink linux driver [here](https://github.com/texane/stlink)   
The J-Link debugging Eclipse plug-in [here](http://gnuarmeclipse.github.io/debug/jlink/)   
Tutorial: Using Eclipse + ST-LINK/v2 + OpenOCD to debug [here](https://community.particle.io/t/tutorial-using-eclipse-st-link-v2-openocd-to-debug/10042)   
How to install the OpenOCD binaries [here](http://gnuarmeclipse.github.io/openocd/install/)   
gnuarmeclipse/openocd/releases [here](https://github.com/gnuarmeclipse/openocd/releases)   
STM32F0Discovery Under Linux Tutorial Part 1 – Setting up the GCC ARM Toolchain, OpenOCD and stlink [here](http://www.hertaville.com/stm32f0discovery-part-1-linux.html)   

https://github.com/LieBtrau/Aiakos/wiki/STM32L053-Nucleo-toolchain-setup   
http://wiki.robolabo.etsit.upm.es/index.php/Nucleo_Boards   



ST LINK Under linux problems
For info the original ST-LINK enumerates using the mass storage usb class; however, its
implementation is completely broken. The result is this causes issues under Linux. The
simplest solution is to get Linux to ignore the ST-LINK using one of the following methods:
- modprobe -r usb-storage && modprobe usb-storage quirks=483:3744:i
- add "options usb-storage quirks=483:3744:i" to /etc/modprobe.conf  



 


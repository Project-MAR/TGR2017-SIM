## System Overview
![alt tag](https://github.com/Project-MAR/TGR2017-SIM/blob/master/img/overallSystem.png)
   
This Project try to build an IoT System for Smart Farm. This system use STM32 as an IoT node  for control the water pump, measure temperature, humidity, soil moisture and communicate with the server using ModBus Protocol. A Raspberry Pi Board act as a local server. It control a watering time, taking a picture and communicate with Cloud Server using REST API. A Cloud Server act as a center of the communication between a local server and LINE Server. Users can interact with the system such as monitor the operation of the system or get a picture from a local server via LINE Application.
---

### 01-python-REST   
   
 This folder provide a basic example for RESTful API with python-2.7. Two important module for learning are   
    
    - [Flask](http://flask.pocoo.org/): A microframework for web development.   
    - [requests](http://docs.python-requests.org/en/master/): Non-GMO HTTP library for Python.   
  
---

### 02-HEROKU-LINEBOT   
   
 This folder provide server codes and config files for HEROKU Clond Platform. I recommend you to go thought a toturial first if you don't familar with this platform. Importain module for this section are   
   
   - [Django](https://www.djangoproject.com/): A python base web framework.
   - [PostgreSQL](https://www.postgresql.org/): A database we will use later.
   - [LINE API](https://developers.line.me/): Use Python base Line Messageing API.
   
---
   
### 03-STM32L053-IOTClient   

 This folder contain template code and project workspace for STM32L053R8 Nucleo Board. This is a hardest part (I think) because I try to use Eclipse + GCC + OpenOCD to build the system. If you dont't want to go deeper, you can use [SW4STM32](http://www.openstm32.org/HomePage) (System Workbench for STM32) instead. It also an Eclipse + GCC + OpenOCD base, ready to use, development platform for STM32.   
 
---

### 04-RPi-Software
   This folder contain a local server code (on Raspberry Pi 2 Model B). this local server use for bridge incommong/outgoing message between HEROKU and STM32.
   
---
   

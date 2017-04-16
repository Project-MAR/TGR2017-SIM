## Sensor Nodes with NUCLEO-L053R8 Powered by FreeRTOS

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


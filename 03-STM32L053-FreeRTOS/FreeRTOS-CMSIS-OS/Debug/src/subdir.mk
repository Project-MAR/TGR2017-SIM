################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/freertos.c \
../src/main.c \
../src/stm32l0xx_hal_msp.c \
../src/stm32l0xx_it.c 

OBJS += \
./src/freertos.o \
./src/main.o \
./src/stm32l0xx_hal_msp.o \
./src/stm32l0xx_it.o 

C_DEPS += \
./src/freertos.d \
./src/main.d \
./src/stm32l0xx_hal_msp.d \
./src/stm32l0xx_it.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0plus -mthumb -O0 -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -ffreestanding -fno-move-loop-invariants  -g3 -DDEBUG -DTRACE -I"../include" -I"../system/include" -I"../system/include/arm" -I"../system/include/cmsis" -I"../system/include/cortexm" -I"../system/include/diag" -I"../system/include/stm32l0xx" -I"../system/include/FreeRTOS" -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



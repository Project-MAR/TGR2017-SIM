/**
  ******************************************************************************
  * @file    UART/UART_TwoBoards_ComIT/Src/main.c
  * @author  MCD Application Team
  * @version V1.8.0
  * @date    25-November-2016
  * @brief   This sample code shows how to use STM32L0xx UART HAL API to transmit
  *          and receive a data buffer with a communication process based on
  *          IT transfer.
  *          The communication is done using 2 Boards.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; COPYRIGHT(c) 2016 STMicroelectronics</center></h2>
  *
  * Redistribution and use in source and binary forms, with or without modification,
  * are permitted provided that the following conditions are met:
  *   1. Redistributions of source code must retain the above copyright notice,
  *      this list of conditions and the following disclaimer.
  *   2. Redistributions in binary form must reproduce the above copyright notice,
  *      this list of conditions and the following disclaimer in the documentation
  *      and/or other materials provided with the distribution.
  *   3. Neither the name of STMicroelectronics nor the names of its contributors
  *      may be used to endorse or promote products derived from this software
  *      without specific prior written permission.
  *
  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/** @addtogroup STM32L0xx_HAL_Examples
  * @{
  */

/** @addtogroup UART_TwoBoards_ComIT
  * @{
  */

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/

/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

/* UART handler declaration */
UART_HandleTypeDef UartHandle;

/* Flag */
__IO ITStatus UartRXReady = RESET;
__IO ITStatus UartTXReady = RESET;
__IO ITStatus TIM1 = RESET;

/* Buffer used for transmission */
uint8_t aTxBuffer[TXBUFFERSIZE];

/* Buffer used for reception */
//uint8_t aRxBuffer[RXBUFFERSIZE];
uint8_t aRxBuffer[RXBUFFERSIZE];
uint8_t EmptyRxBuffer[RXBUFFERSIZE];

/* RaspberryPi message */
RPiMessage RpiMSG;

/* Sensor Value and Sensor Configulation  */
uint32_t SensorValueArray[10];
uint16_t SensorConfigArray[10][10];

/* TIM handle declaration */
TIM_HandleTypeDef    TimHandle;

/* Prescaler declaration */
uint32_t uwPrescalerValue = 0;
uint32_t timeCount = 0;

/* Private function prototypes -----------------------------------------------*/
static void SystemClock_Config(void);
static void Error_Handler(void);
static void MX_GPIO_Init(void);
static uint16_t Buffercmp(uint8_t* pBuffer1, uint8_t* pBuffer2, uint16_t BufferLength);

uint8_t LRCCheck(RPiMessage *RpiMSG);
void ProcessCMD(RPiMessage *RpiMSG);

/* Private functions ---------------------------------------------------------*/

/**
  * @brief  Main program.
  * @param  None
  * @retval None
  */
int main(void)
{

  uint8_t i, u, sum;
  uint8_t tempChar[2];

  HAL_Init();
  MX_GPIO_Init();

  /* Configure the system clock to 32 Mhz */
  SystemClock_Config();

  /* Compute the prescaler value to have TIMx counter clock equal to 10 KHz */
  uwPrescalerValue = (uint32_t) ((SystemCoreClock / 10000) - 1);

  /* Set TIMx instance */
  TimHandle.Instance = TIMx;

   /** Initialize TIMx peripheral as follow:
   *   + Period = 10000 - 1
   *   + Prescaler = SystemCoreClock/10000 Note that APB clock = TIMx clock if
   *				 APB prescaler = 1.
   *   + ClockDivision = 0
   *   + Counter direction = Up
   */
  TimHandle.Init.Period = 10000 - 1;
  TimHandle.Init.Prescaler = uwPrescalerValue;
  TimHandle.Init.ClockDivision = 0;
  TimHandle.Init.CounterMode = TIM_COUNTERMODE_UP;

  if(HAL_TIM_Base_Init(&TimHandle) != HAL_OK)
  {
	 Error_Handler();
  }

  /* Start Channel1 */
  if(HAL_TIM_Base_Start_IT(&TimHandle) != HAL_OK)
  {
	 Error_Handler();
  }

  UartHandle.Instance        = USARTx;
  UartHandle.Init.BaudRate   = 115200;
  UartHandle.Init.WordLength = UART_WORDLENGTH_8B;
  UartHandle.Init.StopBits   = UART_STOPBITS_1;
  UartHandle.Init.Parity     = UART_PARITY_NONE;
  UartHandle.Init.HwFlowCtl  = UART_HWCONTROL_NONE;
  UartHandle.Init.Mode       = UART_MODE_TX_RX;

  if(HAL_UART_Init(&UartHandle) != HAL_OK)
  {
    Error_Handler();
  }

  if(HAL_UART_Receive_IT(&UartHandle, (uint8_t *)aRxBuffer, RXBUFFERSIZE) != HAL_OK)
  {
	Error_Handler();
  }

  // Dummy Value for test
  SensorValueArray[0] = 0  ; SensorValueArray[5] = 150876;
  SensorValueArray[1] = 1  ; SensorValueArray[6] = 45678;
  SensorValueArray[2] = 7  ; SensorValueArray[7] = 1955922247;
  SensorValueArray[3] = 14 ; SensorValueArray[8] = 0xFFFFFFFF;
  SensorValueArray[4] = 100; SensorValueArray[9] = 634222654;

  while (1)
  {
	  // Process Incoming message -----------------------------------------------------
	  if (UartRXReady == SET)
	  {
		  UartRXReady = RESET;

		  // Begin Process Command from RPi
		  // 1. Convert STR-CMD to INT-CMD
		  u = 0;
		  RpiMSG.msg[u] = ':';
		  for(i = 1; i < RXBUFFERSIZE - 3; i+=2)
		  {
			  tempChar[0] = aRxBuffer[i];
			  tempChar[1] = aRxBuffer[i+1];
			  u++;
			  sum = (int)strtol(tempChar, NULL, 16);
			  RpiMSG.msg[u] = sum;
		  }

		  RpiMSG.len = u + 3;
		  RpiMSG.msg[u+1] = '\r';
		  RpiMSG.msg[u+2] = '\n';

		  // 2. Do a Basic Check
		  if(RpiMSG.msg[0] == ':')
			  if(LRCCheck(&RpiMSG) == TRUE)
				  if(RpiMSG.msg[1] == BoardID)
					  ProcessCMD(&RpiMSG);

		  if(HAL_UART_Receive_IT(&UartHandle, (uint8_t *)aRxBuffer, RXBUFFERSIZE) != HAL_OK)
		  {
			  Error_Handler();
		  }
	  }

	  // Send Message to RPi ----------------------------------------------------------
	  if(UartTXReady == SET)
	  {
 		  UartTXReady = RESET;

		  if(HAL_UART_Transmit_IT(&UartHandle, (uint8_t*)aTxBuffer, TXBUFFERSIZE)!= HAL_OK)
		  {
		    Error_Handler();
		  }

		  while (UartTXReady != SET)
		  {
		  }

		  UartTXReady = RESET;
	  }

	  // 1 Second Timer ---------------------------------------------------------------
	  if(TIM1 == SET)
	  {
		  TIM1 = RESET;
		  HAL_GPIO_TogglePin(LD2_GPIO_Port, LD2_Pin);
		  timeCount++;
		  if(timeCount >= 5)
		  {
			  timeCount=0;
			  //strcpy(aTxBuffer, EmptyRxBuffer);
			  strcpy(aTxBuffer, "Report Something to RPi......\r\n");
			  UartTXReady = SET;
		  }
	  }
  }
}


void ProcessCMD(RPiMessage *RpiMSG)
{
	/*   ------------------------------- Command Pattern ------------------------------------
	 *   index       0    1    2      3                  4-13                14   15  16
	 *  Request:     :    01   01     00      01 02 03 04 05 06 07 08 09 10  5E   0D  0A
     *  Meaning:   START  id  CMD   Legnth    |----------payload----------|  LRC  \r  \n
     *  Note:                      [MAX==10]
     *
     *   index
     *   Response:    :    01   01     00       01 02 03 04 05 06 07 08 09 10    5E   0D  0A
     *   Meaning:   START  id  CMD   Legnth     |----------payload----------|    LRC  \r  \n
     *    Note:                     [MAX==10]  Sensor Number follow by its value
     *
     *  Example
     *   - Read Sensor1
     *       Request:    : 01 01 01 04 00 00 00 00 00 00 00 00 00 xx 0D 0A
     *       Meaning: GET Value From Sensor Number 4
     *
     *       Response    : 01 01 0A 04 00 00 00 00 00 00 02 4D 5C xx 0D 0A
     *       Meaning: Value From Sensor Number 4 is 0x024D5C
     *       Note: Sensor Value = 1508.76 =>> 150876 == 0x024D5C
	 * */

	uint8_t i, sensorNumber;
	uint32_t sensorValue;
    uint8_t intToChar[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
    uint8_t sensorValueSegment;

	if(RpiMSG->msg[2] == CMD_GET)
	{
		/*
		* TODO: - GET multiple Sensor Value in single command
		* */
		sensorNumber = RpiMSG->msg[4];
		sensorValue = SensorValueArray[sensorNumber];

		//memset(aTxBuffer, '\0', TXBUFFERSIZE);

		// Sensor value is int32
		// It use 4 byte to transmit
		aTxBuffer[0] = ':';

		aTxBuffer[1] = intToChar[(BoardID & 0xF0) << 4];
		aTxBuffer[2] = intToChar[BoardID & 0x0F];

		aTxBuffer[3] = intToChar[(CMD_GET & 0xF0) << 4];
		aTxBuffer[4] = intToChar[CMD_GET & 0x0F];

		/*
		* TODO: - Calculate for a Real Length
		* */
		aTxBuffer[5] = '0';
		aTxBuffer[6] = 'A';

		// Client ID
		aTxBuffer[7] = intToChar[(sensorNumber & 0xF0) << 4];
		aTxBuffer[8] = intToChar[sensorNumber & 0x0F];

		//byte 9-26 are payloads (total 18 bytes)
		// 00 00 00 00 00 00 00 00 00
		for (i = 26; i >= 9; i--)
		{
			sensorValueSegment    = sensorValue & 0xF;
			sensorValue = sensorValue >> 4;
			aTxBuffer[i] = intToChar[sensorValueSegment];
		}
		UartTXReady = SET;

		/*
		 * TODO: Calculate LRC
		 * */
		aTxBuffer[27] = '5';
		aTxBuffer[28] = '5';

		aTxBuffer[29] = '\r';
		aTxBuffer[30] = '\n';

		// SET TX Flag
		UartTXReady = SET;
	}
	else if (RpiMSG->msg[2] == CMD_SET)
	{
		/*   ------------------------------- Command Pattern ------------------------------------
		 *   index       0    1    2      3                  4-13                14   15  16
		 *  Request:     :    01   02     00      01 02 03 04 05 06 07 08 09 10  5E   0D  0A
	     *  Meaning:   START  id  CMD   Legnth    |----------payload----------|  LRC  \r  \n
	     *  Note:                      [MAX==10]
	     *
	     *   index
	     *   Response:    :    01   02     00       01 02 03 04 05 06 07 08 09 10    5E   0D  0A
	     *   Meaning:   START  id  CMD   Legnth     |----------payload----------|    LRC  \r  \n
	     *    Note:                     [MAX==10]  Sensor Number follow by its value
	     *
	     *  Example
	     *   - Read Sensor1
	     *       Request:    : 01 02 0A 01 02 00 00 00 00 00 00 00 03 xx 0D 0A
	     *       Meaning: SET Sensor 1, Parameter 2, to 3
	     *
	     *       Response    : 01 02 0A 01 02 00 00 00 00 00 00 00 03 xx 0D 0A
	     *       Meaning: Repeat SET Command
		 * */

		uint8_t i;
		uint8_t SensorNumber;
		uint8_t SensorParamNum;
		uint16_t SensorConfigValue;

		SensorNumber      = RpiMSG->msg[4];
		SensorParamNum    = RpiMSG->msg[5];
		SensorConfigValue = 0;

		// byte 6-13 contain SensorConfigValue
		SensorConfigValue = RpiMSG->msg[6];
		for(i = 7; i<= 13; i++)
		{
			SensorConfigValue <<= 8;
			SensorConfigValue |= RpiMSG->msg[i];
		}

		SensorConfigArray[SensorNumber][SensorParamNum] = SensorConfigValue;

		//memset(aTxBuffer, '\0', TXBUFFERSIZE);
		strcpy(aTxBuffer, aRxBuffer);
		UartTXReady = SET;
	}
}

uint8_t LRCCheck(RPiMessage *RpiMSG)
{

	/*
	 * TODO: Implement LRC Check
	 * */
	return TRUE;
}


/**
  * @brief  System Clock Configuration
  *         The system Clock is configured as follow :
  *            System Clock source            = PLL (HSI)
  *            SYSCLK(Hz)                     = 32000000
  *            HCLK(Hz)                       = 32000000
  *            AHB Prescaler                  = 1
  *            APB1 Prescaler                 = 1
  *            APB2 Prescaler                 = 1
  *            HSI Frequency(Hz)              = 16000000
  *            PLL_MUL                        = 4
  *            PLL_DIV                        = 2
  *            Flash Latency(WS)              = 1
  *            Main regulator output voltage  = Scale1 mode
  * @param  None
  * @retval None
  */
static void SystemClock_Config(void)
{
  RCC_ClkInitTypeDef RCC_ClkInitStruct;
  RCC_OscInitTypeDef RCC_OscInitStruct;

  /* Enable Power Control clock */
  __HAL_RCC_PWR_CLK_ENABLE();

  /* The voltage scaling allows optimizing the power consumption when the device is
     clocked below the maximum system frequency, to update the voltage scaling value
     regarding system frequency refer to product datasheet.  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /* Enable HSI Oscillator and activate PLL with HSI as source */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSEState = RCC_HSE_OFF;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL4;
  RCC_OscInitStruct.PLL.PLLDIV = RCC_PLL_DIV2;
  RCC_OscInitStruct.HSICalibrationValue = 0x10;
  HAL_RCC_OscConfig(&RCC_OscInitStruct);

  /* Select PLL as system clock source and configure the HCLK, PCLK1 and PCLK2
     clocks dividers */
  RCC_ClkInitStruct.ClockType = (RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2);
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
  HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_1);
}


static void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct;

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

}


/**
  * @brief  Tx Transfer completed callback
  * @param  UartHandle: UART handle.
  * @note   This example shows a simple way to report end of IT Tx transfer, and
  *         you can add your own implementation.
  * @retval None
  */
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *UartHandle)
{
  /* Set transmission flag: trasfer complete*/
  UartTXReady = SET;
}


/**
  * @brief  Rx Transfer completed callback
  * @param  UartHandle: UART handle
  * @note   This example shows a simple way to report end of IT Rx transfer, and
  *         you can add your own implementation.
  * @retval None
  */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *UartHandle)
{
  /* Set transmission flag: trasfer complete*/
  UartRXReady = SET;
}


/**
  * @brief  Period elapsed callback in non blocking mode
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* Toggle LED2 */
  TIM1 = SET;
}


/**
  * @brief  Compares two buffers.
  * @param  pBuffer1, pBuffer2: buffers to be compared.
  * @param  BufferLength: buffer's length
  * @retval 0  : pBuffer1 identical to pBuffer2
  *         >0 : pBuffer1 differs from pBuffer2
  */
static uint16_t Buffercmp(uint8_t* pBuffer1, uint8_t* pBuffer2, uint16_t BufferLength)
{
  while (BufferLength--)
  {
    if ((*pBuffer1) != *pBuffer2)
    {
      return BufferLength;
    }
    pBuffer1++;
    pBuffer2++;
  }

  return 0;
}


/**
  * @brief  UART error callbacks
  * @param  UartHandle: UART handle
  * @note   This example shows a simple way to report transfer error, and you can
  *         add your own implementation.
  * @retval None
  */
 void HAL_UART_ErrorCallback(UART_HandleTypeDef *UartHandle)
{
    while(1)
    {
    }
}


/**
  * @brief  This function is executed in case of error occurrence.
  * @param  None
  * @retval None
  */
static void Error_Handler(void)
{
    while(1)
    {
    }
}


#ifdef  USE_FULL_ASSERT

/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */

  /* Infinite loop */
  while (1)
  {
  }
}
#endif


/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/

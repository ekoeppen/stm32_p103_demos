/* vim: set expandtab ts=4 sw=4 */

#define USE_STDPERIPH_DRIVER
#include "stm32f10x.h"
#include "stm32_p103.h"

#define ARRAY_COUNT(a) (sizeof(a) / sizeof(a[0]))

void send_byte(uint8_t b)
{
    /* Send one byte */
    USART_SendData(USART2, b);

    /* Loop until USART2 DR register is empty */
    while(USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET);
}

void send_string(uint8_t *string)
{
    while (*string != 0) {
        send_byte(*string++);
    }
}

void send_hex(uint32_t n)
{
    uint8_t c;
    int i;

    for (i = 0; i < 8; i++) {
        c = (n >> 28);
        send_byte(c + (c > 9 ? 'a' - 10 : '0'));
        n <<= 4;
    }
}

void delay(uint32_t n)
{
    while (n--) ;
}

uint32_t samples[32];
uint32_t samples_count;

void SysTick_Handler(void)
{
    samples[samples_count++] = 0x10000000;
}

int main(void)
{
    int input_state, old_state = 0;
    int i;
    uint32_t t, t0;

    init_led();
    init_button();
    init_rs232();
    USART_Cmd(USART2, ENABLE);
   
    SysTick->LOAD = 0x00ffffff;
    SysTick->VAL = 0;
    SysTick->CTRL = SysTick_CTRL_ENABLE_Msk | SysTick_CTRL_CLKSOURCE_Msk | SysTick_CTRL_TICKINT_Msk;

    while (1) {
        send_string("Ready.\r\n");
        for (samples_count = 0; samples_count < ARRAY_COUNT(samples);  ) {
            input_state = (GPIOC->IDR & 0x00000100) << 16;
            if (GPIOA->IDR & 0x00000001) break;
            if (input_state ^ old_state) {
                samples[samples_count++] = SysTick->VAL | input_state;
                old_state = input_state;
            }
        }
        send_string("Done.\r\n");
        for (t0 = 0, i = 0; i < samples_count; i++) {
            send_hex((samples[i] & 0xff000000) >> 24);
            send_byte(' ');
            if (samples[i] & 0x10000000) {
                send_hex(0x10000000);
            } else {
                t = SysTick->LOAD - (samples[i] & 0x00ffffff);
                send_hex(t);
                send_byte(' ');
                send_hex(t - t0);
                t0 = t;
            }
            send_string("\r\n");
        }
    }
}

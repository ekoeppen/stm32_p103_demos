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

int main(void)
{
    int input_state, old_state = 0;
    int i;
    uint32_t t, t0;

    init_led();
    init_button();
    init_rs232();
    USART_Cmd(USART2, ENABLE);

    while (1) {
        send_string("START\r\n");
        samples_count = sampler(samples, ARRAY_COUNT(samples));
        send_string("STOP\r\n");
        for (t0 = 0, i = 0; i < samples_count; i++) {
            send_hex(samples[i]);
            send_string("\r\n");
        }
    }
}

#define USE_STDPERIPH_DRIVER
#include "stm32f10x.h"
#include "stm32_p103.h"

#define ARRAY_COUNT(a) (sizeof(a) / sizeof(a[0]))

void send_byte(uint8_t b)
{
    USART_SendData(USART2, b);
    while(USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET);
}

uint8_t read_byte(void)
{
    while(USART_GetFlagStatus(USART2, USART_FLAG_RXNE) == RESET);
    return USART_ReceiveData(USART2);
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

uint32_t read_long(void)
{
    return read_byte() + (read_byte() << 8) + (read_byte() << 16) + (read_byte() << 24);
}

void delay(uint32_t n)
{
    while (n--) ;
}

uint32_t samples[1024];
uint32_t samples_count;

void start_sampling(void)
{
    samples_count = sampler(samples, ARRAY_COUNT(samples));
    send_samples();
}

void send_samples(void)
{
    int i, j, b;
    uint32_t sample, last_sample;
    uint32_t t, sample_t;
    uint32_t timer;

    t = 0;
    timer = 0;
    for (i = 0; i < ARRAY_COUNT(samples); i++) {
        sample = samples[i];

        if (sample & 0x80000000) {
            timer++;
        } else {
            sample_t = ((0x01000000 - (sample & 0x00ffffff)) / 72) + timer * 0x01000000;

            while (t < sample_t) {
                send_byte((last_sample >> 24) & 0x7f);
                t++;
            }
            send_byte((sample >> 24) & 0x7f);
            last_sample = sample;
        }
    }
}

void sump_handler(void)
{
    uint8_t command;

    while (1) {
        command = read_byte();
        switch (command) {
        case 0x00: break;
        case 0x01: start_sampling(); break;
        case 0x02: send_string("1ALS"); break;
        case 0x11: break;
        case 0x13: break;
        case 0xc0:
        case 0xc4:
        case 0xc8:
        case 0xcc: read_long(); break;
        case 0xc1:
        case 0xc5:
        case 0xc9:
        case 0xcd: read_long(); break;
        case 0xc2:
        case 0xc6:
        case 0xca:
        case 0xce: read_long(); break;
        case 0x80: read_long(); break;
        case 0x81: read_long(); break;
        case 0x82: read_long(); break;
        }
    }
}

int main(void)
{
    int input_state, old_state = 0;
    int i;
    uint32_t t, t0;

    init_led();
    init_button();
    init_rs232();
    enable_rs232();
    sump_handler();
}

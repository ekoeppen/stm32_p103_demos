        .syntax unified

        .global sampler
sampler:
        mov r4, r0
        mov r9, r0
        mov r10, r1
        mov r7, #0
        ldr r1, =0x40011008     @ GPIOC->IDR
        ldr r2, =0x40010808     @ GPIOA->IDR
        ldr r3, =0xe000e018     @ STCURRENT

sample_loop:
        ldr r5, [r1]
        and r5, #0x7f
        teq r7, r5
        beq sample_loop
        mov r7, r5
        lsl r5, #24
        ldr r6, [r3]
        orr r6, r5
        str r6, [r9], #4
        sub r0, r9, r4
        lsr r0, #2
        cmp r0, r10
        blt sample_loop

        mov pc, lr

        .global SysTick_Handler
SysTick_Handler:
        ldr r0, [r3]
        mov r1, #1
        ror r1, #1
        and r0, r1
        str r0, [r9], #4
        mov pc, lr

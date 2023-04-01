//
// Created by victo on 01/04/2023.
//

#include "common.h"
#include "mini_uart.h"

_Noreturn void kernel_main(){
    uart_init();
    uart_send_string("RISC-V Single Cycle Emulator on BCM2837\n");
    uart_send_string("by Victor Alicino\n");

#if RPI_VERSION == 3
    uart_send_string("Running on Raspberry Pi 3\n");
#elif RPI_VERSION == 4
    uart_send_string("Running on Raspberry Pi 4\n");
#endif

    while(1){
        uart_send(uart_recv());
    }
}
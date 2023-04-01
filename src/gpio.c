//
// Created by victo on 01/04/2023.
//

#include "gpio.h"
#include "utils.h"

void gpio_pin_set_func(uint8_t pin, GpioFunc func){
    uint8_t bit_start = (pin * 3) % 30;
    uint8_t reg = pin / 10;

    uint32_t selector = REGS_GPIO->func_select[reg];
    selector &= ~(0b111 << bit_start);
    selector |= (func << bit_start);

    REGS_GPIO->func_select[reg] = selector;
}

void gpio_pin_enable(uint8_t pin){
    REGS_GPIO->pupd_enable = 0;
    delay(150);
    REGS_GPIO->pupd_enable_clocks[pin / 32] = 1 << (pin % 32);
    delay(150);
    REGS_GPIO->pupd_enable = 0;
    REGS_GPIO->pupd_enable_clocks[pin / 32] = 0;
}
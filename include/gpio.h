//
// Created by victo on 01/04/2023.
//

#pragma once

#include "peripherals/gpio.h"

typedef enum _GpioFunc{
    GFI_INPUT = 0,
    GFI_OUTPUT = 1,
    GFI_ALT0 = 4,
    GFI_ALT1 = 5,
    GFI_ALT2 = 6,
    GFI_ALT3 = 7,
    GFI_ALT4 = 3,
    GFI_ALT5 = 2
} GpioFunc;

void gpio_pin_set_func(uint8_t pin, GpioFunc func);

void gpio_pin_enable(uint8_t pin);
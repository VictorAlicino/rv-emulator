//
// Created by victo on 01/04/2023.
//

#pragma once

#include "common.h"

void delay(uint64_t ticks);
void put32(uint64_t addr, uint32_t value);
uint32_t get32(uint64_t addr);

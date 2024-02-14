"""Implementation of a Risc-V Single Cycle CPU simulator."""

import logging
from typing import IO
from rv_units.control_unit import ControlUnit
from rv_units.register_bank import RegisterBank


class RiscV:
    """This class represents a Risc-V Single Cycle CPU simulator."""
    def __init__(self):
        self._prog_mem: dict = {} # This is a dictionary of instructions

        # Data Memory (RAM) on binary file
        self._data_mem: IO[bytes] = open('data_memory.bin', 'wb')

        self._control: ControlUnit = ControlUnit()
        self._registers: RegisterBank = RegisterBank()

    def __del__(self):
        self._data_mem.close()

    def pc_value(self) -> int:
        """Returns the current value of the program counter register"""
        return self._registers.pc.to_int()

    def dump_memory(self):
        """Dump the memory to the console"""
        for addr, instruction in self._prog_mem.items():
            print(f'0x{addr} {instruction}')

    def load_program(self, file_name):
        """Load the program from a file"""
        # Test if the file is empty
        if file_name == '':
            raise ValueError('Program path was not provided')
        logging.debug('Loading memory from %s', file_name)
        with open(file_name, encoding='utf-8') as f:
            temp_last_addr = 0
            for i, line in enumerate(f):
                if line == "\n":
                    continue
                if i == 0:
                    addr = format(i, '02x')
                else:
                    temp_last_addr = temp_last_addr + 4
                    addr = format(temp_last_addr, '02x')
                self._prog_mem.update({addr: line.rstrip()})
        logging.debug('Loaded %d instructions', len(self._prog_mem))

    def instruction_at_address(self, address: int):
        """Returns the instruction at the given address"""
        hex_addr = format(address, '02x')
        try:
            return self._prog_mem[hex_addr]
        except KeyError:
            return None

    def cycle(self) -> bool:
        """This is the main loop of the CPU"""
        # This code mimics the Risc-V Single Cycle Data Path


        # From the PC we get 3 lines on the data path:
        # One line goes to PC+4;
        # another goes to the branch mux;
        # and the last one goes to the instruction memory.
        curr_addr: int = self.pc_value()
        pc_add: bytearray = (curr_addr + 4).to_bytes(4, byteorder='big')

        # The output of the instruction memory is the line
        # which is pointed by the PC, its 32 bits will
        # feed other 4 lines on the data path.

        try:
            instruction: str = self._prog_mem[format(self.pc_value(), '02x')]
        except KeyError:
            logging.debug('[CPU] Instruction not found at address %s', hex(curr_addr))
            logging.debug('[CPU] Halting...\n')
            return False

        # -----Instruction Decode-----

        logging.debug('[CPU] Instruction at %s: %s', curr_addr, instruction)

        # The first 7 bits of the instruction are the opcode
        # which will be used to set the control signals.

        # Decoding the Opcode
        opcode: int = int(instruction[25:32], 2)
        self._control.set_opcode(opcode)

        self._registers.pc.write(pc_add)
        print(self._control)
        return True

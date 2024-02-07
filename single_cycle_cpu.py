"""Implementation of a Risc-V Single Cycle CPU simulator."""

import logging
from rv_units.control_unit import ControlUnit
from rv_units.register_bank import RegisterBank


class RiscV:
    """This class represents a Risc-V Single Cycle CPU simulator."""
    def __init__(self):
        self._prog_mem: dict = {} # This is a dictionary of instructions

        self._control: ControlUnit = ControlUnit()
        self._registers: RegisterBank = RegisterBank()

    def pc_value(self, to_int: bool = False) -> int:
        """Returns the current value of the program counter register"""
        return self._registers.pc.to_int() if to_int else self._registers.pc

    def dump_memory(self):
        """Dump the memory to the console"""
        for line in self._prog_mem.items():
            print(f'0x{line} {self._prog_mem[line]}')

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
        addr = format(self._program_counter, '02x')
        try:
            instruction = self._prog_mem[addr]
        except KeyError:
            return False

        # Sending the bites to the correct data path
        opcode = instruction[25:32]
        self._control.set_control_signals(opcode)

        logging.debug(f'\nInstruction at {addr}: {instruction}\n'
                      f'-----Control signals-----\n'
                      f'ALU Src: {self._control.alu_src}\n'
                      f'Mem to Reg: {self._control.mem_to_reg}\n'
                      f'Reg Write: {self._control.reg_write}\n'
                      f'Mem Read: {self._control.mem_read}\n'
                      f'Mem Write: {self._control.mem_write}\n'
                      f'Branch: {self._control.branch}\n'
                      f'ALU Op1: {self._control.alu_op1}\n'
                      f'ALU Op2: {self._control.alu_op2}\n')
        self._program_counter += 4
        return True

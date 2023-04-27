from control_unit import ControlUnit
import control_unit
import logging


class RiscV:
    def __init__(self):
        # This is a dictionary of instructions
        self._instruction_memory = {}
        self._program_counter = 0

        self._control = ControlUnit()
        self._register_file = {}

    def pc_value(self):
        return self._program_counter

    def print_memory(self):
        for line in self._instruction_memory:
            print(f'0x{line} {self._instruction_memory[line]}')

    def load_memory(self, file_name):
        logging.debug(f'Loading memory from {file_name}')
        with open(file_name) as f:
            temp_last_addr = 0
            for i, line in enumerate(f):
                if line == "\n":
                    continue
                if i == 0:
                    addr = format(i, '02x')
                else:
                    temp_last_addr = temp_last_addr + 4
                    addr = format(temp_last_addr, '02x')
                self._instruction_memory.update({addr: line.rstrip()})
        logging.debug(f'Loaded {len(self._instruction_memory)} instructions')

    def instruction_at_address(self, address: int):
        hex_addr = format(address, '02x')
        try:
            return self._instruction_memory[hex_addr]
        except KeyError:
            return None

    def cycle(self) -> bool:
        addr = format(self._program_counter, '02x')
        try:
            instruction = self._instruction_memory[addr]
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

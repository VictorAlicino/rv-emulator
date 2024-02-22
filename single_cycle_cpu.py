"""Implementation of a Risc-V Single Cycle CPU simulator."""

import logging
from typing import IO
from rv_units.control_unit import ControlUnit
from rv_units.register_file import RegisterFile, DataRegister
from rv_units.alu import ALU, ADDER

class MUX:
    """This class represents a Multiplexer"""
    def __init__(self, _0 = 0, _1 = 0, select = False):
        self._input0: DataRegister | int = _0
        self._input1: DataRegister | int = _1
        self._select: bool = select

    def write(self, value: DataRegister, select: bool) -> None:
        """Write data to the multiplexer"""
        if select:
            self._input1 = value
        else:
            self._input0 = value

    def read(self) -> DataRegister | int:
        """Read the selected input"""
        if self._select:
            return self._input1
        return self._input0

    def set_select(self, select: bool) -> None:
        """Set the select signal"""
        self._select = select

    def __str__(self):
        return f'Input0: {self._input0} | Input1: {self._input1} | Select: {self._select}'

    def __repr__(self):
        return f'Input0: {self._input0} | Input1: {self._input1} | Select: {self._select}'


class RiscV:
    """This class represents a Risc-V Single Cycle CPU simulator."""
    def __init__(self):
        self._imem: dict = {} # This is a dictionary of instructions

        self._data_mem: IO[bytes] = open('data_memory.bin', 'wb') # Data Memory (Cache) on binary file

        self._control: ControlUnit = ControlUnit() # Control Unit
        self._registers: RegisterFile = RegisterFile() # Register File
        self._alu: ALU = ALU() # Arithmetic Logic Unit

        self.pc: DataRegister = self._registers.zero()  # Program Counter
        self.pc_mux: MUX = MUX()  # Program Counter Multiplexer

    def __del__(self):
        self._data_mem.close()

    def pc_value(self) -> int:
        """Returns the current value of the program counter register"""
        return self.pc.to_int()

    def dump_memory(self):
        """Dump the memory to the console"""
        for addr, instruction in self._imem.items():
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
                self._imem.update({addr: line.rstrip()})
        logging.debug('Loaded %d instructions', len(self._imem))

    def instruction_at_address(self, address: int):
        """Returns the instruction at the given address"""
        hex_addr = format(address, '02x')
        try:
            return self._imem[hex_addr]
        except KeyError:
            return None

    @staticmethod
    def imm_gen(imm: str) -> bytearray:
        """This function receives a 12-bit immediate value and sign extends it to 32 bits"""
        return bytearray([int(imm[0])] * 20) + bytearray(imm, 'utf-8')

    def cycle(self) -> bool:
        """This is the main loop of the CPU"""
        # This code mimics the Risc-V Single Cycle Data Path


        # -----Instruction Fetch-----

        # From the PC we get 3 lines on the data path:
        # One line goes to PC+4;
        # another goes to the branch mux;
        # and the last one goes to the instruction memory.
        curr_addr: int = self.pc_mux.read() # type: ignore
        pc_add_4 = ADDER.do(curr_addr, 4) # PC + 4

        # The output of the instruction memory is the line
        # which is pointed by the PC, its 32 bits will
        # feed other 4 lines on the data path.

        try:
            instruction: str = self._imem[format(self.pc_value(), '02x')]
        except KeyError:
            logging.debug('[CPU] Instruction not found at address %s', hex(curr_addr))
            logging.debug('[CPU] Halting...\n')
            return False


        # -----Instruction Decode-----

        logging.debug('[CPU] Instruction at %s: %s', hex(curr_addr), instruction)

        # The first 7 bits of the instruction are the opcode
        # which will be used to set the control signals.

        # Decoding the Opcode
        opcode: int = int(instruction[25:32], 2)
        self._control.set_opcode(opcode)

        # The next 12 bits are the immediate value
        imm: bytearray = self.imm_gen(instruction)

        # -----Execution-----

        # The next 5 bits are the source register 1
        rr_1: int = int(instruction[12:17], 2)
        # The next 5 bits are the source register 2
        rr_2: int = int(instruction[7:12], 2)
        # The next 5 bits are the destination register
        #rd: int = int(instruction[20:25], 2)

        self._registers.select_register(rr_1, 1)
        self._registers.select_register(rr_2, 2)

        # The next 7 bits are the function code
        #func_code: int = int(instruction[0:7], 2)

        alu_mux: MUX = MUX(self._registers.get_reg(2), imm, self._control.alu_src) # type: ignore

        # The ALU receives the source registers, the immediate value and the function code
        # and the control signals to perform the operation.

        self._alu.set_op_a(self._registers.get_reg(1))
        self._alu.set_op_b(alu_mux.read())
        self._alu.do_op()
        print('ALU Result:', self._alu.result())

        #print(self._control)
        return True

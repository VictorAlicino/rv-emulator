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

        self._data_mem: IO[bytes] = open('data_memory.bin', 'wb') # Cache Memory on binary file

        self._control: ControlUnit = ControlUnit() # Control Unit
        self._registers: RegisterFile = RegisterFile() # Register File
        self._wb_sel: MUX = MUX() # Write Back Selector MUX
        self._alu: ALU = ALU() # Arithmetic Logic Unit

        self._b_sel: MUX = MUX() # Branch Selector MUX

        self.pc: DataRegister = self._registers.zero()  # Program Counter
        self._pc_sel: MUX = MUX()  # Program Counter Multiplexer

    def __del__(self):
        self._data_mem.close()

    def pc_value(self) -> int:
        """Returns the current value of the program counter register"""
        return int(self.pc)

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
    def imm_gen(imm: str) -> DataRegister:
        """This function receives a 12-bit immediate value and sign extends it to 32 bits"""
        temp = int(imm, 2).to_bytes(4, byteorder='big')
        imm32: DataRegister = DataRegister(bytearray.fromhex(temp.hex()))
        return imm32

    def cycle(self) -> bool:
        """This is the main loop of the CPU"""
        # This code mimics the Risc-V Single Cycle Data Path

        # -----Instruction Fetch-----

        # From the PC we get 3 lines on the data path:
        # One line goes to PC+4;
        # another goes to the branch mux;
        # and the last one goes to the instruction memory.
        curr_addr: int = int(self.pc)
        pc_add_4: DataRegister = DataRegister(
            ADDER.do( # PC + 4
                curr_addr,
                4
                ))

        # The output of the instruction memory is the line
        # which is pointed by the PC, its 32 bits will
        # feed other 4 lines on the data path.

        try:
            instruction: str = self._imem[format(curr_addr, '02x')]
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
        imm: DataRegister = self.imm_gen(instruction)

        # The next 5 bits are the source register 1
        rr_1: int = int(instruction[12:17], 2)
        # The next 5 bits are the source register 2
        rr_2: int = int(instruction[7:12], 2)
        # The next 5 bits are the destination register
        rd: int = int(instruction[20:25], 2)

        self._registers.select_register(rr_1, 1)
        self._registers.select_register(rr_2, 2)

        # -----Execution-----

        # The ALU receives the source registers,
        # the immediate value and the ALU Control

        # Select first ALU operand
        self._alu.set_op_a(self._registers.read_data(1))

        # Setting the ALU Multiplexer
        self._b_sel.write(value = self._registers.read_data(2), select = False)
        self._b_sel.write(value = imm, select = True)
        self._b_sel.set_select(self._control.alu_src)

        # Select second ALU operand
        self._alu.set_op_b(self._b_sel.read())

        # The ALU receives the source registers, the immediate value and the function code
        # and the control signals to perform the operation.
        #self._alu.do_op()
        #print('ALU Result:', self._alu.result())

        pc_add_offset: DataRegister = DataRegister(
            ADDER.do( # PC + Offset
                curr_addr,
                int(imm) >> 1) # ImmGen (Shift left 1)
                )

        # -----Memory Access-----

        # TODO: tem que implementar todo esse negócio ainda

        # -----Write Back-----

        dmem_read_data: DataRegister = self._registers.zero()

        if self._control.mem_write:
            # Write the data memory using the ALU result as the address
            # Dev Note: DataRegister should just return bytes if asked so
            self._data_mem.write(bytes(self._registers.read_data(2)))
            self._data_mem.flush()

        elif self._control.mem_read:
            # Read the data memory using the ALU result as the address
            dmem_read_data = DataRegister(
                bytearray(self._data_mem.read( # TODO: aquela coisa ali em cima não rolou
                        self._alu.result()
                    )))
        else:
            pass # Logical "Don't Care"

        # Setting the Write Back Multiplexer
        self._wb_sel.write(dmem_read_data, False)
        self._wb_sel.write(DataRegister(self._alu.result()), True)
        self._wb_sel.set_select(self._control.mem_to_reg)
        # Writing the result to the destination register
        if self._control.reg_write:
            self._registers.write_data(rd, self._wb_sel.read()) # type: ignore
            #-> maybe I need to fix this problems with the MUX returns types

        # Setting the PC Multiplexer
        self._pc_sel.write(pc_add_4, False)
        self._pc_sel.write(pc_add_offset, True)
        self._pc_sel.set_select(
            self._control.branch and self._alu.zero() # Branch AND ALU Zero
            )

        self.pc = self._pc_sel.read() # type: ignore
        #print(self._control)
        return True

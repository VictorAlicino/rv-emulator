"""This module contains the ALU class and the ALUOp enumeration"""
from enum import Enum
from dataclasses import dataclass
from rv_units.register_file import DataRegister

class ALUOp(Enum):
    """Enumeration for the ALU operations"""
    ADD = 0b0000
    SUB = 0b0001
    AND = 0b0010
    OR = 0b0011
    XOR = 0b0100
    SLL = 0b0101
    SRL = 0b0110
    SRA = 0b0111
    SLT = 0b1000
    SLTU = 0b1001
    MUL = 0b1010
    MULH = 0b1011
    MULHSU = 0b1100
    MULHU = 0b1101
    DIV = 0b1110
    DIVU = 0b1111
    REM = 0b10000
    REMU = 0b10001


@dataclass
class ALUmux:
    """This is the second operator MUX of the ALU"""
    a: DataRegister
    b: int

class ADDER:
    """Adder generic class"""
    def __init__(self):
        self._a: int = 0
        self._b: int = 0
        self._result: int = 0

    @classmethod
    def do(cls, op_a: int, op_b: int) -> int:
        """Perform the addition"""
        return op_a + op_b

class ALU:
    """This is the ALU of the CPU"""
    def __init__(self):
        self._op: int = 0
        self._a: int = 0
        self._b: int = 0
        self._result: int = 0
        self._zero: bool = False

    def set_op_a(self, operand: DataRegister) -> None:
        """Set the first operand"""
        self._a = operand.to_int()

    def set_op_b(self, b: int | DataRegister) -> None:
        """Set the second operand"""
        if isinstance(b, DataRegister):
            self._b = b.to_int()
        else:
            self._b = b

    def result(self) -> int | float:
        """Return the result of the operation"""
        return self._result

    def do_op(self) -> None:
        """Perform the operation"""
        if self._op is None:
            raise ValueError('Operation not set')

        match self._op:
            case ALUOp.ADD:
                self._result = self._a + self._b
            case ALUOp.SUB:
                self._result = self._a - self._b
            case ALUOp.AND:
                self._result = self._a & self._b
            case ALUOp.OR:
                self._result = self._a | self._b
            case ALUOp.XOR:
                self._result = self._a ^ self._b
            case ALUOp.SLL:
                self._result = self._a << self._b
            case ALUOp.SRL:
                self._result = self._a >> self._b
            case ALUOp.SRA:
                self._result = self._a >> self._b
            case ALUOp.SLT:
                self._result = int(self._a < self._b)
            case ALUOp.SLTU:
                self._result = int(self._a < self._b)
            case ALUOp.MUL:
                self._result = self._a * self._b
            case ALUOp.MULH:
                self._result = self._a * self._b
            case ALUOp.MULHSU:
                self._result = self._a * self._b
            case ALUOp.MULHU:
                self._result = self._a * self._b
            case ALUOp.DIV:
                self._result = self._a // self._b
            case ALUOp.DIVU:
                self._result = self._a // self._b
            case ALUOp.REM:
                self._result = self._a % self._b
            case ALUOp.REMU:
                self._result = self._a % self._b
            case _:
                raise ValueError('Invalid operation')

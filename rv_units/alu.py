"""This module contains the ALU class and the ALUOp enumeration"""
from enum import Enum
from dataclasses import dataclass
from rv_units.control_unit import ControlUnit
from rv_units.register_file import DataRegister

@dataclass
class ALUmux:
    """This is the second operator MUX of the ALU"""
    a: DataRegister
    b: int

class ADDER:
    """Adder generic class"""
    def __init__(self):
        pass

    @classmethod
    def do(cls, op_a: int | DataRegister, op_b: int | DataRegister) -> int:
        """Perform the addition"""
        a: int = int(op_a)
        b: int = int(op_b)
        return a + b

class ALU:
    """This is the ALU of the CPU"""
    def __init__(self):
        self._a: int = 0
        self._b: int = 0
        self._result: int = 0
        self._zero: bool = False
        self._control: int = 0b0000

    def set_op_a(self, operand: DataRegister) -> None:
        """Set the first operand"""
        self._a = int(operand)

    def set_op_b(self, operand: int | DataRegister) -> None:
        """Set the second operand"""
        self._b = int(operand)

    def result(self) -> int:
        """Return the result of the operation"""
        return self._result

    def zero(self) -> bool:
        """Return the zero flag"""
        return self._zero

    def alu_control(self, control_signal: ControlUnit, funct: int) -> None:
        """Set the ALU control signal"""
        if control_signal.alu_op[0] is True:
            # Branch Equal (BEQ)
            self._control = 0b0110
        else:
            if control_signal.alu_op[1] is True:
                match funct:
                    case 0b100000: # ADD
                        self._control = 0b0010
                    case 0b100010: # SUB
                        self._control = 0b0110
                    case 0b100100: # AND
                        self._control = 0b0000
                    case 0b100101: # OR
                        self._control = 0b0001
                    case 0b101010: # SLT (Set Less Than)
                        self._control = 0b0111
                    case _: # Default
                        raise ValueError('Invalid function code')
            else:
                # Load or Store Word (LW | SW)
                self._control = 0b0010

    def do_op(self) -> None:
        """Perform the operation"""
        if self._control is None:
            raise ValueError('Operation not set')

        match self._control:
            case 0b0010:
                self._result = self._a + self._b
            case 0b0110:
                self._result = self._a - self._b
            case 0b0000:
                self._result = self._a & self._b
            case 0b0001:
                self._result = self._a | self._b
            case 0b0111:
                self._result = int(self._a < self._b)
            case _:
                print('ALUControl:', bin(self._control))
                raise ValueError('Invalid operation')

"""This module contains the ALU class and the ALUOp enumeration"""
from enum import Enum
from dataclasses import dataclass
from rv_units.register_bank import DataRegister

class ALUOp(Enum):
    """Enumeration for the ALU operations"""
    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    XOR = 4
    SLT = 5
    SLL = 6
    SRL = 7
    SRA = 8

@dataclass
class ALUmux:
    """This is the second operator MUX of the ALU"""
    a: DataRegister
    b: int

class ALU:
    """This is the ALU of the CPU"""
    def __init__(self):
        self._op: str = ''
        self._a: DataRegister
        self._b: int = 0
        self._result: int = 0

"""Registers Bank"""

from dataclasses import dataclass
from typing import Final

@dataclass
class DataRegister():
    """Structure to represent a Register"""
    data: bytearray(4) # 32 bits

    def write(self, value: (bytearray)) -> None:
        """Write data to a byte"""
        self.data = value

    def write_int(self, value: int) -> None:
        """Write an integer to the register"""
        self.data = value.to_bytes(4, byteorder='big')

    # To String
    def __str__(self):
        # Printing all the bits
        return ''.join(format(x, '08b') for x in self.data)

    def to_int(self) -> int:
        """Convert the byte array to an integer"""
        return int.from_bytes(self.data, byteorder='big')

    def wipe(self) -> None:
        """Set all bits to 0"""
        self.data = (0 for _ in range(4))


class RegisterBank():
    """Structure to represent the Register Bank"""
    def __init__(self):
        self.x0: Final[DataRegister] = DataRegister(0 for _ in range(4)) # Zero Register
        self.x1: DataRegister = self.x0 # Return Address
        self.x2: DataRegister = self.x0 # Stack Pointer
        self.x3: DataRegister = self.x0 # Global Pointer
        self.x4: DataRegister = self.x0 # Thread Pointer
        self.x5: DataRegister = self.x0 # Temporary 0
        self.x6: DataRegister = self.x0 # Temporary 1
        self.x7: DataRegister = self.x0 # Temporary 2
        self.x8: DataRegister = self.x0 # Frame Pointer
        self.x9: DataRegister = self.x0 # Saved Register 1
        self.x10: DataRegister = self.x0 # Function Argument 0 / Return Value 0
        self.x11: DataRegister = self.x0 # Function Argument 1 / Return Value 1
        self.x12: DataRegister = self.x0 # Function Argument 2
        self.x13: DataRegister = self.x0 # Function Argument 3
        self.x14: DataRegister = self.x0 # Function Argument 4
        self.x15: DataRegister = self.x0 # Function Argument 5
        self.x16: DataRegister = self.x0 # Function Argument 6
        self.x17: DataRegister = self.x0 # Function Argument 7
        self.x18: DataRegister = self.x0 # Saved Register 2
        self.x19: DataRegister = self.x0 # Saved Register 3
        self.x20: DataRegister = self.x0 # Saved Register 4
        self.x21: DataRegister = self.x0 # Saved Register 5
        self.x22: DataRegister = self.x0 # Saved Register 6
        self.x23: DataRegister = self.x0 # Saved Register 7
        self.x24: DataRegister = self.x0 # Saved Register 8
        self.x25: DataRegister = self.x0 # Saved Register 9
        self.x26: DataRegister = self.x0 # Saved Register 10
        self.x27: DataRegister = self.x0 # Saved Register 11
        self.x28: DataRegister = self.x0 # Temporary 3
        self.x29: DataRegister = self.x0 # Temporary 4
        self.x30: DataRegister = self.x0 # Temporary 5
        self.x31: DataRegister = self.x0 # Temporary 6
        self.pc: DataRegister = self.x0 # Program Counter

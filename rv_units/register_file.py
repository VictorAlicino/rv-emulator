"""Registers Bank"""

from typing import Final

class DataRegister():
    """Structure to represent a Register"""

    def __init__(self, data: bytearray | int) -> None:
        if isinstance(data, bytearray):
            self.data: bytearray = data# 32 bits
            return
        self.data = data.to_bytes(4, byteorder='big') # type: ignore

    def __str__(self):
        # Printing all the bits
        return ''.join(format(x, '08b') for x in self.data)

    def __int__(self):
        return int.from_bytes(self.data, byteorder='big')

    def __bytes__(self):
        return self.data

    def write(self, value: bytearray) -> None:
        """Write data to a byte"""
        self.data = value

    def write_int(self, value: int) -> None:
        """Write an integer to the register"""
        self.data = value.to_bytes(4, byteorder='big') # type: ignore

    def wipe(self) -> None:
        """Set all bits to 0"""
        self.data = (0 for _ in range(4)) # type: ignore


class RegisterFile():
    """Structure to represent the Register Bank"""
    def __init__(self):
        self.x0: Final[DataRegister] = DataRegister(0) # Zero Register (Always 0) # type: ignore
        self.x1: DataRegister = self.x0  # Return Address
        self.x2: DataRegister = self.x0  # Stack Pointer
        self.x3: DataRegister = self.x0  # Global Pointer
        self.x4: DataRegister = self.x0  # Thread Pointer
        self.x5: DataRegister = self.x0  # Temporary 0
        self.x6: DataRegister = self.x0  # Temporary 1
        self.x7: DataRegister = self.x0  # Temporary 2
        self.x8: DataRegister = self.x0  # Frame Pointer
        self.x9: DataRegister = self.x0  # Saved Register 1
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

        self._read_data_1: int = 0
        self._read_data_2: int = 0

    def zero(self) -> DataRegister:
        """Return the zero register"""
        return self.x0

    def get_reg(self, read_data: int) -> DataRegister:
        """Get the register by its name"""
        match read_data:
            case 1: return getattr(self, f'x{self._read_data_1}')
            case 2: return getattr(self, f'x{self._read_data_2}')
            case _: raise ValueError('Invalid Read ouput')

    def select_register(self, instruction_reg: str | int, read_data: int) -> None:
        """Set the value on Read Data 1 or Read Data 2"""
        if read_data < 1 or read_data > 2:
            raise ValueError('Invalid Read ouput')

        if isinstance(instruction_reg, str):
            setattr(self, f'read_data_{read_data}', int(instruction_reg, 2))
        else:
            setattr(self, f'read_data_{read_data}', instruction_reg)

    def read_data(self, read_data: int) -> DataRegister:
        """Return the selected register"""
        return getattr(self, f'read_data_{read_data}')

    def write_data(self, write_register: int, value: DataRegister) -> None:
        """Write data to a register"""
        if write_register == 0:
            raise ValueError('Cannot write to x0')
        getattr(self, f'x{write_register}').write(value.data)

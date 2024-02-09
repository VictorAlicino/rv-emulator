"""This module contains the Control Unit"""


class ControlUnit:
    """This class represents the Control Unit of the CPU"""
    def __init__(self):
        self.alu_src: bool = False
        self.mem_to_reg: bool = False
        self.reg_write: bool = False
        self.mem_read: bool = False
        self.mem_write: bool = False
        self.branch: bool = False
        self.alu_op: bool = False

    def set_control_signals(self, signals: dict):
        """Set the control signals from a dictionary of values"""
        for signal, value in signals.items():
            setattr(self, signal, value)

    def __str__(self):
        return (
            f'           |Branch------{self.branch}\n'
            f'           |Mem Read----{self.mem_read}\n'
            f'           |Mem to Reg--{self.mem_to_reg}\n'
            f'Control--->|ALU Op------{self.alu_op}\n'
            f'           |Mem Write---{self.mem_write}\n'
            f'           |ALU Src-----{self.alu_src}\n'
            f'           |Reg Write---{self.reg_write}\n'
        )

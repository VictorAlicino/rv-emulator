# Constants for control signals


class ControlUnit:
    def __init__(self):
        self.alu_src: bool = False
        self.mem_to_reg: bool = False
        self.reg_write: bool = False
        self.mem_read: bool = False
        self.mem_write: bool = False
        self.branch: bool = False
        self.alu_op1: bool = False
        self.alu_op2: bool = False

    def set_control_signals(self, opcode: str):
        control_signals = {
            '0110011': {
                'alu_src': False,
                'mem_to_reg': False,
                'reg_write': True,
                'mem_read': False,
                'mem_write': False,
                'branch': False,
                'alu_op1': True,
                'alu_op2': False,
            },
            '0000011': {
                'alu_src': True,
                'mem_to_reg': True,
                'reg_write': True,
                'mem_read': True,
                'mem_write': False,
                'branch': False,
                'alu_op1': False,
                'alu_op2': False,
            },
            '0100011': {
                'alu_src': True,
                'mem_to_reg': None,
                'reg_write': False,
                'mem_read': False,
                'mem_write': True,
                'branch': False,
                'alu_op1': False,
                'alu_op2': False,
            },
            '1100011': {
                'alu_src': False,
                'mem_to_reg': None,
                'reg_write': False,
                'mem_read': False,
                'mem_write': False,
                'branch': True,
                'alu_op1': False,
                'alu_op2': True,
            },
            '0010011': {
                'alu_src': True,
                'mem_to_reg': False,
                'reg_write': True,
                'mem_read': False,
                'mem_write': False,
                'branch': False,
                'alu_op1': True,
                'alu_op2': False,
            }
        }

        if opcode in control_signals:
            signals = control_signals[opcode]
            for signal, value in signals.items():
                setattr(self, signal, value)

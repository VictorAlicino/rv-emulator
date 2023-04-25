# Constants for control signals
ADD = '0110011'
SUB = '000001'
AND = '000010'
OR = '000011'
ADDI = '0010011'
LW = '0000011'
SW = '0100011'
BEQ = '000111'
BNE = '001000'


class ControlUnit:
    def __init__(self):
        self.last_instruction: str = ""
        self.branch: bool = False
        self.mem_read: bool = False
        self.mem_to_reg: bool = False
        self.alu_op: int = 0
        self.mem_write: bool = False
        self.alu_src: bool = False
        self.reg_write: bool = False

    def set_control_signals(self, opcode: str):
        self.last_instruction = f"{opcode} | {'ADD' if opcode == ADD else 'SUB' if opcode == SUB else 'AND' if opcode == AND else 'OR' if opcode == OR else 'ADDI' if opcode == ADDI else 'LW' if opcode == LW else 'SW' if opcode == SW else 'BEQ' if opcode == BEQ else 'BNE' if opcode == BNE else 'unknown opcode'}"
        control_signals = {
            ADD: {"alu_op": True},
            SUB: {"alu_op": True},
            AND: {"alu_op": True},
            OR: {"alu_op": True},
            ADDI: {"alu_op": True},
            LW: {"mem_read": True, "mem_to_reg": True, "reg_write": True},
            SW: {"mem_write": True, "alu_src": True},
            BEQ: {"branch": True},
            BNE: {"branch": True}
        }

        if opcode in control_signals:
            signals = control_signals[opcode]
            for signal, value in signals.items():
                setattr(self, signal, value)


class ControlUnit:
    def __init__(self):
        self.branch: bool = False
        self.mem_read: bool = False
        self.mem_to_reg: bool = False
        self.alu_op: int = 0
        self.mem_write: bool = False
        self.alu_src: bool = False
        self.reg_write: bool = False

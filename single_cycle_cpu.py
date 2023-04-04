class RiscV:
    def __init__(self):
        # This is a dictionary of instructions
        self._instruction_memory = {}
        self._program_counter = 0

    def load_memory(self, file_name):
        with open(file_name) as f:
            temp_last_addr = 0
            for i, line in enumerate(f):
                if line == "\n":
                    continue
                if i == 0:
                    addr = format(i, '02x')
                else:
                    temp_last_addr = temp_last_addr + 4
                    addr = format(temp_last_addr, '02x')
                self._instruction_memory.update({addr: line.rstrip()})

    def print_memory(self):
        for line in self._instruction_memory:
            print(f'0x{line} {self._instruction_memory[line]}')

    def cycle(self) -> bool:
        addr = format(self._program_counter, '02x')
        try:
            instruction = self._instruction_memory[addr]
        except KeyError:
            return False
        print(instruction)
        self._program_counter += 4
        return True

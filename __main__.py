import tkinter as tk
from tkinter import filedialog
from single_cycle_cpu import RiscV


def _main():
    risc_v = RiscV()
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    risc_v.load_memory(file_path)
    while risc_v.cycle():
        pass


if __name__ == "__main__":
    _main()

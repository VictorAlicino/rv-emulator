"""This is a simple RISC-V Single Cycle CPU simulator."""

import sys
import logging
import tkinter as tk
from tkinter import filedialog
from single_cycle_cpu import RiscV


def _main() -> int:
    """Main function"""
    root = tk.Tk()
    root.withdraw()
    if len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                                format='%(asctime)s %(message)s',
                                handlers=[
                                    logging.FileHandler("debug.log"),
                                    logging.StreamHandler()
                                ]
                                )
        else:
            print('Invalid arguments')
            return 1
    else:
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            handlers=[logging.FileHandler("debug.log")]
                            )

    risc_v = RiscV()
    file_path = filedialog.askopenfilename() # Won't work with TUI

    try:
        risc_v.load_program(file_path)
    except ValueError as e:
        print(f'Failed to load program: {e}')
        return 1

    while risc_v.cycle():
        pass

    return 0


if __name__ == "__main__":
    sys.exit(_main())

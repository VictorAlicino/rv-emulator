import tkinter as tk
from tkinter import filedialog
from single_cycle_cpu import RiscV
import logging
import sys


def _main() -> int:
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
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    try:
        risc_v.load_memory(file_path)
    except ValueError as e:
        print(e)
        return 1

    while risc_v.cycle():
        pass

    return 0


if __name__ == "__main__":
    exit(_main())

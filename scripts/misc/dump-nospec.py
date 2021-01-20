#!/usr/bin/python3

import os
import sys
sys.path.append(f'{os.path.dirname(sys.argv[0])}/../../lib')
from dump import *


def main(args):
    if len(args) == 0:
        print("Usage: %s <vmlinux>" % sys.argv[0], file=sys.stderr)
        return 1

    path = args[0]
    syms = read_symbols(path)

    init_begin = find_symbol(syms, '__init_begin')
    init_end = find_symbol(syms, '__init_end')

    print("# Dumping barrier_nospec fixup sites")
    print("# Fixup entry    Address          Symbol")

    try:
        for entry_addr, addr in iter_nospec_fixups(path):
            in_init = ''
            if init_begin and init_end:
                if init_begin <= addr and addr <= init_end:
                    in_init = '# in .init section'

            symbol, offset = find_addr(syms, addr)
            print(f'{entry_addr:016x} {addr:016x} {symbol}+0x{offset:x} {in_init}')
    except (KeyboardInterrupt, BrokenPipeError):
        pass

    return 0


sys.exit(main(sys.argv[1:]))

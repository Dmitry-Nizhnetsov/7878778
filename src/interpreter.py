"""Interpreter for the educational virtual machine."""

import sys
import xml.etree.ElementTree as et
from constants import OP_LOAD_CONST, OP_READ_MEM
from constants import OP_WRITE_MEM, OP_UNARY_MINUS
from constants import MIN_ARGC_INTERP, SHIFT_AMOUNT
from constants import BITS_CONST, BITS_OFFSET, BITS_ADDR


def mask(n):
    """Return bitmask with n ones."""
    return (1 << n) - 1


def parse_arguments(argv):
    """Parse command line arguments and return a tuple."""
    if len(argv) < MIN_ARGC_INTERP:
        return None, None, 0, 0
    bin_path = argv[1]
    dump_path = argv[2]
    start_addr = int(argv[3])
    end_addr = int(argv[4])
    return bin_path, dump_path, start_addr, end_addr


def load_binary(path):
    """Load binary file and return bytes."""
    with open(path, "rb") as file:
        return file.read()


def save_dump(memory, start, end, path):
    """Save memory range to XML."""
    root = et.Element("memory")
    for i in range(start, end + 1):
        cell = et.SubElement(root, "cell", address=str(i))
        cell.text = str(memory[i])
    tree = et.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def run_program(bytecode, dump_path, start, end):
    """Main interpreter loop."""
    memory = [0] * 65536
    pc = 0
    acc = 0
    while pc < len(bytecode):
        b1 = bytecode[pc]
        opcode = b1 & 0b11111

        if opcode == OP_LOAD_CONST:
            b2 = bytecode[pc + 1]
            b3 = bytecode[pc + 2]
            val = b1 | (b2 << 8) | (b3 << 16)
            acc = (val >> SHIFT_AMOUNT) & mask(BITS_CONST)
            pc += 3

        elif opcode == OP_READ_MEM:
            b2 = bytecode[pc + 1]
            val = b1 | (b2 << 8)
            offset = (val >> SHIFT_AMOUNT) & mask(BITS_OFFSET)
            acc = memory[acc + offset]
            pc += 2

        elif opcode == OP_WRITE_MEM:
            b2 = bytecode[pc + 1]
            b3 = bytecode[pc + 2]
            b4 = bytecode[pc + 3]
            val = b1 | (b2 << 8) | (b3 << 16) | (b4 << 24)
            addr = (val >> SHIFT_AMOUNT) & mask(BITS_ADDR)
            memory[addr] = acc
            pc += 4

        elif opcode == OP_UNARY_MINUS:
            acc = -acc
            pc += 1

        else:
            break

    save_dump(memory, start, end, dump_path)


def main(argv):
    """Entry point of the interpreter."""
    bin_path, dump_path, start, end = parse_arguments(argv)
    if bin_path is None:
        print("Usage: python src/interpreter.py <bin> <xml> <start> <end>")
        return
    bytecode = load_binary(bin_path)
    run_program(bytecode, dump_path, start, end)


if __name__ == "__main__":
    main(sys.argv)
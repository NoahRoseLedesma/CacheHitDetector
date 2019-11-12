#!/usr/bin/env python3

# Python script to determine the order of cache hits and misses given a test input file

import argparse
import os

parser = argparse.ArgumentParser(description="Determine the order of cache hits/misses given a test file.")
parser.add_argument("test_file", type=str, help="The test input file. This is the file you would load into the 'Inputs' circuit.")
args = parser.parse_args()

if not os.path.isfile(args.test_file):
    print("No such file", args.test_file)
    exit(1)

TestInputs = open(args.test_file, "r").read().split("\n")

if "v2.0 raw" not in TestInputs[0]:
    print("File", args.test_file, "is not a valid image file.")

TestCaseNumber = 0
for line in TestInputs:
    # Remove comments from the line
    if "#" in line:
        line = line[0: line.index("#")]

    # Ignore file header and empty lines
    if "v2.0 raw" in line or line is "":
        continue

    # Remove whitespace
    line = "".join(line.split())

    # Line should now be hex
    opcode = int(line, 16)

    operation = ""
    address = (opcode & 0b111111111100000000) >> 8
    value = opcode & 0b11111111
    
    # Determine the type of operation
    if opcode & (1 << 19):
        operation = "Read "
    elif opcode & (1 << 18):
        operation = "Write"
    elif opcode & (1 << 20):
        operation = "Done "
    else:
        operation = "Nop  "

    print("Input ", TestCaseNumber)
    print("\t", operation, "| Address:", address, "| Value:", value)
    TestCaseNumber += 1

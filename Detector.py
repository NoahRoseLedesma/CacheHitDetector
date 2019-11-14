#!/usr/bin/env python3

# Python script to determine the order of cache hits and misses given a test input file

import argparse
import os
from Cache import Cache

parser = argparse.ArgumentParser(description="Determine the order of cache hits/misses given a test file.")
parser.add_argument("test_file", type=str, help="The test input file. This is the file you would load into the 'Inputs' circuit.")
parser.add_argument("--verbose", type=bool)
args = parser.parse_args()

if not os.path.isfile(args.test_file):
    print("No such file", args.test_file)
    exit(1)

TestInputs = open(args.test_file, "r").read().split("\n")

if "v2.0 raw" not in TestInputs[0]:
    print("File", args.test_file, "is not a valid image file.")

TestCaseNumber = 0
cache = Cache()
HitCount = 0
MissCount = 0

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
    set_id = (address & (0b100)) >> 2
    tag = (address & (0b1111111000)) >> 3
    offset = address & (0b11)
    value = opcode & 0b11111111
    
    didHit = None

    # Determine the type of operation
    if opcode & (1 << 19):
        operation = "Read"
        didHit = cache.contains(set_id, tag)
    elif opcode & (1 << 18):
        operation = "Write"
        didHit = cache.contains(set_id, tag)
    elif opcode & (1 << 20):
        operation = "Done"
    else:
        operation = "Nop" 

    if args.verbose:
        print("Input", TestCaseNumber, operation, "Set:", set_id, "Tag:", tag, "Offset:", offset, "Value:", bin(value), end=" ")
    else:
        print(str(TestCaseNumber) + ":", end=" ")
    if didHit is not None:
        if didHit:
            print("Hit")
            HitCount += 1
        else:
            print("Miss")
            MissCount += 1

        line = cache.updateTag(set_id, tag)
        cache.updateAges(set_id, line[1])
        line_index = 0
        for line in cache.sets[set_id].lines:
            print("\t" + "Line", line_index, "Tag", line.tag, "Age", line.age)
            line_index += 1
    else:
        print("")
    TestCaseNumber += 1

print("Total hits:", HitCount, "Total Misses:", MissCount)

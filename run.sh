#!/bin/bash

echo "=== Stage 1 ==="
python src/assembler.py tests/test_prog.yaml out.bin --test

echo "=== Stage 2 ==="
python src/assembler.py tests/copy_prog.yaml copy.bin

echo "=== Stage 3 ==="
python src/interpreter.py copy.bin copy_dump.xml 198 202

echo "=== Stage 4 ==="
python src/assembler.py tests/alu_prog.yaml alu.bin
python src/interpreter.py alu.bin alu_dump.xml 300 300

echo "=== Stage 5 ==="
python src/assembler.py tests/task_prog.yaml task.bin
python src/interpreter.py task.bin task_dump.xml 1000 1008

echo "=== Done ==="
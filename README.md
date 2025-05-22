# chip8
# CHIP-8 Emulator

This is a basic CHIP-8 emulator written in Python using the Pygame library. It aims to emulate the classic CHIP-8 system and run simple CHIP-8 programs (ROMs).


I am a beginner in emulator development, and this project is my attempt to understand how CHIP-8 works and how to implement an emulator from scratch. The emulator is a work in progress and may contain errors or incomplete features.

Features:
- Loads and runs CHIP-8 ROMs
- Supports basic opcodes (e.g., display clearing, jumps, subroutine calls, etc.)
- Keyboard input mapped to CHIP-8 hex keys
- Display rendering using Pygame

Known Issue:
- **Opcode 0xF007**: The implementation for setting register `Vx` to the value of the delay timer may not function correctly. Further debugging is needed.


Acknowledgements:
This project is inspired by various CHIP-8 documentation and tutorials online. Special thanks to the CHIP-8 community for the available resources.

Future Improvements:
- Fix the `0xF007` opcode issue
- Add support for more opcodes
- Improve performance and display accuracy
- Implement sound support


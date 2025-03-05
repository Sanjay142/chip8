import pygame
import sys
import time
import random

class Chip8:
    def __init__(self):
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        self.stack = []
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [0] * (64 * 32)
        self.keys = [0] * 16
        self.running = True

        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for i in range(len(self.fontset)):
            self.memory[i] = self.fontset[i]

    def load_rom(self, filename):
        with open(filename, 'rb') as f:
            rom = f.read()
        for i in range(len(rom)):
            self.memory[0x200 + i] = rom[i]

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 320))
        pygame.display.set_caption("CHIP-8 Emulator")

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
            self.pc += 2

            self.execute_opcode(opcode)

            if self.delay_timer > 0:
                self.delay_timer -= 1

            if self.sound_timer > 0:
                self.sound_timer -= 1

            self.draw_display(screen)

            clock.tick(500)

        pygame.quit()
        sys.exit()

    def execute_opcode(self, opcode):
        if opcode == 0x00E0:  # Clear the display
            self.display = [0] * (64 * 32)

        elif opcode == 0x00EE:  # Return from subroutine
            self.pc = self.stack.pop()

        elif opcode & 0xF000 == 0x1000:  # 1nnn: Jump to address nnn
            self.pc = opcode & 0x0FFF

        elif opcode & 0xF000 == 0x2000:  # 2nnn: Call subroutine at nnn
            self.stack.append(self.pc)
            self.pc = opcode & 0x0FFF

        elif opcode & 0xF000 == 0x3000:  # 3xkk: Skip if Vx == kk
            x = (opcode & 0x0F00) >> 8
            kk = opcode & 0x00FF
            if self.V[x] == kk:
                self.pc += 2

        elif opcode & 0xF000 == 0x4000:  # 4xkk: Skip if Vx != kk
            x = (opcode & 0x0F00) >> 8
            kk = opcode & 0x00FF
            if self.V[x] != kk:
                self.pc += 2

        elif opcode & 0xF00F == 0x8004:  # 8xy4: Add Vx + Vy with carry
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            result = self.V[x] + self.V[y]
            self.V[0xF] = 1 if result > 255 else 0
            self.V[x] = result & 0xFF

        elif opcode & 0xF000 == 0x6000:  # 6xkk: Set Vx = kk
            x = (opcode & 0x0F00) >> 8
            self.V[x] = opcode & 0x00FF

        elif opcode & 0xF000 == 0x7000:  # 7xkk: Add kk to Vx (no carry)
            x = (opcode & 0x0F00) >> 8
            self.V[x] = (self.V[x] + (opcode & 0x00FF)) & 0xFF

        elif opcode & 0xF000 == 0xA000:  # Annn: Set I to nnn
            self.I = opcode & 0x0FFF

        elif opcode & 0xF000 == 0xD000:  # Dxyn: Display/draw
            x = self.V[(opcode & 0x0F00) >> 8]
            y = self.V[(opcode & 0x00F0) >> 4]
            height = opcode & 0x000F

            self.V[0xF] = 0

            for row in range(height):
                sprite = self.memory[self.I + row]
                for col in range(8):
                    if (sprite & (0x80 >> col)) != 0:
                        index = (x + col) % 64 + ((y + row) % 32) * 64
                        if self.display[index] == 1:
                            self.V[0xF] = 1
                        self.display[index] ^= 1

        else:
            print(f"Unknown opcode: {hex(opcode)}")

    def draw_display(self, screen):
        screen.fill((0, 0, 0))
        for i in range(64 * 32):
            if self.display[i]:
                x = (i % 64) * 10
                y = (i // 64) * 10
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 10, 10))
        pygame.display.flip()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python chip8.py <ROM file>")
        sys.exit(1)

    chip8 = Chip8()
    chip8.load_rom(sys.argv[1])
    chip8.run()

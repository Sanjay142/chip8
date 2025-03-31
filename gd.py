import sys
import pygame
import random

class Chip8:
    def __init__(s):
        s.memory = [0] * 4096
        s.V = [0] * 16
        s.I = 0
        s.pc = 0x200
        s.stack = []
        s.delay_timer = 0
        s.sound_timer = 0
        s.display = [0] * (64 * 32)
        s.keys = [0] * 16
        s.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, 0x20, 0x60, 0x20, 0x20, 0x70,
            0xF0, 0x10, 0xF0, 0x80, 0xF0, 0xF0, 0x10, 0xF0, 0x10, 0xF0,
            0x90, 0x90, 0xF0, 0x10, 0x10, 0xF0, 0x80, 0xF0, 0x10, 0xF0,
            0xF0, 0x80, 0xF0, 0x90, 0xF0, 0xF0, 0x10, 0x20, 0x40, 0x40,
            0xF0, 0x90, 0xF0, 0x90, 0xF0, 0xF0, 0x90, 0xF0, 0x10, 0xF0
        ]
        for i in range(len(s.fontset)):
            s.memory[i] = s.fontset[i]
        
        pygame.init()
        s.scale = 10
        s.screen = pygame.display.set_mode((64 * s.scale, 32 * s.scale))
        pygame.display.set_caption("CHIP-8 Emulator")
    
    def draw_display(s):
        s.screen.fill((0, 0, 0))
        for y in range(32):
            for x in range(64):
                if s.display[y * 64 + x]:
                    pygame.draw.rect(s.screen, (255, 255, 255), (x * s.scale, y * s.scale, s.scale, s.scale))
        pygame.display.flip()
    
    def load_rom(s, filename):
        with open(filename, 'rb') as f:
            rom = f.read()
        for i in range(len(rom)):
            s.memory[0x200 + i] = rom[i]
    
    def run(s):
            
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            opcode = (s.memory[s.pc] << 8) | s.memory[s.pc + 1]
            s.pc += 2
            nnn = opcode & 0x0FFF
            kk = opcode & 0x00FF
            n = opcode & 0x000F
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            
            if opcode == 0x00E0:
                s.display = [0] * (64 * 32)
                s.draw_display()
            elif opcode == 0x00EE:
                s.pc = s.stack.pop()
            elif opcode & 0xF000 == 0x1000:
                s.pc = nnn
            elif opcode & 0xF000 == 0x2000:
                s.stack.append(s.pc)
                s.pc = nnn
            elif opcode & 0xF000 == 0x3000:
                if s.V[x] == kk:
                    s.pc += 2
            elif opcode & 0xF000 == 0x4000:
                if s.V[x] != kk:
                    s.pc += 2
            elif opcode & 0xF000 == 0x5000:
                if s.V[x] == s.V[y]:
                    s.pc += 2
            elif opcode & 0xF000 == 0x6000:
                s.V[x] = kk
            elif opcode & 0xF000 == 0x7000:
                s.V[x] = (s.V[x] + kk) & 0xFF
            elif opcode & 0xF000 == 0xA000:
                s.I = nnn
            elif opcode & 0xF000 == 0xC000:
                s.V[x] = random.randint(0, 255) & kk
            elif opcode & 0xF000 == 0xD000:
                s.V[0xF] = 0
                for row in range(n):
                    pixel = s.memory[s.I + row]
                    for col in range(8):
                        if pixel & (0x80 >> col):
                            idx = (s.V[y] + row) * 64 + (s.V[x] + col)
                            if s.display[idx]:
                                s.V[0xF] = 1
                            s.display[idx] ^= 1
                s.draw_display()
            if s.delay_timer > 0:
                s.delay_timer -= 1
            if s.sound_timer > 0:
                s.sound_timer -= 1
            
            clock.tick(500)

if __name__ == "__main__":
    chip8 = Chip8()
    chip8.load_rom(sys.argv[1])
    chip8.run()

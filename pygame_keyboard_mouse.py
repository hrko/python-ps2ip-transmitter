#!/usr/bin/env python3

# AUTHOR=EMARD,hrko
# LICENSE=GPL

import pygame
import struct
import socket
import time
import signal
import sys

esp32_ip = "172.21.186.100"
esp32_port = 3252
esp32_addr = (esp32_ip, esp32_port)
toggle_grab_key = pygame.K_INSERT
mouse_speed_factor = 1.2
report_rate_hz = 60

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Sending events to udp://%s:%s" % (esp32_ip,esp32_port))

def generate_and_send_keyboard_packet(key, action):
  pygame_key_to_scan_code = {pygame.K_ESCAPE: {"is_special_key":  False, "scan_code": 0x76},
                            pygame.K_F1: {"is_special_key":  False, "scan_code": 0x05},
                            pygame.K_F2: {"is_special_key":  False, "scan_code": 0x06},
                            pygame.K_F3: {"is_special_key":  False, "scan_code": 0x04},
                            pygame.K_F4: {"is_special_key":  False, "scan_code": 0x0c},
                            pygame.K_F5: {"is_special_key":  False, "scan_code": 0x03},
                            pygame.K_F6: {"is_special_key":  False, "scan_code": 0x0b},
                            pygame.K_F7: {"is_special_key":  False, "scan_code": 0x83},
                            pygame.K_F8: {"is_special_key":  False, "scan_code": 0x0a},
                            pygame.K_F9: {"is_special_key":  False, "scan_code": 0x01},
                            pygame.K_F10: {"is_special_key":  False, "scan_code": 0x09},
                            pygame.K_F11: {"is_special_key":  False, "scan_code": 0x78},
                            pygame.K_F12: {"is_special_key":  False, "scan_code": 0x07},
                            pygame.K_SCROLLOCK: {"is_special_key":  False, "scan_code": 0x7e},
                            pygame.K_BACKQUOTE: {"is_special_key":  False, "scan_code": 0x0e},
                            pygame.K_1: {"is_special_key":  False, "scan_code": 0x16},
                            pygame.K_2: {"is_special_key":  False, "scan_code": 0x1e},
                            pygame.K_3: {"is_special_key":  False, "scan_code": 0x26},
                            pygame.K_4: {"is_special_key":  False, "scan_code": 0x25},
                            pygame.K_5: {"is_special_key":  False, "scan_code": 0x2e},
                            pygame.K_6: {"is_special_key":  False, "scan_code": 0x36},
                            pygame.K_7: {"is_special_key":  False, "scan_code": 0x3d},
                            pygame.K_8: {"is_special_key":  False, "scan_code": 0x3e},
                            pygame.K_9: {"is_special_key":  False, "scan_code": 0x46},
                            pygame.K_0: {"is_special_key":  False, "scan_code": 0x45},
                            pygame.K_MINUS: {"is_special_key":  False, "scan_code": 0x4e},
                            pygame.K_EQUALS: {"is_special_key":  False, "scan_code": 0x55},
                            pygame.K_BACKSPACE: {"is_special_key":  False, "scan_code": 0x66},
                            pygame.K_TAB: {"is_special_key":  False, "scan_code": 0x0d},
                            pygame.K_q: {"is_special_key":  False, "scan_code": 0x15},
                            pygame.K_w: {"is_special_key":  False, "scan_code": 0x1d},
                            pygame.K_e: {"is_special_key":  False, "scan_code": 0x24},
                            pygame.K_r: {"is_special_key":  False, "scan_code": 0x2d},
                            pygame.K_t: {"is_special_key":  False, "scan_code": 0x2c},
                            pygame.K_y: {"is_special_key":  False, "scan_code": 0x35},
                            pygame.K_u: {"is_special_key":  False, "scan_code": 0x3c},
                            pygame.K_i: {"is_special_key":  False, "scan_code": 0x43},
                            pygame.K_o: {"is_special_key":  False, "scan_code": 0x44},
                            pygame.K_p: {"is_special_key":  False, "scan_code": 0x4d},
                            pygame.K_LEFTBRACKET: {"is_special_key":  False, "scan_code": 0x54},
                            pygame.K_RIGHTBRACKET: {"is_special_key":  False, "scan_code": 0x5b},
                            pygame.K_BACKSLASH: {"is_special_key":  False, "scan_code": 0x5d},
                            pygame.K_CAPSLOCK: {"is_special_key":  False, "scan_code": 0x58},
                            pygame.K_a: {"is_special_key":  False, "scan_code": 0x1c},
                            pygame.K_s: {"is_special_key":  False, "scan_code": 0x1b},
                            pygame.K_d: {"is_special_key":  False, "scan_code": 0x23},
                            pygame.K_f: {"is_special_key":  False, "scan_code": 0x2b},
                            pygame.K_g: {"is_special_key":  False, "scan_code": 0x34},
                            pygame.K_h: {"is_special_key":  False, "scan_code": 0x33},
                            pygame.K_j: {"is_special_key":  False, "scan_code": 0x3b},
                            pygame.K_k: {"is_special_key":  False, "scan_code": 0x42},
                            pygame.K_l: {"is_special_key":  False, "scan_code": 0x4b},
                            pygame.K_SEMICOLON: {"is_special_key":  False, "scan_code": 0x4c},
                            pygame.K_QUOTE: {"is_special_key":  False, "scan_code": 0x52},
                            pygame.K_RETURN: {"is_special_key":  False, "scan_code": 0x5a},
                            pygame.K_LSHIFT: {"is_special_key":  False, "scan_code": 0x12},
                            pygame.K_z: {"is_special_key":  False, "scan_code": 0x1a},
                            pygame.K_x: {"is_special_key":  False, "scan_code": 0x22},
                            pygame.K_c: {"is_special_key":  False, "scan_code": 0x21},
                            pygame.K_v: {"is_special_key":  False, "scan_code": 0x2a},
                            pygame.K_b: {"is_special_key":  False, "scan_code": 0x32},
                            pygame.K_n: {"is_special_key":  False, "scan_code": 0x31},
                            pygame.K_m: {"is_special_key":  False, "scan_code": 0x3a},
                            pygame.K_COMMA: {"is_special_key":  False, "scan_code": 0x41},
                            pygame.K_PERIOD: {"is_special_key":  False, "scan_code": 0x49},
                            pygame.K_SLASH: {"is_special_key":  False, "scan_code": 0x4a},
                            pygame.K_RSHIFT: {"is_special_key":  False, "scan_code": 0x59},
                            pygame.K_LCTRL: {"is_special_key":  False, "scan_code": 0x14},
                            pygame.K_LALT: {"is_special_key":  False, "scan_code": 0x11},
                            pygame.K_SPACE: {"is_special_key":  False, "scan_code": 0x29},
                            pygame.K_NUMLOCK: {"is_special_key":  False, "scan_code": 0x77},
                            pygame.K_KP_MULTIPLY: {"is_special_key":  False, "scan_code": 0x7c},
                            pygame.K_KP_MINUS: {"is_special_key":  False, "scan_code": 0x7b},
                            pygame.K_KP7: {"is_special_key":  False, "scan_code": 0x6c},
                            pygame.K_KP8: {"is_special_key":  False, "scan_code": 0x75},
                            pygame.K_KP9: {"is_special_key":  False, "scan_code": 0x7d},
                            pygame.K_KP_PLUS: {"is_special_key":  False, "scan_code": 0x79},
                            pygame.K_KP4: {"is_special_key":  False, "scan_code": 0x6b},
                            pygame.K_KP5: {"is_special_key":  False, "scan_code": 0x73},
                            pygame.K_KP6: {"is_special_key":  False, "scan_code": 0x74},
                            pygame.K_KP1: {"is_special_key":  False, "scan_code": 0x69},
                            pygame.K_KP2: {"is_special_key":  False, "scan_code": 0x72},
                            pygame.K_KP3: {"is_special_key":  False, "scan_code": 0x7a},
                            pygame.K_KP0: {"is_special_key":  False, "scan_code": 0x70},
                            pygame.K_KP_PERIOD: {"is_special_key":  False, "scan_code": 0x71},
                            pygame.K_LSUPER: {"is_special_key": True, "scan_code": 0x1f},
                            pygame.K_RALT: {"is_special_key": True, "scan_code": 0x11},
                            pygame.K_RSUPER: {"is_special_key": True, "scan_code": 0x27},
                            pygame.K_MENU: {"is_special_key": True, "scan_code": 0x2f},
                            pygame.K_RCTRL: {"is_special_key": True, "scan_code": 0x14},
                            pygame.K_INSERT: {"is_special_key": True, "scan_code": 0x70},
                            pygame.K_HOME: {"is_special_key": True, "scan_code": 0x6c},
                            pygame.K_PAGEUP: {"is_special_key": True, "scan_code": 0x7d},
                            pygame.K_DELETE: {"is_special_key": True, "scan_code": 0x71},
                            pygame.K_END: {"is_special_key": True, "scan_code": 0x69},
                            pygame.K_PAGEDOWN: {"is_special_key": True, "scan_code": 0x7a},
                            pygame.K_UP: {"is_special_key": True, "scan_code": 0x75},
                            pygame.K_LEFT: {"is_special_key": True, "scan_code": 0x6b},
                            pygame.K_DOWN: {"is_special_key": True, "scan_code": 0x72},
                            pygame.K_RIGHT: {"is_special_key": True, "scan_code": 0x74},
                            pygame.K_KP_DIVIDE: {"is_special_key": True, "scan_code": 0x4a},
                            pygame.K_KP_ENTER: {"is_special_key": True, "scan_code": 0x5a}
  }

  if key in pygame_key_to_scan_code:
    item = pygame_key_to_scan_code[key]
    code = item["scan_code"]
    if item["is_special_key"] == True:
      if action == 'make':
        packet = bytearray([ord('K'), 2, 0xE0, code])
      elif action == 'break':
        packet = bytearray([ord('K'), 3, 0xE0, 0xF0, code])
    elif item["is_special_key"] == False:
      if action == 'make':
        packet = bytearray([ord('K'), 1, code])
      elif action == 'break':
        packet = bytearray([ord('K'), 2, 0xF0, code])
    sock.sendto(packet, esp32_addr)
  if key == pygame.K_PRINT:
    if action == 'make':
      packet = bytearray([ord('K'), 4, 0xE0, 0x12, 0xE0, 0x7C])
    elif action == 'break':
      packet = bytearray([ord('K'), 6, 0xE0, 0xF0, 0x7C, 0xE0, 0xF0, 0x12])
    sock.sendto(packet, esp32_addr)
  if key == pygame.K_PAUSE:
    if action == 'make':
      0xE1, 0x14, 0x77, 0xE1, 0xF0, 0x14, 0xE0, 0x77, 
      packet = bytearray([ord('K'), 8, 0xE1, 0x14, 0x77, 0xE1, 0xF0, 0x14, 0xE0, 0x77])
    # Pause key does not have a break code
    sock.sendto(packet, esp32_addr)

def generate_mouse_packet(dx,dy,dz,btn_left,btn_middle,btn_right):
  dx_overflow_bit = 0
  dy_overflow_bit = 0
  dx = int(dx)
  dy = int(dy)
  if dx > 255:
    dx = 255
    dx_overflow_bit = 1
  elif dx < -255:
    dx = -255
    dx_overflow_bit = 1
  if dy > 255:
    dy = 255
    dy_overflow_bit = 1
  elif dy < -255:
    dy = -255
    dy_overflow_bit = 1
  dx_sign_bit = ((dx & 0x100) >> 8) & 1
  dy_sign_bit = ((dy & 0x100) >> 8) & 1
  return struct.pack("<BBBBBB",
    ord('M'), 4, # 4-byte mouse packet
     (btn_left   & 1)       ^
    ((btn_right  & 1) << 1) ^
    ((btn_middle & 1) << 2) ^
    (              1  << 3) ^
    ( dx_sign_bit     << 4) ^
    ( dy_sign_bit     << 5) ^
    ( dx_overflow_bit << 6) ^
    ( dy_overflow_bit << 7),
    dx & 0xFF, 
    dy & 0xFF, 
    dz & 0x0F
    )

pygame.init()
(width, height) = (400, 300)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption(f'Press [{pygame.key.name(toggle_grab_key)}] to release/lock mouse')
pygame.display.flip()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 32)

last_time_reported_ms = 0
report_interval_ms = 1000 / report_rate_hz

# mouse pointer visual feedback
line_pos_x=0
line_pos_y=0
# keyboard visual feedback
key_pressed_list = []
# mouse counter
mouse_counter_x=0
mouse_counter_y=0
# mouse button state
btn_left = 0
btn_middle = 0
btn_right = 0

signal.signal(signal.SIGINT, lambda: exit())

def update_screen():
  # visual feedback
  screen.fill((0,0,0))
  keyboard_text = ""
  for key in key_pressed_list:
    keyboard_text += f"[{pygame.key.name(key)}] "
  screen.blit(font.render(keyboard_text, True, (255, 255, 255)), (0, 0))
  # draw mouse line
  pygame.draw.line(screen, (255, 255, 255), (line_pos_x, 0), (line_pos_x, height-1))
  pygame.draw.line(screen, (255, 255, 255), (0, line_pos_y), (width-1, line_pos_y))
  pygame.display.flip()

while(True):
  event = pygame.event.wait()

  if event.type == pygame.KEYDOWN:
    # Toggle input grab mode
    if event.key == toggle_grab_key:
      if pygame.event.get_grab() == True:
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        print("Mouse cursor released.")
      else:
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        print("Mouse cursor locked.")
    generate_and_send_keyboard_packet(event.key, "make")
    print(f"Key pressed: {pygame.key.name(event.key)}")
    key_pressed_list.append(event.key)
    update_screen()
    continue

  if event.type == pygame.KEYUP:
    generate_and_send_keyboard_packet(event.key, "break")
    print(f"Key released: {pygame.key.name(event.key)}")
    key_pressed_list.remove(event.key)
    update_screen()
    continue

  if event.type == pygame.MOUSEBUTTONDOWN:
    dz = 0
    if event.button == 1:
      btn_left = 1
    if event.button == 2:
      btn_middle = 1
    if event.button == 3:
      btn_right = 1
    if event.button == 4: # wheel UP
      dz = 1
    if event.button == 5: # wheel DOWN
      dz = -1
    packet = generate_mouse_packet(0, 0, dz, btn_left, btn_middle, btn_right)
    sock.sendto(packet, esp32_addr)
    update_screen()
    continue

  if event.type == pygame.MOUSEBUTTONUP:
    if event.button == 1:
      btn_left = 0
    if event.button == 2:
      btn_middle = 0
    if event.button == 3:
      btn_right = 0
    packet = generate_mouse_packet(0, 0, 0, btn_left, btn_middle, btn_right)
    sock.sendto(packet, esp32_addr)
    update_screen()
    continue

  if event.type == pygame.MOUSEMOTION:
    (dx, dy) = event.rel
    dx = dx * mouse_speed_factor
    dy = -dy * mouse_speed_factor
    mouse_counter_x = int(mouse_counter_x + dx)
    mouse_counter_y = int(mouse_counter_y + dy)
    now_ms = int(round(time.time() * 1000))
    if now_ms - last_time_reported_ms > report_interval_ms:
      packet = generate_mouse_packet(mouse_counter_x, mouse_counter_y, 0, btn_left, btn_middle, btn_right)
      sock.sendto(packet, esp32_addr)
      mouse_counter_x = 0
      mouse_counter_y = 0
      last_time_reported_ms = now_ms
    if pygame.mouse.get_visible():
      line_pos_x, line_pos_y = event.pos
    else:
      line_pos_x = (line_pos_x + dx) % width
      line_pos_y = (line_pos_y - dy) % height
    update_screen()
    continue

  if event.type == pygame.VIDEORESIZE:
    width, height = screen.get_size()
    update_screen()
    continue

  if event.type == pygame.QUIT:
    pygame.quit()
    sys.exit(0)





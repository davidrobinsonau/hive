#!/usr/bin/python3

import os
import pygame, sys
from pygame.locals import *
import time
from datetime import datetime

def FindDisplayDriver():
  for driver in ["fbcon", "directfb", "svgalib"]:
    if not os.getenv("SDL_VIDEODRIVER"):
      os.putenv("SDL_VIDEODRIVER", driver)
    try:
      pygame.display.init()
      return True
    except pygame.error:
      pass
  return False

def ShowClock(screen, width, height, thisTime):

  def Render(s, rgb, size):
    fnt = pygame.font.SysFont("Any", size * height // 1080)
    txt = fnt.render(s, True, rgb)
    return txt

  screen.fill((0,0,0))

  txtTim = Render(thisTime, (255,255,255),  728)
  h = ( height - txtTim.get_height() ) // 2
  w = ( width  - txtTim.get_width()  ) // 2
  screen.blit(txtTim,(w,h))

  pygame.display.update()

def Main():
  if not FindDisplayDriver():
    print("Failed to initialise display driver")
  else:
    width  = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN)
    #pygame.mouse.set_visible(False)
    lastTime = ""
    start_time = datetime.now()
    while True:
      curr_time = datetime.now()
      difference = start_time - curr_time
      thisTime = str(difference.seconds) + "." + str(difference.microseconds)
      #thisTime = difference.strftime("%M:%S.%f")[:-3]
      print(thisTime)
      if thisTime != lastTime:
        ShowClock(screen, width, height, thisTime)
        lastTime = thisTime
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
          kz = 0
          if event.type == KEYDOWN:
             kz = event.key
             if kz == K_ESCAPE:
                pygame.quit()
                sys.exit()
      time.sleep(0.1)

if __name__ == "__main__":
  pygame.init()
  Main()
  pygame.quit()

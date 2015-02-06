#!/usr/bin/env python

from __future__ import division
import os
import time
import gtk
import pygame
from pygame.locals import *
from pyscreenshot import grab as snapshot

BLACK = (0, 0, 0)


class Engine(object):
    def __init__(self):
        pygame.init()
        self._running = True
        self.render = True
        self.fps = 3
        self.ptx = 36
        self.line_width = 5
        self.prevRects = list()
        self.count = 0
        x, y, scwidth, scheight = gtk.Window().get_screen().get_monitor_geometry(0)
        self.bgname = 'background.jpg'
        im = snapshot(bbox=(0, 0, int(scwidth), int(scheight)))
        im.save(self.bgname)
        self.background = pygame.image.load(self.bgname)
        size = scwidth, scheight
        self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        self.ctrldown = False
        self.altdown = False
        self.prevRects = list()
        self.curRect = self.screen.get_rect()

    def crop(self, number):
        self.preAdjustment()
        # adjust x
        if number == 1: pass
        elif number in [4, 7]:
            self.curRect.x = self.curRect.left
        elif number in [2, 5, 8]:
            self.curRect.x += (self.curRect.width/3)
        elif number in [3, 6, 9]:
            self.curRect.x = (self.curRect.right - (self.curRect.width/3))
        # adjust y
        if number == 1: pass
        elif number in [2, 3]:
            self.curRect.y = self.curRect.top
        elif number in [4, 5, 6]:
            self.curRect.y += (self.curRect.bottom/3)
        elif number in [7, 8, 9]:
            self.curRect.y += ((self.curRect.bottom/3)*2)
        self.postAdjustment()

    def preAdjustment(self):
        self.prevRects.append(pygame.Rect(self.curRect))
        self.ptx -= 10
        if self.ptx < 10:
            self.ptx = 10

    def postAdjustment(self):
        self.curRect.width /= 3
        self.curRect.height /= 3
        self.line_width -= 1
        self.render = True

    def moveMouse(self, x, y):
        cmd = "xdotool mousemove {x} {y}".format(x=x, y=y)
        os.popen(cmd)

    def doubleClickMouse(self):
        os.popen("xdotool click 1")
        time.sleep(0.1)
        os.popen("xdotool click 1")

    def singleClickMouse(self):
        os.popen("xdotool click 1")

    def rightClickMouse(self):
        os.popen("xdotool click 3")

    def run(self):
        clock = pygame.time.Clock()
        while self._running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                self.on_event(event)
            if self.render:
                self.on_render()
                pygame.display.flip()
        self.cleanup()

    def on_render(self):
        self.screen.blit(self.background, (0, 0))
        DrawLines(self.screen, self.curRect, self.line_width, self.ptx)
        self.render = False  # Always last line of on_render function

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if len(self.prevRects) == 0:
                    self.stop()
                else:
                    self.curRect = self.prevRects.pop()
                    self.ptx += 10
                    self.line_width += 1
                    self.render = True

            elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                self.ctrldown = True

            elif event.key == pygame.K_LALT or event.key == pygame.K_LALT:
                self.altdown = True

            elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                pygame.quit()
                x, y = self.curRect.center
                self.moveMouse(x, y)
                if self.altdown:
                    self.rightClickMouse()
                elif self.ctrldown:
                    self.singleClickMouse()
                else:
                    self.doubleClickMouse()
                self.stop()

            else:
                keyname = pygame.key.name(event.key)
                keyname = keyname.replace('[', "")
                keyname = keyname.replace("]", "")
                if keyname == "0": return
                print(type(keyname), keyname)
                try:
                    number = int(keyname)
                except ValueError: return

                self.crop(number)

        elif event.type==KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                self.ctrldown = False
            elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                self.altdown = False

    def stop(self):
        self._running = False

    def cleanup(self):
        pygame.quit()


def DrawLines(screen, r, lw, ptx):
    ##Bounding Box
    pygame.draw.rect(screen, BLACK, r, lw)
    ##Horizontal
    pygame.draw.line(screen, BLACK, (r.left, r.bottom-(2/3*r.height)), (r.right, r.bottom-(2/3*r.height)), lw)
    pygame.draw.line(screen, BLACK, (r.left, (r.top+(2/3*r.height))), (r.right, (r.top+(2/3*r.height))), lw)
    ##Vertical
    pygame.draw.line(screen, BLACK, ((r.right-r.width/3), r.top), ((r.right-r.width/3), r.bottom), lw)
    pygame.draw.line(screen, BLACK, ((r.right-(r.width/3*2)), r.top), ((r.right-r.width/3*2), r.bottom), lw)

    font = pygame.font.Font(None, ptx)
    text1 = font.render("1", 1, BLACK)
    text2 = font.render("2", 1, BLACK)
    text3 = font.render("3", 1, BLACK)
    text4 = font.render("4", 1, BLACK)
    text5 = font.render("5", 1, BLACK)
    text6 = font.render("6", 1, BLACK)
    text7 = font.render("7", 1, BLACK)
    text8 = font.render("8", 1, BLACK)
    text9 = font.render("9", 1, BLACK)
    screen.blit(text1, (((r.left+(r.width/6)-ptx/3)), (r.top+(r.height/6))-ptx/3))
    screen.blit(text2, ((r.centerx-(ptx/3)), (r.top+r.height/6)-ptx/3))
    screen.blit(text3, (((r.right-(r.width/6)-ptx/3)), (r.top+(r.height/6))-ptx/3))
    screen.blit(text4, (((r.left+(r.width/6)-ptx/3)), (r.centery-ptx/3)))
    screen.blit(text5, ((r.centerx-ptx/3), (r.centery-ptx/3)))
    screen.blit(text6, (((r.right-(r.width/6)-ptx/3)), (r.centery-ptx/3)))
    screen.blit(text7, (((r.left+(r.width/6)-ptx/3)), (r.bottom-(r.height/6))-ptx/3))
    screen.blit(text8, (((r.centerx-ptx/3), (r.bottom-(r.height/6))-ptx/3)))
    screen.blit(text9, (((r.right-(r.width/6)-ptx/3)), (r.bottom-(r.height/6))-ptx/3))

if __name__ == "__main__":
    engine = Engine()
    engine.run()

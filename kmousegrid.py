from __future__ import division
import os, sys, pygame, gtk
import pyscreenshot as pshot
from pygame.locals import *

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
        im=pshot.grab(bbox=(0,0,int(scwidth),int(scheight)))
        im.save(self.bgname)
        self.background=pygame.image.load(self.bgname)
        size = scwidth, scheight
        self.screen=pygame.display.set_mode(size, pygame.NOFRAME)

        self.prevRects = list()
        self.curRect = self.screen.get_rect()

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
        self.render = False #Always last line of on_render function

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
                    
            if event.key == K_1 or event.key == K_KP1:
                self.preAdjustment()
                self.postAdjustment()

            elif event.key == K_2 or event.key == K_KP2:
                self.preAdjustment()
                self.curRect.x += (self.curRect.width/3)
                self.curRect.y = self.curRect.top
                self.postAdjustment()

            elif event.key == K_3 or event.key == K_KP3:
                self.preAdjustment()
                self.curRect.x = (self.curRect.right-(self.curRect.width/3))
                self.curRect.y = self.curRect.top
                self.postAdjustment()

            elif event.key == K_4 or event.key == K_KP4:
                self.preAdjustment()
                self.curRect.x = self.curRect.left
                self.curRect.y += (self.curRect.bottom/3)
                self.postAdjustment()

            elif event.key == K_5 or event.key == K_KP5:
                self.preAdjustment()
                self.curRect.x += (self.curRect.width/3)
                self.curRect.y += (self.curRect.height/3)
                self.postAdjustment()

            elif event.key == K_6 or event.key == K_KP6:
                self.preAdjustment()
                self.curRect.x = (self.curRect.right-(self.curRect.width/3))
                self.curRect.y += (self.curRect.height/3)
                self.postAdjustment()
                
            elif event.key == K_7 or event.key == K_KP7:
                self.preAdjustment()
                self.curRect.x = self.curRect.left
                self.curRect.y += ((self.curRect.bottom/3)*2)
                self.postAdjustment()
                
            elif event.key == K_8 or event.key == K_KP8:
                self.preAdjustment()
                self.curRect.x += (self.curRect.width/3)
                self.curRect.y += ((self.curRect.height/3)*2)
                self.postAdjustment()
                
            elif event.key == K_9 or event.key == K_KP9:
                self.preAdjustment()
                self.curRect.x = (self.curRect.right-(self.curRect.width/3))
                self.curRect.y += ((self.curRect.height/3)*2)
                self.postAdjustment()

    def stop(self):
        self._running = False

    def cleanup(self):
        pygame.quit()


def DrawLines(screen, r, lw, ptx):
    print "Left, Right, Height, Width, X, Y = "+str(r.left)+", "+str(r.right)+", "+str(r.height)+", "+str(r.width)+", "+str(r.x)+", "+str(r.y)
    pygame.draw.rect(screen, BLACK, r, lw)
    ##Horizontal
    pygame.draw.line(screen, BLACK, (r.left, r.bottom-(2/3*r.height)), (r.right,r.bottom-(2/3*r.height)) , lw)
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
    screen.blit(text1, (((r.left+(r.width/6)-ptx/3)),(r.top+(r.height/6))-ptx/3))
    screen.blit(text2, ((r.centerx-(ptx/3)), (r.top+r.height/6)-ptx/3))
    screen.blit(text3, (((r.right-(r.width/6)-ptx/3)), (r.top+(r.height/6))-ptx/3))
    screen.blit(text4, (((r.left+(r.width/6)-ptx/3)),(r.centery-ptx/3)))
    screen.blit(text5, ((r.centerx-ptx/3),(r.centery-ptx/3)))
    screen.blit(text6, (((r.right-(r.width/6)-ptx/3)), (r.centery-ptx/3)))
    screen.blit(text7, (((r.left+(r.width/6)-ptx/3)), (r.bottom-(r.height/6))-ptx/3))
    screen.blit(text8, (((r.centerx-ptx/3), (r.bottom-(r.height/6))-ptx/3)))
    screen.blit(text9, (((r.right-(r.width/6)-ptx/3)), (r.bottom-(r.height/6))-ptx/3))

if __name__ == "__main__":
    engine = Engine()
    engine.run()

import pygame, sys
from pygame.locals import *
import random
import math

pygame.init()

FPS = 30
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.mouse.set_visible(False)

DEBUG_MODE = False
GRAY  = (128, 128, 128)
BLACK = (  0,   0,   0)
SPEED = 25
BALL_SPEED = 300
BALL_ANGLE = 155

def main():
    SCORE_ONE = 0
    SCORE_TWO = 0
    elapsed = 0.
    bar_one = Bar(DISPLAYSURF.get_width() - 100, 540, SPEED)
    bar_two = Bar(100, 540, SPEED)
    ball = Ball(DISPLAYSURF.get_width() / 2, 800, BALL_SPEED, 0, 0, BALL_ANGLE)
    while True:
        DISPLAYSURF.fill(BLACK)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        FONT_SCORE = pygame.font.Font('freesansbold.ttf', 45)
        score_surface = FONT_SCORE.render(
            '%r   %r' % (SCORE_ONE, SCORE_TWO), True, GRAY)
        DISPLAYSURF.blit(score_surface, (DISPLAYSURF.get_width() / 2 - 55, 25))

        elapsed = fps_clock.tick(FPS)
        sec = elapsed / 1000.0
        ball.play(sec)
        bar_one.play()
        bar_two.move()

        diff_angle = 90 - ball.THETA
        if DEBUG_MODE:
            COORDS = pygame.font.Font('freesansbold.ttf', 40)
            bar_two_x = COORDS.render(
                'bar_two.x: %r' % (bar_two.x), True, GRAY)
            DISPLAYSURF.blit(bar_two_x, (500, 85))
            ball_x = COORDS.render(
                'ball.x: %r' % (ball.x), True, GRAY)
            DISPLAYSURF.blit(ball_x, (500, 125))
            bar_two_y = COORDS.render(
                'bar_two.y: %r' % (bar_two.y), True, GRAY)
            DISPLAYSURF.blit(bar_two_y, (500, 165))
            ball_y = COORDS.render(
                'ball.y: %r' % (ball.y), True, GRAY)
            DISPLAYSURF.blit(ball_y, (500, 205))
            ball_diff_y = COORDS.render(
                'bar_two.y - ball.y: %r' % (ball.y - bar_two.y), True, GRAY)
            DISPLAYSURF.blit(ball_diff_y, (500, 245))

        if (abs(bar_one.x - ball.x) < 14 and
                0 < (ball.y - bar_one.y) < 130):
            if ball.vy < 0:
                ball.THETA += 2 * diff_angle
            elif ball.vy > 0:
                ball.THETA += 2 * diff_angle
        if (abs(bar_two.x - ball.x) < 14 and
                0 < (ball.y - bar_two.y) < 130):
            if ball.vy < 0:
                ball.THETA += 2 * diff_angle
            elif ball.vy > 0:
                ball.THETA += 2 * diff_angle

        bar_one.draw()
        bar_two.draw()
        if ball.x < 10:
            ball.x, ball.y = DISPLAYSURF.get_width() / 2, 800
            SCORE_TWO += 1
        if ball.x > DISPLAYSURF.get_width():
            ball.x, ball.y = DISPLAYSURF.get_width() / 2, 800
            SCORE_ONE += 1
        ball.draw()
        pygame.display.update()


class Bar(object):

    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v

    def draw(self):
        pygame.draw.rect(
            DISPLAYSURF, GRAY, ((self.x, self.y, 15, 130))
        )

    def move(self):
        self.y += self.v
        if self.y <= 0:
            self.v = SPEED
        elif self.y >= 950:
            self.v = -SPEED

    def play(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y >= 10:
            self.y -= SPEED
        elif keys[pygame.K_DOWN] and self.y <= 940:
            self.y += SPEED


class Ball(object):

    def __init__(self, x, y, v, vx, vy, THETA):
        self.x = x
        self.y = y
        self.v = v
        self.THETA = THETA

    def draw(self):
        pygame.draw.rect(
            DISPLAYSURF, GRAY, ((self.x, self.y, 15, 15))
        )

    def play(self, sec):
        self.vx = self.v * math.cos(self.THETA * math.pi/180)
        self.vy = self.v * math.sin(self.THETA * math.pi/180)
        self.x = self.x + self.vx * sec
        self.y = self.y - self.vy * sec

        add_angle = 360 - self.THETA
        if self.vx > 0:
            if self.y <= -10 and self.vy > 0:
                self.THETA += 2 * add_angle
            elif self.y >= 1070 and self.vy < 0:
                self.THETA += 2 * add_angle
        if self.vx < 0:
            if self.y <= -10 and self.vy > 0:
                self.THETA += 2 * add_angle
            elif self.y >= 1070 and self.vy < 0:
                self.THETA += 2 * add_angle


if __name__=='__main__':
    main()

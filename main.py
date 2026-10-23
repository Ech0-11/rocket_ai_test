import pygame
import math

fps = 200
width = 900
height = 700
target = (width // 2, 50)

darkBlue = (10,0,60)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)

DT = 1 / fps
THRUST = 300
TURN_SPEED = 3.0
DRAG = 0.5


class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = 0

    def draw(self, surface, color = white):

        nose_x = self.x + math.sin(self.angle) * 18
        nose_y = self.y - math.cos(self.angle) * 18
        left_x = self.x + math.sin(self.angle - 2.3) * 16
        left_y = self.y - math.cos(self.angle - 2.3) * 16
        right_x = self.x + math.sin(self.angle + 2.3) * 16
        right_y = self.y - math.cos(self.angle + 2.3) * 16
        back_x = self.x + math.sin(self.angle + math.pi) * 6
        back_y = self.y - math.cos(self.angle + math.pi) * 6

        nose_pos = (nose_x, nose_y)
        left_pos = (left_x, left_y)
        back_pos = (back_x, back_y)
        right_pos = (right_x, right_y)

        pygame.draw.polygon(surface, color, [nose_pos, left_pos, back_pos, right_pos])
        
        # pygame.draw.circle(surface, white, (self.x, self.y), 4)
        # pygame.draw.circle(surface, red, (nose_x, nose_y), 4)
        # pygame.draw.circle(surface, green, (left_x, left_y), 4)
        # pygame.draw.circle(surface, green, (right_x, right_y), 4)
        # pygame.draw.circle(surface, blue, (back_x, back_y), 4)
    
    def update(self, thrust, turn, dt):

        dragValue = math.exp(-DRAG * dt)

        self.angle += turn * TURN_SPEED * dt
        self.vx += math.sin(self.angle) * thrust * THRUST * dt
        self.vy -= math.cos(self.angle) * thrust * THRUST * dt
        self.vx *= dragValue
        self.vy *= dragValue

        if self.x >= width:
            self.vx = (abs(self.vx) * 0.9) * -1
        elif self.x <= 0: 
            self.vx = (abs(self.vx) * 0.9) * 1
        if self.y >= height:
            self.vy = (abs(self.vy) * 0.9) * -1
        elif self.y <= 0: 
            self.vy = (abs(self.vy) * 0.9) * 1

        self.x += self.vx * dt
        self.y += self.vy * dt

pygame.init()

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

rocket = Rocket(width // 2, height - 50)
# print(rocket.x,rocket.y)

running = True
while running:

    thrust = 0
    turn = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            target = event.pos

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: thrust = 1
    else: thrust = 0
    if keys[pygame.K_a]: turn = -1
    elif keys[pygame.K_d]: turn = 1
    else: turn = 0
    
    rocket.update(thrust, turn, DT)
    
    screen.fill(darkBlue)
    pygame.draw.circle(screen, red, target, 5)
    rocket.draw(screen)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
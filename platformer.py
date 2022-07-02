from pygame.math import Vector2
import pygame,sys

width=1024
height=600
tile_size=64
RED=(255,0,0)
camera_x=0
camera_y=0
lastpos=0
lastpos_y=0

pygame.init()
screen=pygame.display.set_mode((width,height))
clock=pygame.time.Clock()


map=[
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

class player():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.pos=Vector2(self.x,self.y)
        self.friction=-0.2
        self.acc=Vector2(0,0.6)
        self.speed=Vector2(0,0)
        self.surface=pygame.Surface((tile_size//2,tile_size))
        self.hitbox=pygame.Rect(self.pos.x,self.pos.y,tile_size//2,tile_size)
        self.jump=False
        self.jumpcounter=2

    def draw_player(self,window):
        self.move_player()
        self.surface.fill((0,255,0))
        #pygame.draw.rect(window,pygame.Color('green'),self.hitbox)
        window.blit(self.surface,(self.hitbox.x-camera_x,self.hitbox.y-camera_y))
    
    def apply_gravity(self):
        #Y axis
        self.speed+=self.acc
        self.hitbox.y+=self.speed.y+self.acc.y*0.5
    

    def move_player(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.speed.x=5
        elif keys[pygame.K_LEFT]:
            self.speed.x=-5
        else:
            self.speed.x=0

        #self.hitbox.center=self.pos


    def v_collisions(self,tile_list):
        self.apply_gravity()
        for rects in tile_list:
            #hitbox2=pygame.Rect(self.hitbox.x,self.hitbox.y+self.dy,tile_size//2,tile_size)
            if rects.colliderect(self.hitbox):
                if self.speed.y>0:
                    self.jump=False
                    self.speed.y=0
                    self.hitbox.bottom=rects.top
                    self.jumpcounter=2

                if self.speed.y<0:
                    self.speed.y=0
                    self.hitbox.top=rects.bottom


    def h_collisions(self,tile_list):
        global camera_x
        #X axis
        self.hitbox.x+=self.speed.x
        for rects in tile_list:
            if rects.colliderect(self.hitbox):
                if self.speed.x>0:
                    self.speed.x=0
                    self.acc.x=0
                    self.hitbox.right=rects.left
                    player1.jumpcounter=2

                if self.speed.x<0:
                    self.speed.x=0
                    self.acc.x=0
                    self.hitbox.left=rects.right        

def draw_map(map,window,char):
    global camera_x,camera_y
    x=-char.hitbox.centerx + width//2
    y=-char.hitbox.centery + height//2
    surface=pygame.Surface((2000,2000))
    surface.set_colorkey((0,0,0))
    x=min(0,x)
    y=min(0,y)
    x=max(-(len(map[0])*tile_size-width),x)
    y=max(-(len(map)*tile_size-height),y)
    camera_x-=(x+camera_x)//20
    camera_y-=(y+camera_y)//20  
    hit_list=[]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j]==1:
                rect=pygame.Rect((j)*tile_size,i*tile_size,tile_size,tile_size)
                hit_list.append(rect)
                pygame.draw.rect(surface,RED,rect)
    window.blit(surface,(0-camera_x,0-camera_y))
    return hit_list


player1=player(600,600)


def game(window,clock):
    gameover=False
    while not gameover:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP :
                    if player1.jumpcounter>0: 
                        player1.speed.y=-15
                        player1.jumpcounter-=1
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_UP:
                    print("released")
                    if player1.jumpcounter==1:
                       if player1.speed.y<-2: 
                            player1.speed.y=-2
        screen.fill(pygame.Color('white'))
        hits=draw_map(map,screen,player1)
        player1.draw_player(screen)
        player1.h_collisions(hits)
        player1.v_collisions(hits)
        pygame.display.flip()
        clock.tick(60)

game(screen,clock)

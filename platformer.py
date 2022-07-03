from pygame.math import Vector2
import pygame,sys
from water import *

width=1024
height=600
tile_size=64
RED=(255,0,0)
grey=(100,100,100)
camera_x=0
camera_y=0
lastpos=0
lastpos_y=0

pygame.init()
screen=pygame.display.set_mode((width,height))
Game_surface=pygame.Surface((2000,2000))
water_surf=pygame.Surface((1500,1500))
water_surf.set_colorkey((0,0,0))
water_surf.set_alpha(120)
water_surf.fill((0,0,0))

clock=pygame.time.Clock()

map=[
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2,2,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,1,2,2,2,2,2,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

class player():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.pos=Vector2(self.x,self.y)
        self.friction=1
        self.acc=Vector2(1,0.6)
        self.speed=Vector2(0,0)
        self.momentum=5
        self.dir=0
        self.surface=pygame.Surface((tile_size//2,tile_size))
        self.hitbox=pygame.Rect(self.pos.x,self.pos.y,tile_size//2,tile_size)
        self.jump=False
        self.jumpcounter=2

    def draw_player(self,window):
        self.move_player()
        self.surface.fill((0,255,0))
        window.blit(self.surface,(self.hitbox.x-camera_x,self.hitbox.y-camera_y))
    
    def apply_gravity(self):
        #Y axis
        self.speed.y+=self.acc.y
        self.pos.y+=self.speed.y+self.acc.y*0.5
        self.hitbox.y=int(self.pos.y)
    

    def move_player(self):
        
        keys=pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.dir=1
        elif keys[pygame.K_LEFT]:
            self.dir=-1
        else:
            self.dir=0
        
        if self.dir!=0:
            self.speed.x=lerp(self.speed.x,self.momentum*self.dir,self.acc.x)
        else:
            self.speed.x=lerp(self.speed.x,0,self.friction)


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
            self.pos.y=self.hitbox.y


    def h_collisions(self,tile_list):
        #X axis
        self.pos.x+=self.speed.x
        self.hitbox.x=int(self.pos.x)
        for rects in tile_list:
            if rects.colliderect(self.hitbox):
                if self.speed.x>0:
                    self.speed.x=0
                    #self.acc.x=0
                    self.hitbox.right=rects.left
                    player1.jumpcounter=2

                if self.speed.x<0:
                    self.speed.x=0
                    #self.acc.x=0
                    self.hitbox.left=rects.right  
            self.pos.x=self.hitbox.x
            
def display_fps(window,clock):
    font=pygame.font.Font(None,20)
    fps=font.render(str(int(clock.get_fps())),True,(255,255,255))
    window.blit(fps,(10,10))

def lerp(start_value,end_value,amount):
    return start_value*(1-amount)+end_value*amount

def draw_map(map,window,char,game_surface):
    global camera_x,camera_y
    x=-char.hitbox.centerx + width//2
    y=-char.hitbox.centery + height//2
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
                if (j*tile_size-camera_x>-tile_size and j*tile_size-camera_x<width+tile_size) and (i*tile_size-camera_y>-tile_size and i*tile_size-camera_y<height+tile_size)  :
                    rect=pygame.Rect((j)*tile_size,i*tile_size,tile_size-5,tile_size-5)
                    hit_list.append(rect)
                    pygame.draw.rect(game_surface,RED,rect)
    
    return hit_list

def find_water(list):
    for i in range(len(map)):
        j=0
        while j<len(map[0]):
            a=j
            if map[i][j]==2:
                print(j)
                while(map[i][a]==2):
                    a+=1
                list.append(water(j*tile_size,(i+1/2)*tile_size,tile_size,8,a-j))
                j=a-1
            j+=1                          
                
def draw_water(list,player_rect,player_speed_y,player_speed_x,water_surf):
    global camera_x,camera_y
    water_surf.fill((0,0,0))
    for water in list:
       water.check_collision(player_rect,player_speed_y,player_speed_x)
       water.wave_spread(0.85,0.045)
       poly_points,water_lines=(water.water_polygon_list(tile_size//2,camera_x,camera_y))
       pygame.draw.polygon(water_surf,(23, 135, 250),poly_points)
       pygame.draw.lines(screen,(255, 255, 255),False,water_lines,2)
       screen.blit(water_surf,(0-camera_x,0-camera_y))
                   
def game(clock):
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
                    if player1.jumpcounter==1:
                       if player1.speed.y<-2: 
                            player1.speed.y=-2
        screen.fill((0,0,0))
        Game_surface.fill((0,0,0))
        hits=draw_map(map,screen,player1,Game_surface)
        screen.blit(Game_surface,(0-camera_x,0-camera_y))
        player1.draw_player(screen)
        player1.h_collisions(hits)
        player1.v_collisions(hits)
        draw_water(water_list,player1.hitbox,player1.speed.y,player1.speed.x,water_surf)
        display_fps(screen,clock)
        pygame.display.flip()
        clock.tick(60)
        
water_list=[]

player1=player(600,600)
        
#main 

find_water(water_list)
game(clock)

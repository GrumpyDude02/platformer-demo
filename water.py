
import pygame
from pygame.math import Vector2 as vc


class spring():
    def __init__(self,x,y,speed):
        self.pos=vc(x,y)
        self.y=y
        self.speed=speed
        self.rect=pygame.Rect(self.pos.x,self.pos.y,2,2)
    
    def oscillation(self,dampening,target):
        k=0.015
        x=self.pos.y-self.y
        acceleration=(-k)*x
        self.pos.y+=self.speed
        self.speed+=acceleration-self.speed*dampening
    

class water():
    def __init__(self,x,y,tile_size,spacing,length):
        self.x=x
        self.y=y
        self.tile_size=tile_size
        self.spacing=spacing
        self.length=length
        self.springs_list=[spring(self.x,self.y,0)]
        self.right=[]
        self.left=[]
        for i in range(0,int((length*tile_size/spacing))):
            self.springs_list.append(spring(self.springs_list[i].pos.x+spacing,self.y,0))
        for i in range(0,len(self.springs_list)):
            self.left.append(0)
            self.right.append(0)
    
    def wave_spread(self,spread,damp):
        for i in range(len(self.springs_list)):
            self.springs_list[i].oscillation(damp,self.y)
        for i in range(len(self.springs_list)):
            if i>0:
                self.left[i]=spread*(self.springs_list[i].pos.y-self.springs_list[i-1].pos.y)
                self.springs_list[i-1].speed+=self.left[i]
            if i<len(self.springs_list)-1:
                self.right[i]=spread*(self.springs_list[i].pos.y-self.springs_list[i+1].pos.y)
                self.springs_list[i+1].speed+=self.right[i]
         
                 
    def water_polygon_list(self,bounding_y):
        self.water_polygon=[(self.x-1+self.tile_size*self.length,self.y+self.tile_size-bounding_y),(self.x-1,self.y+self.tile_size-bounding_y)]
        for i in range(len(self.springs_list)):
            self.water_polygon.append((self.springs_list[i].pos.x,self.springs_list[i].pos.y))
        return self.water_polygon
    
    def check_collision(self,ob_rect,ob_speed_y,ob_speed_x):
        for i in range(len(self.springs_list)):
            if ob_rect.colliderect(self.springs_list[i].rect):
                self.springs_list[i].speed+=ob_speed_y*0.08
                self.springs_list[i].speed-=abs(ob_speed_x)*0.03
                print('collide')
                
                
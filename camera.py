import pygame

class Camera():
    def __init__(self,camera_x,camera_y,SC_width,SC_height,left,right,top,bottom) :
        self.pos=pygame.math.Vector2(camera_x,camera_y)
        self.sc_width=SC_width
        self.sc_height=SC_height
        
        #atributes for box camera
        
        self.camera_borders=[left,right,top,bottom]
        width=self.sc_width-(self.camera_borders[0]+self.camera_borders[1])
        height=self.sc_height-(self.camera_borders[2]+self.camera_borders[3])
        self.camera_box=pygame.Rect(self.camera_borders[0],self.camera_borders[2],width,height)
    
    def center_camera(self,player_rect,tile_size,lag,map):
        x=-player_rect.centerx + self.sc_width//2
        y=-player_rect.centery+ self.sc_height//2
        x=min(0,x)
        y=min(0,y)
        x=max(-(len(map[0])*tile_size-self.sc_width),x)
        y=max(-(len(map)*tile_size-self.sc_height),y)
        self.pos.x-=(x+self.pos.x)//lag
        self.pos.y-=(y+self.pos.y)//lag
        
    def box_camera(self,player_rect,tile_size,map):
        
        if self.camera_box.left>player_rect.left:
            self.camera_box.left=player_rect.left
        
        if self.camera_box.right<player_rect.right:
            self.camera_box.right=player_rect.right
            
        if self.camera_box.top>player_rect.top:
            self.camera_box.top=player_rect.top
        
        if self.camera_box.bottom<player_rect.bottom:
            self.camera_box.bottom=player_rect.bottom
        
          
        
        self.pos.x=(self.camera_box.left-self.camera_borders[0])
        self.pos.y=(self.camera_box.top-self.camera_borders[2])
        
        print(self.pos)
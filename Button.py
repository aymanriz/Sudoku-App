import pygame


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)
class Button:
    def __init__(self,x,y,msg,font_size=16):
        self.x=x
        self.y=y
        self.msg = msg
        font=pygame.font.Font("freesansbold.ttf",font_size)
        self.text=font.render(msg,True,BLUE,WHITE)
        self.rect=self.text.get_rect()
        self.width=self.rect.width
        self.height=self.rect.height

    def is_clicked(self):
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        if self.x<=mouse[0]<=self.x+self.width and self.y<=mouse[1]<=self.y+self.height:#if mouse is over the button
            if click[0]==1:#if there is a left mouse click
                return True
        return False

    def draw(self,win):
        pygame.draw.rect(win,BLACK,(self.x,self.y,self.width,self.height),4)
        win.blit(self.text, (self.x, self.y))





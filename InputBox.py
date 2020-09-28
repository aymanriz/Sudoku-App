import pygame
TURQUOISE = (64, 224, 208)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class InputBox:
    def __init__(self,x,y,width,val):
        self.font=pygame.font.SysFont("Arial",18)
        self.x=x
        self.y=y
        self.width = width
        self.val = val
        self.selected=False
        self.color=BLACK

    def select(self):
        self.selected=True
        self.color=TURQUOISE
    def unselect(self):
        self.selected=False
        self.color=BLACK

    def is_clicked(self):
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        if self.x<=mouse[0]<=self.x+self.width and self.y<=mouse[1]<=self.y+self.width:#if mouse is over the button
            if click[0]==1:#if there is a left mouse click
                return True
        return False

    def draw(self,win):
        rect=pygame.Rect(self.x,self.y,self.width,self.width)
        pygame.draw.rect(win,self.color,rect,3)
        msg=str(self.val) if self.val!=0 else ""
        win.blit(self.font.render(msg, True, BLACK),(self.x+self.width//4,self.y+self.width//3))
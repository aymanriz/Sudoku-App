import pygame
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)

class CheckBox:
    def __init__(self,x,y,width):
        self.x = x
        self.y = y
        self.width = width
        self.rect = pygame.Rect(x,y,width,width)
        self.color=WHITE
        self.clicked=False

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0]==1 :  # if mouse is over the button
            if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.width:
                return True
        return False

    def draw(self, win):
        pygame.draw.rect(win, BLACK, self.rect,3)
        win.fill(self.color,self.rect)

    def click(self):
        if self.clicked:
            self.clicked=False
            self.color=WHITE
        else:
            self.clicked=True
            self.color=GREEN


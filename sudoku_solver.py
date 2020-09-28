import random
import pygame
import time
from Sudoku_app.Button import Button
from Sudoku_app.CheckBox import CheckBox
from Sudoku_app.InputBox import InputBox

pygame.init()
WIDTH = 450
HEIGHT=550
WIN = pygame.display.set_mode((WIDTH+100, HEIGHT))
pygame.display.set_caption("Sudoku App")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


pygame_nums={pygame.K_0:0,pygame.K_DELETE:0,pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,pygame.K_5:5,pygame.K_6:6,pygame.K_7:7,pygame.K_8:8,pygame.K_9:9}
subgrid_dict={0:0,1:0,2:0,3:1,4:1,5:1,6:2,7:2,8:2}
dict={0:[0,1,2],1:[3,4,5],2:[6,7,8]}


####generating a unique random sudoku board####

def fill(grid):
    cell=find_min_cell(grid)
    if not cell:
        return True
    x,y=cell
    poss=grid[x][y].get_possibilities(grid)
    random.shuffle(poss)
    for p in poss:
        grid[x][y].val=p
        if fill(grid):
            return True
    grid[x][y].val = 0
    return False

cnt=0
def create_sudoku(lim):
    global cnt
    grid=make_empty_grid()
    fill(grid)
    pos = [(x, y) for x in range(9) for y in range(9)]
    random.shuffle(pos)
    empty=0
    for (x,y) in pos:
        if empty==lim:
            break
        tmp=grid[x][y].val
        grid[x][y].val=0
        temp_grid=deepcopy(grid)
        cnt=0
        if not_unique(temp_grid):
            grid[x][y].val=tmp
        else:
            empty+=1
    for row in grid:
        for cell in row:
            cell.can_be_changed=True if cell.val==0 else False
    return grid

def not_unique(grid):
    global cnt
    cell = find_min_cell(grid)
    if not cell:
        cnt+=1
        if cnt>=2:
            return True
        return False
    x, y = cell
    poss = grid[x][y].get_possibilities(grid)
    random.shuffle(poss)
    for p in poss:
        grid[x][y].val = p
        if not_unique(grid):
            return True
    grid[x][y].val = 0
    return False

def deepcopy(grid):
    res=[]
    for i in range(len(grid)):
        res.append([])
        for j in range(len(grid)):
            res[i].append(Cell(i,j,grid[i][j].val,50))
    return res


                     ####end########

class Cell:

    def __init__(self,x,y,val,width):
        self.font=pygame.font.SysFont("Arial",18)
        self.x=x
        self.y=y
        self.val=val
        self.box_rows=dict[subgrid_dict[x]]
        self.box_cols=dict[subgrid_dict[y]]
        self.width=width
        self.color=WHITE
        self.can_be_changed=True if val==0 else False
        self.selected = False
        self.changed=False

    def get_possibilities(self,grid):
        res=[x for x in range(0,10)]
        taken=self.get_vals_in_row(grid)
        taken.update(self.get_vals_in_box(grid))
        taken.update(self.get_vals_in_col(grid))
        for x in taken:
            if x in res:
                res.remove(x)
        if 0 in res:
            res.remove(0)
        return res

    def get_vals_in_row(self,grid):
        res={x.val for x in grid[self.x]}
        return res

    def get_vals_in_col(self,grid):
        res=set()
        for i in range(len(grid)):
            res.add(grid[i][self.y].val)
        return res

    def get_vals_in_box(self,grid):
        res=set()
        for i in self.box_rows:
            for j in self.box_cols:
                res.add(grid[i][j].val)
        return res

    def make_green(self):
        self.color=GREEN

    def make_red(self):
        self.color=RED

    def make_white(self):
        self.color=WHITE

    def select(self):
        self.selected=True
        self.color=TURQUOISE
    def unselect(self):
        self.selected=False
        self.color=WHITE

    def draw(self,win):
        rect=pygame.Rect(self.y*self.width,self.x*self.width+40,self.width,self.width)
        pygame.draw.rect(win,self.color,rect,5)
        msg=str(self.val) if self.val!=0 else ""
        win.blit(self.font.render(msg, True, BLACK),(self.y*self.width+self.width//2,self.x*self.width+self.width//2+40))




def update_selected(grid,inputBox):
    gap=WIDTH//9
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if click[0]==1:
        if 0<=mouse[0]<=WIDTH and 40<=mouse[1]<WIDTH+40:
            x,y=((mouse[1]-40)//gap,mouse[0]//gap)
            for i in range(len(grid)):
                for j in range(len(grid)):
                    if (i,j)==(x,y):
                        grid[i][j].select()
                    else:
                        grid[i][j].unselect()
            inputBox.unselect()
        else:
            for row in grid:
                for cell in row:
                    cell.unselect()
            if inputBox.is_clicked():
                inputBox.select()
            else:
                inputBox.unselect()


def get_selected(grid):
    for row in grid:
        for cell in row:
            if cell.selected:
                return cell
    return None


def find_cell(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].val==0:
                return i,j
    return False

def find_min_cell(grid):
    min=10
    x,y=0,0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].val==0:
                if len(grid[i][j].get_possibilities(grid))<min:
                    min=len(grid[i][j].get_possibilities(grid))
                    x,y=i,j
    if min==10:
        return False
    else:
        return x,y


def backtracking_soduko(draw,grid,min,steps):
    if min:
        cell=find_min_cell(grid)
    else:
        cell=find_cell(grid)
    if not cell:
        return True
    else:
        x,y=cell
        poss = grid[x][y].get_possibilities(grid)
        for p in poss:
            grid[x][y].val=p
            if steps:
                grid[x][y].make_green()
                draw()
                time.sleep(0.2)
            if backtracking_soduko(draw,grid,min,steps):
                return True
            if steps:
                grid[x][y].make_red()
                draw()
                time.sleep(0.2)
        grid[x][y].val=0
        if steps:
            grid[x][y].make_red()
            draw()
            time.sleep(0.2)
        return False


def make_empty_grid():
    grid=[]
    gap=WIDTH//9
    for i in range(9):
        grid.append([])
        for j in range(9):
            grid[i].append(Cell(i,j,0,gap))
    return grid

def draw_grid_lines(win,grid,width):
    gap=width//9
    for i in range(10):
        if i%3==0:
            w=3
        else:
            w=1
        pygame.draw.line(win,BLACK, (0,i*gap+40), (width,i*gap+40),w)#HORIZONTAL
        pygame.draw.line(win,BLACK,(i*gap,40),(i*gap,width+40),w)#VERTICAL

def draw(win,grid,width,buttons):
    win.fill(WHITE)
    font = pygame.font.Font("freesansbold.ttf", 16)
    welcome_msg = font.render("Insert a valid sudoku board,or press generate to generate a new board! ", True, BLUE, WHITE)
    number_of_empty_cells=font.render("Number of empty cells :", True, BLUE, WHITE)
    stepsText=font.render("Show Steps",True,BLUE,WHITE)
    MVR_heuristic=font.render("Use MVR",True,BLUE,WHITE)
    MVR_heuristic2=font.render("Heuristic",True,BLUE,WHITE)
    win.blit(welcome_msg, (0, 10))
    win.blit(number_of_empty_cells,(0,515))
    win.blit(stepsText,(454,176))
    win.blit(MVR_heuristic,(462,225))
    win.blit(MVR_heuristic2,(462,240))

    for button in buttons:
        button.draw(win)

    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid_lines(win,grid,width)
    pygame.display.update()

def main():

    grid=make_empty_grid()
    user_defined_grid=True
    generateBTN = Button(244, 515, "Generate")
    clearBTN = Button(344, 515, "Clear Board")
    inputBox=InputBox(190,503,40,0)
    solveBTN=Button(468,298,"Solve",24)
    StepsBox=CheckBox(494,195,10)
    MVRbox=CheckBox(494,260,10)
    buttons=[generateBTN,clearBTN,inputBox,solveBTN,StepsBox,MVRbox]

    run=True

    while run:
        update_selected(grid,inputBox)
        cell=get_selected(grid)
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key in pygame_nums:
                    if cell:
                        if cell.can_be_changed:
                            if pygame_nums[event.key] in cell.get_possibilities(grid) or pygame_nums[event.key]==0:#check if its a valid input
                                cell.val=pygame_nums[event.key]
                                cell.changed=True
                            else:#little graphics incase input is not valid
                                cell.val=pygame_nums[event.key]
                                draw(WIN,grid,WIDTH,buttons)
                                time.sleep(0.1)
                                cell.val=0
                                cell.make_red()
                                cell.draw(WIN)
                                pygame.display.update()
                                time.sleep(0.1)
                                cell.select()
                    if inputBox.selected:
                        if event.key!=pygame.K_DELETE:
                            inputBox.val=inputBox.val*10+pygame_nums[event.key]
                        else:
                            inputBox.val=0
        if clearBTN.is_clicked():
            grid=make_empty_grid()
            user_defined_grid=True

        if generateBTN.is_clicked():
            if inputBox.val>81:
                inputBox.val=81
            grid=create_sudoku(inputBox.val)
            user_defined_grid=False

        if StepsBox.is_clicked():
            StepsBox.click()
            time.sleep(0.1)#to prevent hyperclick

        if MVRbox.is_clicked():
            MVRbox.click()
            time.sleep(0.1)#to prevent hyperclick

        if solveBTN.is_clicked():
            if not user_defined_grid:
                for row in grid:
                    for cell in row:
                        if cell.changed:
                            cell.val = 0
                            cell.changed = False
            backtracking_soduko(lambda: draw(WIN, grid, WIDTH, buttons), grid,MVRbox.clicked,StepsBox.clicked)
        draw(WIN,grid,WIDTH,buttons)
    pygame.quit()
    quit()


if __name__=="__main__":
    main()

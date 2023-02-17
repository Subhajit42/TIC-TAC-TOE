import pygame, sys , numpy , random , sqlite3
pygame.init()
board=numpy.zeros((3,3)) #(3,3) for (rows,columns)
player=1
space=55
circle_colour=(255,250,123)
line_colour=(255,250,123)


#Database with Scoreboard
mydb=sqlite3.connect('RESULT.sqlite')
mycursor=mydb.cursor()
try:
    mycursor.execute("DROP table Scoreboard")
except:
    pass
mycursor.execute("""CREATE table Scoreboard (S_no integer Primary Key AUTOINCREMENT,Player_1 VARCHAR(4) default LOST,Player_2 VARCHAR(4) default LOST)""")

#for different colours
def randomcolour():
    rand=random.randint(1,5)
    if rand==1:
        BGCOLOUR=(30,210,255)

    elif rand==2:
        BGCOLOUR=(255,139,123)
    elif rand==3:
        BGCOLOUR=(137,21,245)
    elif rand==4:
        BGCOLOUR=(48,220,90)
    elif rand==5:
        BGCOLOUR=(248,23,29)
    return BGCOLOUR

#RGB format
screen=pygame.display.set_mode( (600,600) )
pygame.display.set_caption('TIC TAC TOE')

screen.fill(randomcolour())

#Drawing lines
def draw_lines():
    """VERTICAL LINES"""
    pygame.draw.line( screen,(255,255,255),(200,20),(200,580),15)
    pygame.draw.line( screen,(255,255,255),(400,20),(400,580),15)
    """HORTIZONTAL LINES"""
    pygame.draw.line( screen,(255,255,255),(20,200),(580,200),15)
    pygame.draw.line( screen,(255,255,255),(20,400),(580,400),15)

#contolling array or retrieving data from array
def write_sq(row,column,player):
    board[row][column]= player

def read_sq(row,column):
    return board[row][column]==0

def board_full():
    for row in range(3):
        for column in range(3):
            if board[row][column]==0:
                return False
    return True

#winner
def check_win(player):
    #for vertical check
    for col in range(3):
        if board[0][col]==player and board[1][col]==player and board[2][col]==player:
            draw_vert_line_win(col,player)
            return True #for terminating function
    #for horizintal check
    for row in range(3):
        if board[row][0]==player and board[row][1]==player and board[row][2]==player:
            draw_hori_line_win(row,player)
            return True
    #for diagonal(front) check "\"
    if board[0][0]==player and board[1][1]==player and board[2][2]==player:
        draw_slash_line_win(player)
        return True

    #for diagonal(back) check "/"
    if board[0][2]==player and board[1][1]==player and board[2][0]==player:
        draw_backslash_line_win(player)
        return True

    return False

def draw_vert_line_win(col,player):
    posX=col*200+100
    if player==1:
        colour=circle_colour
    elif player==2:
        colour=line_colour

    pygame.draw.line(screen,colour,(posX,space),(posX,600-space),15)

def draw_hori_line_win(row,player):
    posY=row*200+100
    if player==1:
        colour=circle_colour
    elif player==2:
        colour=line_colour

    pygame.draw.line(screen,colour,(space,posY),(600-space,posY),15)

def draw_backslash_line_win(player):
    if player==1:
        colour=circle_colour
    elif player==2:
        colour=line_colour

    pygame.draw.line(screen,colour,(space,600-space),(600-space,space),15)

def draw_slash_line_win(player):
    if player==1:
        colour=circle_colour
    elif player==2:
        colour=line_colour

    pygame.draw.line(screen,colour,(space,space),(600-space,600-space),15)


def database_eval():
        if player==1:
            sql="INSERT INTO Scoreboard (Player_1) VALUES ('WIN ')"
            mycursor.execute(sql)
        elif player==2:
            sql="INSERT INTO Scoreboard (Player_2) VALUES ('WIN ')"
            mycursor.execute(sql)
        mydb.commit()
        return mycursor.execute("SELECT * from Scoreboard")

def database_show():
    mycursor.execute("SELECT * from Scoreboard")
    mydb.commit()
    score=mycursor.fetchall()
    return score


def restart():
    screen.fill(randomcolour())
    draw_lines()
    player=1
    print()
    print("Welcome to TIC TAC TOE\n      => To view score press TAB\n      => To reset board press SPACE\n      => To exit click the cross button on top right corner")
    print()
    for row in range(3):
        for col in range(3):
            board[row][col]=0


def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col]==1:
                pygame.draw.circle(screen,circle_colour,(int(col*200+100),int(row*200+100)),60,15)
            elif board[row][col]==2:
                pygame.draw.line(screen,line_colour,(int(col*200+space),int(row*200+200-space)),(col*200+200-space,row*200+space),30)
                pygame.draw.line(screen,line_colour,(int(col*200+space),int(row*200+space)),(col*200+200-space,row*200+200-space),30)


gameover=False



#MAINLOOP
print()
print("Welcome to TIC TAC TOE\n      => To view score press TAB\n      => To reset board press SPACE\n      => To exit click the cross button on top right corner")
print()
while True:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            
            mycursor.execute("DROP table Scoreboard")
            sys.exit()
        
        draw_lines()
        pygame.display.update()
        if event.type==pygame.MOUSEBUTTONDOWN and not gameover:
            mouseX=event.pos[0]
            mouseY=event.pos[1]
            row_cl  =int(mouseY//200)
            col_cl  =int(mouseX//200)

            if read_sq(row_cl,col_cl):
                if player==1:
                    write_sq(row_cl,col_cl,1)
                    if check_win(player):
                        gameover=True
                        database_eval()
                        mydb=sqlite3.connect('RESULT.sqlite')
                        mycursor=mydb.cursor()
                        mycursor.execute("SELECT * from Scoreboard")
                        print()
                    player=2

                
                elif player==2:
                    write_sq(row_cl,col_cl,2)
                    if check_win(player):
                        gameover=True
                        database_eval()
                        

                    player=1
                
                draw_figures()
                #print(board)    to view the 2D array after each player marks a square


        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                #print(database_show())       shows score
                restart()
                gameover=False


        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_TAB:
                
                data=database_show()
                print()
                print("        SCOREBOARD")
                print("Sno.,player1,player2")
                print("        O   ,   X   ")
                for str_data in data:
                    print(str_data)


    pygame.display.update()
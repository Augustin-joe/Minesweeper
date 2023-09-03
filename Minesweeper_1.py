import random
import os
global r
global c
global n
global flag_count
flag_count=0
r=no_of_rows=8
c=no_of_columns=8
n=no_of_mines=8

def mine_generator(ax,by):
    global a
    global b
    i=0
    a=[None]*n
    b=[None]*n
    def top(ax,by,i):
        def side(ax,by,i):
            if ((a[i]==ax) and (b[i]==by)):
                i-=1
            return i
        i=side(ax,by,i)
        if by!=1:
            i=side(ax,by-1,i)
        if by!=c:
            i=side(ax,by+1,i)
        return i
    while i<n:
        a[i]=random.randint(1,r)
        b[i]=random.randint(1,c)
        i=top(ax,by,i)
        if ax!=1:
            i=top(ax-1,by,i)
        if ax!=r:
            i=top(ax+1,by,i)
            
        for j in range(i):
            if ((a[i]==a[j]) and (b[i]==b[j])):
                i-=1
                break
        i+=1

def define():
    def cal(i,j):
        count=0
        if table[i][j] == -1:
            count=count+1
        if j!=0:
            if table[i][j-1] == -1:
                count=count+1
        if j!=c-1:
            if table[i][j+1] == -1:
                count=count+1
        return count;
    global table
    table=[[0 for i in range(c)]for j in range(r)]
    for i in range(n):
        table[a[i]-1][b[i]-1]=-1
    for i in range(r):
        for j in range(c):
            if table[i][j] != -1:
                count=cal(i,j)
                table[i][j]+=count  
                if i!=0:
                    i-=1
                    count=cal(i,j)
                    i+=1
                    table[i][j]+=count
                if i!=r-1:
                    i+=1
                    count=cal(i,j)
                    i-=1
                    table[i][j]+=count  

def generate_display_table():
    global display_table
    display_table=[[' ' for y in range(c)] for x in range(r)]
    display(display_table)


def display(display_table):
    remaining_flag=n-flag_count
    d=int((c/2)*5)
    print(" "*d,"MINESWEEPER"," "*d,"Flag : ",remaining_flag)
    print()
    print("   ",end="")
    for i in range(c):
            if (i+1) / 10 <1:
                print(" ",i+1,"  ",end="")
            else:
                print(" ",i+1," ",end="")
    print()
    print("  ","-"*6*c)
    for i in range(r):
        if (i+1) / 10 <1:
            print(f"{i+1} |",end="")
        else:
            print(f"{i+1}|",end="")
        for j in range(c):
            print(" ",display_table[i][j]," |",end="")
        print()
        print("  |",end="")
        for k in range(c):
            print("     |",end="")
        print()
        print("  ","-"*6*c)

def check(x,y):
    global list_x
    global list_y
    close=False
    def next(x,y):
        if table[x][y]==0 and display_table[x][y]!="F":
            if x>0:
                check(x-1,y)
            if x<r-1:
                check(x+1,y)
            if y>0:
                check(x,y-1)
            if y<c-1:
                check(x,y+1)
        if display_table[x][y]!="F":
            display_table[x][y]=table[x][y]        

    for i in range(len(list_x)):
        if list_x[i]==x and list_y[i]==y:
            close=True
    if close==False:
        list_x.append(x)
        list_y.append(y)
        next(x,y)
    
generate_display_table()
game=1
first=1
while game ==1:
    try:
        x,y= input("Enter the block you need to select by (row, column) eg 4,4:").split(",")
        flag =int(input("Type '1' if the block selected to be marked flag else '0' :"))
        x=int(x)-1
        y=int(y)-1
    except:
        print("Enter valid input")
        continue
    if 0<=x<r and 0<=y<c:
        
        if first==1 and flag ==0:
            mine_generator(x+1,y+1)
            define()
            first=0
        
        flg=False
        cf=True
        if flag_count<n:
            flg=True
        if flag_count>=n and display_table[x][y] == ' 'and flag==1:
            print("No of flags exceeded")
        if flag==0 and display_table[x][y]=="F":
            try:
                cancel_flag=int(input("It's marked Flag \n If you are sure to select the block enter'1' else '0' :"))
            except:
                print("Enter valid input")
                continue
            if cancel_flag==0:
                cf=False
            elif cancel_flag==1:
                flag_count-=1
                display_table[x][y]=" "
            else:
                cf=False
                print("Enter valid input")
    
        if flag==1:
            if display_table[x][y] == ' ' and flg:
                flag_count+=1
                display_table[x][y]="F"
                os.system('clear')
                display(display_table)
            elif display_table[x][y] == 'F':
                try:
                    remove_flag=int(input("The flag is already marked \n enter '1' to remove flag else '0' : "))
                except:
                    print("Enter valid input")
                    continue
                if remove_flag == 1:
                    flag_count-=1
                    display_table[x][y]=" "
                os.system('clear')
                display(display_table)
                
        elif flag ==0 and cf:
            if table[x][y] ==-1:
                print("Game Over")
                print("you lost")
                display_table=table
                for i in range(r):
                    for j in range(c):
                        if display_table[i][j]==-1:
                            display_table[i][j]="M"
                os.system('clear')
                display(display_table)
                game=0
            
            elif table[x][y] == 0:
                list_x=[]
                list_y=[]
                check(x,y)
                os.system('clear')
                display(display_table)
            
            
            else:
                display_table[x][y]=table[x][y]
                os.system('clear')
                display(display_table)
            
        
        game_count=0
        for i in range(r):
            for j in range(c):
                if display_table[i][j]==' ' or display_table[i][j]=="F":
                    game_count+=1
                
        if game_count<=n and game==1:
            print("Congrats! You won the Game")
            game=0
        
    else:
        print("Enter correct input")
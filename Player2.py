import socket
import threading
import curses
import time

port = 5050
FORMAT = 'utf-8'
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP,port)

mywindow = curses.initscr()
a = [['__' for x in range(7)] for x in range(6)]
r = [5,5,5,5,5,5,5]

def update(move,color):
	move-=1
	a[r[move]][move] = color
	r[move]-=1
	return a

def getMatrixString(m):
	x = ''
	for row in m:
		x+=''.join(str(item) for item in row)
		x+="\n"
	return x

def checkVertical(a,move,color):
	count=1
	if r[move]<2:	
		for i in range(1,4): #vertical
			if a[r[move]+i+1][move] == color :
				count+=1
			else:
				break
		if count==4:
			return True
		else:
			count = 1
def checkHorizontal(a,move,color):
	count = 0
	start = move-3
	if start<0:
		start = 0
	end = move+3
	if end>6:
		end = 6
	for i in range(start,end+1): #horizontal
		if a[r[move]+1][i] == color :
			count+=1
			if count==4:
				return True


def checkLeftDiagonal(a,move,color):
	y = move
	x = r[move]+1
	flag = 'UD'
	i = 1
	count = 0
	while flag!= '':
		if (x+i<=5 and y-i>=0) and 'D' in flag:
			if a[x+i][y-i] == color:
				count+=1
			else:
				flag = flag.replace('D','')
		else:
			flag = flag.replace('D','')
			
		if (x-i>=0 and y+i<=6) and 'U' in flag:
			if a[x-i][y+i] == color:
				count+=1
			else:
				flag = flag.replace('U','')
		else:
			flag = flag.replace('U','')
		if count>2:
			return True
		i+=1
	return False

def checkRightDiagonal(a,move,color):
	y = move
	x = r[move]+1
	flag = 'UD'
	i = 1
	count = 0
	while flag!= '':
		if (x-i>=0 and y-i>=0) and 'U' in flag:
			if a[x-i][y-i] == color:
				count+=1
			else:
				flag = flag.replace('U','')
		else:
			flag = flag.replace('U','')
		if (x+i<=5 and y+i<=6) and 'D' in flag:
			if a[x+i][y+i] == color:
				count+=1
			else:
				flag = flag.replace('D','')

		else:
			flag = flag.replace('D','')
		if count>2:
			return True
		i+=1
		
	return False

def check(a,move,color):
	return checkHorizontal(a,move,color) or checkVertical(a,move,color) or checkRightDiagonal(a,move,color) or checkLeftDiagonal(a,move,color)

def reading(client):
	p = 0
	connected = True
	print("[TOSS]")
	TossResult = client.recv(2048).decode(FORMAT)
	if TossResult=='2':
		print("Hurray!! you won the toss! :)....")
		mywindow.addstr(0, 0, getMatrixString(a))
		mywindow.addstr(6, 0, "1 2 3 4 5 6 7 <--- Choose any one coloumn")
		while connected:
			p+=1
			move = mywindow.getch()
			move = int(move) - 48
			
			while move>7 or move<1 or r[move-1]<0:  #check for valid move
				p+=1
				mywindow.addstr(6+p, 0, "INVALID")
				move = mywindow.getch()
				move = int(move) - 48
				
			client.send(str(move).encode(FORMAT))
			mywindow.addstr(7+p, 0, "WAIT....")
			matrix = update(move,'1 ')
			mywindow.addstr(0, 0, getMatrixString(matrix))
			mywindow.refresh()
			if check(matrix,move-1,'1 '):
				mywindow.addstr(20, 20, "YOU WON")
				mywindow.refresh()
				time.sleep(2)
				break
				
			OpponentMove = int(client.recv(2048).decode(FORMAT))
			
			matrix = update(OpponentMove,'0 ')
			mywindow.addstr(0, 0, getMatrixString(matrix))
			mywindow.refresh()
			if check(matrix,OpponentMove-1,'0 '):
				mywindow.addstr(20, 20, "YOU LOST")
				mywindow.refresh()
				time.sleep(2)
				connected = False
			#display(move,OpponentMove)			

	else:
		print("You lost the toss!...")
		mywindow.addstr(0, 0, getMatrixString(a))
		mywindow.addstr(6, 0, "1 2 3 4 5 6 7 <--- Choose any one coloumn")
		while connected:

			OpponentMove = int(client.recv(2048).decode(FORMAT))

			
			matrix = update(OpponentMove,'0 ')
			mywindow.addstr(0, 0, getMatrixString(matrix))
			mywindow.refresh()
			if check(matrix,OpponentMove-1,'0 '):
				mywindow.addstr(20, 20, "YOU LOST")
				mywindow.refresh()
				time.sleep(2)
				break

			move = mywindow.getch()
			move = int(move) - 48

			while move>7 or move<1 or r[move-1]<0:  #check for valid move
				p+=1
				mywindow.addstr(8+p, 1, "INVALID")
				move = mywindow.getch()
				move = int(move) - 48

			client.send(str(move).encode(FORMAT))

			matrix = update(move,'1 ')
			mywindow.addstr(0, 0, getMatrixString(matrix))
			mywindow.refresh()
			if check(matrix,move-1,'1 '):
				mywindow.addstr(20, 20, "YOU WON")
				mywindow.refresh()
				time.sleep(2)
				connected = False


def start():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
	print("You are connected")
	print("Type END if you want to disconnect")
	reading(client)

if __name__=='__main--':
	start()

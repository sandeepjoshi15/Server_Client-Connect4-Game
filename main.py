import curses
import time
import Player1 as S
import Player2 as C


menu = ['Host', 'Join', 'Exit']

def print_menu(stdscr,curr_row):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	
	for idx,row in enumerate(menu):
		x = w//2 - len(row)//2
		y = h//2 - len(menu)//2 + idx
		if idx==curr_row:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y,x,row)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y,x,row)
	stdscr.refresh()
	
def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLUE)
	current_row = 0
	print_menu(stdscr,current_row)
	curr_row = current_row%3
	while 1:
		key = stdscr.getch()
		if key == curses.KEY_UP:
			current_row-=1
			
		elif key==curses.KEY_DOWN:
			current_row+=1
		elif key == curses.KEY_ENTER or key in (10,13):
			if menu[curr_row]=='Host':
				stdscr.clear()
				S.start()
				stdscr.refresh()
				pass
			elif menu[curr_row]=='Join':
				stdscr.clear()
				C.start()
				pass
			else:
				break;
			stdscr.refresh()
		curr_row = current_row%3
		print_menu(stdscr,curr_row)

curses.wrapper(main)


'''exec(open('./Player1.py').read())
print('bye')'''

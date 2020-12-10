#!/usr/bin/env python3
#
#	This is free and unencumbered software released into the public domain.
#	
#	Anyone is free to copy, modify, publish, use, compile, sell, or
#	distribute this software, either in source code form or as a compiled
#	binary, for any purpose, commercial or non-commercial, and by any
#	means.
#	
#	In jurisdictions that recognize copyright laws, the author or authors
#	of this software dedicate any and all copyright interest in the
#	software to the public domain. We make this dedication for the benefit
#	of the public at large and to the detriment of our heirs and
#	successors. We intend this dedication to be an overt act of
#	relinquishment in perpetuity of all present and future rights to this
#	software under copyright law.
#	
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#	IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#	OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#	ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#	OTHER DEALINGS IN THE SOFTWARE.
#	
#	For more information, please refer to <https://unlicense.org>


import numpy as np
import time
import curses as cu
#import sys
np.random.seed(int(time.time()))
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=200)

class Life:
	#sizex=320
	#sizey=89
	sizex=79
	sizey=23
	gen=0
	even=0
	neigh=[]

	def __init__(self,x,y):
		self.sizex=x
		self.sizey=y
		self.arr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)
		self.warr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)

	def flipGen(self):
		if self.even == 0:
			self.even=1
			return
		elif self.even == 1:
			self.even=0
			return
		self.even=0
	
	def seedRandom(self):
		self.arr=np.random.randint(
			size=(self.sizey, self.sizex), 
			dtype=np.int8,
			low=0,
			high=2)
	
	def getNeigh(self,x,y):
		rl=[]
		e=False
		s=False
		w=False
		n=False
		
		if x == 0:
			w=True
		if y == 0:
			n=True
		if x >= self.sizex-1:
			e=True
		if y >= self.sizey-1:
			s=True
			
		if not e :
			rl.append([x+1,y])
		if not s :
			rl.append([x,y+1])
		if not w :
			rl.append([x-1,y])
		if not n :
			rl.append([x,y-1])
		if (not e) and  (not s) :
			rl.append([x+1,y+1])
		if (not w) and (not n) :
			rl.append([x-1,y-1])
		if (not e) and (not n) :
			rl.append([x+1,y-1])
		if (not w) and (not s) :
			rl.append([x-1,y+1])
		return rl
	
	def genNmap(self):
		self.neigh=[]
		row=[]
		for y in range(0, self.sizey):
			row=[]
			for x in range(0, self.sizex):
				row.append(self.getNeigh(x,y))
			self.neigh.append(row)
	
	def genWmapCached(self):
		sum=0
		for y in range(0, self.sizey):
			for x in range(0, self.sizex):
				sum=0
				for n in self.neigh[y][x]:
					sum+=self.arr[n[1],n[0]]
				self.warr[y,x]=sum
				#print('DEBUG genMap '+str(x))
				#print("DEBUG y "+str(y)+" x "+str(x))
				#print("DEBUG n "+str(self.neigh[y][x]))
				#print("DEBUG sum "+str(sum))
				#print("DEBUG written "+str(int(self.warr[n[1],n[0]])))
	
	def nextGeneration(self):
		for y in range(0, self.sizey):
			for x in range(0, self.sizex):
				#print("DEBUG y"+str(y)+" x "+str(x))
				if self.arr[y,x] == 1:
					if self.warr[y,x] < 2:
						#dies
						#print("DEBUG DIES")
						self.arr[y,x]=0
					elif self.warr[y,x] > 3:
						#dies
						#print("DEBUG DIES")
						self.arr[y,x]=0
					#print("DEBUG LIVES")
				else:
					if self.warr[y,x]==3:
						#reproduction
						self.arr[y,x]=1
						#print("DEBUG CREATES")
		#print("DEBUG")
		#print(self.warr)
	def initAndSeed(self):
		self.seedRandom()
		self.genNmap()
		self.genWmapCached()
	
	def reSeed(self):
		self.seedRandom()
		self.genWmapCached()

	def ng(self):
		self.nextGeneration()
		self.genWmapCached()
		self.gen+=1

def termResize(y,x):
	#sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=y, cols=x))
	print("\x1b[8;{rows};{cols}t".format(rows=y, cols=x))

def testLIFE():
	w = Life()
	w.seedRandom()
	print(w.arr)
	print(w.warr)
	print("getNeigh 0,0") 
	print(w.getNeigh(0,0))
	
	print("getNeigh 10,10") 
	print(w.getNeigh(10,10))
	
	print("getNeigh 79,23") 
	print(w.getNeigh(79,23))
	
	print("getNeigh 0,23") 
	print(w.getNeigh(0,23))
	
	print("getNeigh 79,0") 
	print(w.getNeigh(79,0))

	print("getNeigh 17,0") 
	print(w.getNeigh(17,0))

	print("getNeigh 15,0") 
	print(w.getNeigh(15,0))

	#w.genWmap()
	w.genNmap()
	w.genWmapCached()
	print(w.arr)
	print(w.warr)
	
	for i in range(0,3):
		#print(chr(27) + "[2J")
		w.ng()
		print("arr")
		print(w.arr)
		print("warr")
		print(w.warr)
		time.sleep(0.05)

class Game:
	sizex=79
	sizey=23
	gen=0
	even=0
	neigh=[]

	def __init__(self,x=80,y=24,drawMode=1,delay=0.1):
		if x<80 or y<24:
			print("x or y too small")
			exit()
		if drawMode<1 or drawMode > 3:
			print("wrong draw mode")
			exit()
		l=Life(x,y)
		l.initAndSeed()
		termResize(l.sizey, l.sizex)
		sc=cu.initscr()
		sc.nodelay(1)
		cu.start_color()
		cu.noecho()
		cu.cbreak()
		cu.init_pair(1,cu.COLOR_BLACK,	cu.COLOR_BLACK)
		cu.init_pair(2,cu.COLOR_BLACK,	cu.COLOR_BLUE)
		cu.init_pair(3,cu.COLOR_BLACK,	cu.COLOR_YELLOW)
		cu.init_pair(4,cu.COLOR_BLACK,	cu.COLOR_YELLOW)
		cu.init_pair(5,cu.COLOR_BLACK,	cu.COLOR_RED)
		cu.init_pair(6,cu.COLOR_BLACK,	cu.COLOR_RED)
		cu.init_pair(7,cu.COLOR_BLACK,	cu.COLOR_RED)
		cu.init_pair(8,cu.COLOR_BLACK,	cu.COLOR_RED)
		cu.init_pair(99,cu.COLOR_GREEN,	cu.COLOR_BLACK)
		
		sc.clear()
		cu.curs_set(0)
		w=cu.newwin(l.sizey,l.sizex)
		#w.timeout(100)
		while True:
			termResize(l.sizey, l.sizex)
			l.ng()
			if drawMode==1:
				self.cDrawFrame(l,w)
			elif drawMode==2:
				self.cDrawFrameDebug(l,w)
			elif drawMode==3:
				self.cDrawFrameDebug2(l,w)
			w.addnstr(l.sizey-1, 0, "-=- generation: {} -=-".format(l.gen), 25)
			w.addnstr(l.sizey-1, 25, "delay: {}".format(delay), 10)
			
			
			time.sleep(delay)
			
			c=sc.getch()
			if c==ord('1'):
				drawMode=1
			if c==ord('2'):
				drawMode=2
			if c==ord('3'):
				drawMode=3
			if c==ord('q'):
				cu.endwin()
				exit(0)
			if c==ord('+'):
				if delay>=0.1:
					delay-=0.1
			if c==ord('-'):
				delay+=0.1
			if c==ord('='):
				delay=0.1
			if c==ord('9'):
				delay=1
			if c==ord('8'):
				delay=0.3
			if c==ord('7'):
				delay=0
			if c==ord('s'):
				l.reSeed()
			
		cu.endwin()
		
	
	def cDrawFrameDebug(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				if l.arr[y,x]==1:
					w.addch(y,
						x,
						str(int(l.warr[y,x])),
						cu.color_pair(int(l.warr[y,x])+1))
				if l.arr[y,x]==0:
					w.addch(y,
						x,
						' ',
						cu.color_pair(1))
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					w.addch(y,
						x,
						str(int(l.warr[y,x])),
						cu.color_pair(99))
		w.refresh()
	
	def cDrawFrameDebug2(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				w.addch(y,
					x,
					str(int(l.warr[y,x])),
					cu.color_pair(int(l.warr[y,x])+1))
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					w.addch(y,
						x,
						str(int(l.warr[y,x])),
						cu.color_pair(99))
		w.refresh()
	
	def cDrawFrame(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				if l.arr[y,x]==1:
					w.addch(y,
						x,
						'x',
						cu.color_pair(int(l.warr[y,x])+1))
				if l.arr[y,x]==0:
					w.addch(y,
						x,
						' ',
						cu.color_pair(1))
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					w.addch(y,
						x,
						'*',
						cu.color_pair(99))
		w.refresh()

def main():
	#testLIFE()
	#Game(delay=0)
	#Game(delay=0.3)
	#Game(x=319,yu89)
	Game()
	
	print("exit")

if __name__ == "__main__":
	main()

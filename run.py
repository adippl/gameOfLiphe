#!/usr/bin/env python3
import numpy as np
import time
import curses as cu
np.random.seed(int(time.time()))
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=200)

class Life:
	sizex=80
	sizey=24
	gen=0
	even=0
	neigh=[]

	def __init__(self):
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
		#print(n, s, w, e)
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
		neigh=[]
		sum=0
		for y in self.neigh:
			for x in y:
				sum=0
				for n in x:
					sum+=self.arr[n[1],n[0]]
				self.warr[n[1],n[0]]=sum
				print('DEBUG genMap '+str(x))
				print("DEBUG y "+str(y)+" x "+str(x))
				print("DEBUG sum "+str(sum))
				print("DEBUG written "+str(int(self.warr[n[1],n[0]])))
	
	def nextGeneration(self):
		for y in range(0, self.sizey):
			for x in range(0, self.sizex):
				print("DEBUG y"+str(y)+" x "+str(x))
				if self.arr[y,x] == 1:
					if self.warr[y,x] < 2:
						#dies
						print("DEBUG DIES")
						self.arr[y,x]=0
					elif self.warr[y,x] > 3:
						#dies
						print("DEBUG DIES")
						self.arr[y,x]=0
					print("DEBUG LIVES")
				else:
					if self.warr[y,x]==3:
						#reproduction
						self.arr[y,x]=1
						print("DEBUG CREATES")
		print("DEBUG")
		print(self.warr)
	def initAndSeed(self):
		self.seedRandom()
		self.genNmap()
		self.genWmapCached()

	def ng(self):
		self.nextGeneration()
		self.genWmapCached()
		self.gen+=1
	
def testLIFE():
	print("Compiled!")
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

def cDrawFrameDebug(l, w):
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


def cDrawFrameDebug2(l, w):
	for y in range(0, l.sizey-1):
		for x in range(0, l.sizex-1):
			w.addch(y,
				x,
				str(int(l.arr[y,x])),
				cu.color_pair(int(l.warr[y,x])+1))
			if l.arr[y,x]==0 and l.warr[y,x]==3:
				w.addch(y,
					x,
					str(int(l.warr[y,x])),
					cu.color_pair(99))
	w.refresh()

def cDrawFrame(l, w):
	for y in range(0, l.sizey-1):
		for x in range(0, l.sizex-1):
			w.addch(y,
				x,
				'x',
				cu.color_pair(int(l.warr[y,x])+1))
			if l.arr[y,x]==0 and l.warr[y,x]==3:
				w.addch(y,
					x,
					'*',
					cu.color_pair(99))
	w.refresh()

def cTest():
	l=Life()
	l.initAndSeed()
	#print(l.arr)
	#print(l.warr)
	
	sc=cu.initscr()
	cu.start_color()
	cu.noecho()
	cu.cbreak()
	cu.init_pair(1,cu.COLOR_BLACK,cu.COLOR_BLACK)
	cu.init_pair(2,cu.COLOR_BLUE,cu.COLOR_BLACK)
	cu.init_pair(3,cu.COLOR_GREEN,cu.COLOR_BLACK)
	cu.init_pair(4,cu.COLOR_YELLOW,cu.COLOR_BLACK)
	cu.init_pair(5,cu.COLOR_RED,cu.COLOR_BLACK)
	cu.init_pair(6,cu.COLOR_RED,cu.COLOR_BLACK)
	cu.init_pair(7,cu.COLOR_RED,cu.COLOR_BLACK)
	cu.init_pair(8,cu.COLOR_RED,cu.COLOR_BLACK)
	cu.init_pair(99,cu.COLOR_BLACK,cu.COLOR_GREEN)
	
	sc.clear()
	w=cu.newwin(24,80)
	
	for i in range(0,100):
		l.ng()
		#cDrawFrameDebug(l,w)
		cDrawFrameDebug2(l,w)
		#cDrawFrame(l,w)
		time.sleep(0.1)
	
	
	
	cu.endwin()


def main():
	testLIFE()
	#cTest()
	
	print("exit")

if __name__ == "__main__":
	main()

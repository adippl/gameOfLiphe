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
import sys
import argparse
import signal
import random
np.random.seed(int(time.time()))
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=200)

gliderNE=[[0,1],[1,0],[2,0],[2,1],[2,2]]
gliderSE=[[0,1],[1,2],[2,0],[2,1],[2,2]]
gliderNW=[[0,1],[1,0],[0,0],[2,1],[0,2]]
gliderSW=[[0,1],[1,2],[0,0],[2,1],[0,2]]
gliderGunWstopper=[[0,4],[1,4],[0,5],[1,5],[10,4],[10,5],[10,6],[11,3],[11,7],[12,2],[12,8],[13,2],[13,8],[14,5],[15,3],[15,7],[16,4],[16,5],[16,6],[17,5],[20,2],[20,3],[20,4],[21,2],[21,3],[21,4],[22,1],[22,5],[24,0],[24,1],[24,5],[24,6],[23,10],[23,11],[24,10],[24,12],[25,12],[26,12],[26,13],[34,2],[34,3],[35,2],[35,3]]
gliderGun=[[0,4],[1,4],[0,5],[1,5],[10,4],[10,5],[10,6],[11,3],[11,7],[12,2],[12,8],[13,2],[13,8],[14,5],[15,3],[15,7],[16,4],[16,5],[16,6],[17,5],[20,2],[20,3],[20,4],[21,2],[21,3],[21,4],[22,1],[22,5],[24,0],[24,1],[24,5],[24,6],[34,2],[34,3],[35,2],[35,3]]

class Life:
	#sizex=320
	#sizey=89
	sizex=79
	sizey=23
	gen=0
	even=0
	neigh=[]
	wmapMode=True
	
	def __init__(self,x,y):
		self.sizex=x
		self.sizey=y
		self.arr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)
		self.warr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)
	
	def zero(self):
		self.arr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)
		self.warr = np.zeros(shape=(self.sizey,self.sizex), dtype=np.int8)
	
	def insertShape(self, shape, x, y):
		for s in shape:
			self.arr[s[1]+y][s[0]+x]=1
	
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
		if self.wmapMode:
			self.neigh=[]
			row=[]
			for y in range(0, self.sizey):
				row=[]
				for x in range(0, self.sizex):
					row.append(self.getNeigh(x,y))
				self.neigh.append(row)
		else:
			self.neigh=[]

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

	def genWmapNotCached(self):
		sum=0
		for y in range(0, self.sizey):
			for x in range(0, self.sizex):
				sum=0
				#for n in self.neigh[y][x]:
				#	sum+=self.arr[n[1],n[0]]
				#rl=[]
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
					sum+=self.arr[y][x+1]
				if not s :
					sum+=self.arr[y+1][x]
				if not w :
					sum+=self.arr[y][x-1]
				if not n :
					sum+=self.arr[y-1][x]
				if (not e) and (not s):
					sum+=self.arr[y+1][x+1]
				if (not w) and (not n):
					sum+=self.arr[y-1][x-1]
				if (not e) and (not n):
					sum+=self.arr[y-1][x+1]
				if (not w) and (not s):
					sum+=self.arr[y+1][x-1]
				self.warr[y,x]=sum

	def genWmap(self):
		if self.wmapMode:
			self.genWmapCached()
		else:
			self.genWmapNotCached()
			
	
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
		self.genWmap()

	def initAndZero(self):
		self.genNmap()
		self.genWmap()
	
	def reSeed(self):
		self.seedRandom()
		self.genWmap()

	def ng(self):
		self.nextGeneration()
		self.genWmap()
		self.gen+=1

def termResize(y,x):
	print("\x1b[8;{rows};{cols}t".format(rows=y, cols=x))
	#resize doens't work on linux
	#cu.resizeterm(y,x)

def testLIFE():
	w = Life(80,24)
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

	w.genNmap()
	w.genWmap()
	print(w.arr)
	print(w.warr)
	print(w.neigh)
	
	for i in range(0,3):
		#print(chr(27) + "[2J")
		w.ng()
		print("arr")
		print(w.arr)
		print("warr")
		print(w.warr)
		time.sleep(0.05)

def sighand(sig, frame):
	cu.endwin()
	exit(0)
	

class Game:
	sizex=79
	sizey=23
	gen=0
	even=0
	neigh=[]

	def __init__(self, x=80, y=24, drawMode=1, delay=0.1, maxgen=0, reseed=0, start=0, zero=0, cached=True):
		if x<80 or y<24:
			print("x or y too small")
			exit()
		if drawMode<1 or drawMode > 4:
			print("wrong draw mode")
			exit()
		l=Life(x,y)
		if start==0:
			l.initAndSeed()
			gliderSpawner=False
		elif start==1:
			l.initAndZero()
			gliderSpawner=True
		
		l.wmapMode=cached
		
		#termResize(l.sizey, l.sizex)
		#resize +1 to fix some strange bug
		termResize(l.sizey+1, l.sizex+1)
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
		signal.signal(signal.SIGINT, sighand)
		sc.clear()
		cu.curs_set(0)
		w=cu.newwin(l.sizey,l.sizex)
		w.timeout(100)

		while True:
			termResize(l.sizey, l.sizex)
			start_time=time.time()
			l.ng()
			ngTime=time.time()-start_time
			
			start_time=time.time()
			if drawMode==1:
				self.cDrawFrame(l,w)
			elif drawMode==2:
				self.cDrawFrameDebug(l,w)
			elif drawMode==3:
				self.cDrawFrameDebug2(l,w)
			elif drawMode==4:
				self.cDrawFrameClassic(l,w)
			drTime=time.time()-start_time
			
			try:
				w.addnstr(l.sizey-1, 0, "-=- generation: {} -=-".format(l.gen), 25)
				w.addnstr(l.sizey-1, 25, " delay: {}  ".format(delay), 11)
				w.addnstr(l.sizey-1, 36, " genTime: {}".format(ngTime), 14)
				w.addnstr(l.sizey-1, 51, " drawTime: {}".format(drTime), 15)
				w.addnstr(l.sizey-1, 66, " H: {} ".format(gliderSpawner), 10)
			except (cu.error):
				termResize(l.sizey, l.sizex)
				pass
				#cu.endwin()
				#exit(1)
			
			time.sleep(delay)
			
			c=sc.getch()
			#CONTROLS
			if c==ord('1'):
				drawMode=1
			elif c==ord('2'):
				drawMode=2
			elif c==ord('3'):
				drawMode=3
			elif c==ord('4'):
				drawMode=4
			elif c==ord('q'):
				cu.endwin()
				exit(0)
			elif c==ord('+'):
				if delay>=0.1:
					delay-=0.1
			elif c==ord('-'):
				delay+=0.1
			elif c==ord('='):
				delay=0.1
			elif c==ord('0'):
				delay=2
			elif c==ord('9'):
				delay=1
			elif c==ord('8'):
				delay=0.3
			elif c==ord('7'):
				delay=0
			elif c==ord('s'):
				l.reSeed()
			elif c==ord('z'):
				l.zero()
			elif c==ord('p'):
				time.sleep(5)
			elif c==ord('h'):
				dir=random.randint(0,3)
				x=random.randint(0, l.sizex-3)
				y=random.randint(0, l.sizey-3)
				if dir==0:
					l.insertShape(gliderNE, x, y)
				elif dir==1:
					l.insertShape(gliderNW, x, y)
				elif dir==2:
					l.insertShape(gliderSE, x, y)
				elif dir==3:
					l.insertShape(gliderSW, x, y)
				l.genWmap()
			elif c==ord('H'):
				if gliderSpawner:
					gliderSpawner=False
				else:
					gliderSpawner=True
			elif c==ord('T'):
				l.insertShape(gliderSE, 0, 0)
				l.insertShape(gliderNE, 0, 10)
				l.insertShape(gliderNW, 10, 10)
				l.insertShape(gliderSW, 10, 0)
				l.genWmap()
			elif c==ord('g'):
				l.insertShape(gliderGun,0,0)
				l.genWmap()
			elif c==ord('G'):
				l.insertShape(gliderGunWstopper,0,0)
				l.genWmap()
			
			if gliderSpawner and l.gen%10==0:
				dir=random.randint(0,3)
				x=random.randint(0, l.sizex-3)
				y=random.randint(0, l.sizey-3)
				if dir==0:
					l.insertShape(gliderNE, x, y)
				elif dir==1:
					l.insertShape(gliderNW, x, y)
				elif dir==2:
					l.insertShape(gliderSE, x, y)
				elif dir==3:
					l.insertShape(gliderSW, x, y)
				l.genWmap()
			
			if maxgen!=0 and l.gen>=maxgen:
				time.sleep(5)
				cu.endwin()
				sys.exit(0)
			if reseed!=0 and l.gen%reseed==0:
				l.reSeed()
			if zero!=0 and l.gen%zero==0:
				l.zero()
		cu.endwin()
	
	def cDrawFrameDebug(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				if l.arr[y,x]==1:
					ch=str(int(l.warr[y,x]))
					col=int(l.warr[y,x])+1
				if l.arr[y,x]==0:
					ch=' '
					col=1
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					ch=str(int(l.warr[y,x]))
					col=99
				try:
					w.addch(y, x, ch, cu.color_pair(col))
				except (cu.error):
					termResize(l.sizey, l.sizex)
					pass
		w.refresh()
	
	
	def cDrawFrameDebug2(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				ch=str(int(l.warr[y,x]))
				col=int(l.warr[y,x])+1
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					ch=str(int(l.warr[y,x]))
					col=99
				try:
					w.addch(y, x, ch, cu.color_pair(col))
				except (cu.error):
					termResize(l.sizey, l.sizex)
					pass
		w.refresh()
	
	def cDrawFrame(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				if l.arr[y,x]==1:
					ch='x'
					col=int(l.warr[y,x])+1
				if l.arr[y,x]==0:
					ch=' '
					col=1
				if l.arr[y,x]==0 and l.warr[y,x]==3:
					ch='*'
					col=99
				try:
					w.addch(y, x, ch, cu.color_pair(col))
				except (cu.error):
					termResize(l.sizey, l.sizex)
					pass
		w.refresh()
	
	def cDrawFrameClassic(self, l, w):
		for y in range(0, l.sizey-1):
			for x in range(0, l.sizex-1):
				if l.arr[y,x]==1:
					ch='x'
					col=int(l.warr[y,x])+1
				if l.arr[y,x]==0:
					ch=' '
					col=1
				try:
					#w.addch(y, x, ch, cu.color_pair(col))
					w.addch(y, x, ch)
				except (cu.error):
					termResize(l.sizey, l.sizex)
					pass
		w.refresh()


def main():
	#testLIFE()
	#Game(delay=0)
	#Game(delay=0.3)
	#Game(x=319,yu89)
	#Game()
	
	p=argparse.ArgumentParser()
	p.add_argument("-x", default=80,	type=int,	help="terminal height (min 80)")
	p.add_argument("-y", default=24,	type=int,	help="terminal width (min 24)")
	p.add_argument("-M", default=1,	type=int,	help="drawing mode (1 normal, 2 debug cell neigh, 3 neigh map)")
	p.add_argument("-d", default=0.1,	type=float,	help="delay between frames")
	p.add_argument("-e", default=0,	type=int,	help="stop after E generatison")
	p.add_argument("-r", default=0,	type=int,	help="reseed after R generatison")
	p.add_argument("-z", default=0,	type=int,	help="zero every Z generations")
	p.add_argument("-s", default=0,	type=int,	help="0 start seeded, 1 start empty + glider spawner")
	p.add_argument("-c", default=1,	type=int,	help="1 == cached mode; 0 == non cached mode")
	a=p.parse_args()
	if a.x < 80:
		a.x=80
	if a.y < 24:
		a.y=24
	if a.M < 1 or a.M > 4:
		a.M=1
	if a.d < 0.1:
		a.d=0
	if a.e <0:
		a.e=0
	if a.r <0:
		a.r=0
	if a.s <0 or a.s>1:
		a.r=0
	if a.z <0:
		a.z=0
	if a.c==1:
		lcached=True
	else:
		lcached=False
	
	Game(x=a.x, y=a.y, delay=a.d, drawMode=a.M, maxgen=a.e, reseed=a.r, start=a.s, zero=a.z, cached=lcached) 
	exit(0)

if __name__ == "__main__":
	main()

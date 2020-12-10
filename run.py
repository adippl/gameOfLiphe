#!/usr/bin/env python3
import numpy as np
import time
np.random.seed(int(time.time()))
np.set_printoptions(threshold=np.inf)
np.set_printoptions(linewidth=200)

class World:
	sizex=80
	sizey=24
	generationNumber=0
	even=0

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
			high=2
			)
	
	def calculateWarr(self):
		print("lol")
		
	
	def getNeigh(self,x,y):
		rl=[]
		e=False
		s=False
		w=False
		n=False
		
		if x == 0:
			e=True
		if y == 0:
			s=True
		if x >= self.sizex-1:
			w=True
		if y >= self.sizey-1:
			n=True
			
		if e :
			rl.append([x+1,y])
		if s :
			rl.append([x,y+1])
		if e and s :
			rl.append([x+1,y+1])
		if w :
			rl.append([x-1,y])
		if n :
			rl.append([x,y-1])
		if w and n :
			rl.append([x-1,y-1])
		if e and n :
			rl.append([x+1,y-1])
		if w and s :
			rl.append([x-1,y+1])
		if not e and not w and not n and not s:
			rl.append([x+1,y])
			rl.append([x,y+1])
			rl.append([x+1,y+1])
			rl.append([x-1,y])
			rl.append([x,y-1])
			rl.append([x-1,y-1])
			rl.append([x+1,y-1])
			rl.append([x-1,y+1])
		print(n, s, w, e)
		return rl
	
	def genWmap(self):
		neigh=[]
		for y in range(0, self.sizey-1):
			for x in range(0, self.sizex-1):
				print(y, x, self.arr[y,x])
				neigh=self.getNeigh(x,y)
				print(neigh)


		

def main():
	print("Compiled!")
	w = World()
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
	print("getNeigh 0,17") 
	print(w.getNeigh(0,17))

	#w.genWmap()

if __name__ == "__main__":
	main()

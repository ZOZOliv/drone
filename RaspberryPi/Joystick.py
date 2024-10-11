import tkinter as tk
import types
import keyboard

class pad():
	def __init__(self, window, posX, posY, color='red'):
		self.click = False
		self.c = tk.Canvas(window, height=100, width=100, bg=color)
		self.c.place(x=posX, y=posY, anchor='center')
		self.circle1 = self.c.create_oval(40, 40, 60, 60, outline='white')
		self.c.bind('<Motion>', self.Mouse_Move)
		self.c.bind('<Button-1>', self.Mouse_Clicked)
		self.c.bind('<ButtonRelease-1>', self.Mouse_released)
		self.callbacks = list()

	def registerCallback(self, callback: types.FunctionType):
		self.callbacks.append(callback)

	def Mouse_Clicked(self, event):
		self.click = True
		posX = event.x
		posY = event.y
		self.Eval_Pos(posX, posY)
		
	def Mouse_released(self, event):
		self.click = False
		posX = 50
		posY = 50
		self.Eval_Pos(posX, posY)

	def Mouse_Move(self, event):
		if self.click == True:
			if event.x < 0:
				posX = 0
			elif event.x > 100:
				posX = 100
			else:
				posX = event.x

			if event.y < 0:
				posY = 0
			elif event.y > 100:
				posY = 100
			else:
				posY = event.y
	
			self.Eval_Pos(posX, posY)
	
	def Eval_Pos(self, posX, posY):
		self.c.coords(self.circle1, posX-10, posY-10, posX+10, posY+10)
		for callback in self.callbacks:
			callback(posX, posY)

class scale():
	def __init__(self, window, posX, posY):
		self.Var = 0
		self.scale = tk.Scale(window, variable = self.Var, from_ = 100, to = 0, orient = tk.VERTICAL, command=self.scale_cmd)
		self.scale.place(x=posX, y=posY, anchor='center')
		self.callbacks = list()

	def scale_cmd(self, newValue):
		self.Var = int(newValue)
		for callback in self.callbacks:
			callback(self.Var)

	def up(self):
		if self.Var < 100:
			self.Var = self.Var + 1
		self.scale.set(value=self.Var)
	
	def down(self):
		if self.Var > 0:
			self.Var = self.Var - 1
		self.scale.set(value=self.Var)

	def reset(self):
		self.Var = 0
		self.scale.set(value=self.Var)

	def registerCallback(self, callback: types.FunctionType):
		self.callbacks.append(callback)

def printPos(X, Y):
	global horizontal
	global verticale
	horizontal = X
	verticale = Y

def printGaz(X):
	global gaz
	gaz = X

def Getkey():
	if keyboard.is_pressed('a'):
		myScale.up()
	elif keyboard.is_pressed('q'):
		myScale.down()
	elif keyboard.is_pressed('w'):
		myScale.reset()

	root.after(2, Getkey)

gaz = 0
horizontal = 0
verticale = 0

root = tk.Tk()
root.geometry('400x200')

myScale = scale(root, 200, 100)
myScale.registerCallback(printGaz)

myPad = pad(root, 100, 100, 'green')
myPad.registerCallback(printPos)

Getkey()
root.mainloop()
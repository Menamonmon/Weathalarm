from Sound import *

class StyledCheckbutton(tk.Label):
	def __init__(self, master, state=1, size=(32, 32), **kwargs):
		super().__init__(master)
		self["bd"] = 0
		self["bg"] = master["bg"]
		self.master = master
		self.size = size
		self.state = state
		self.pic = ImageTk.PhotoImage(Image.open(f"customCheckbutton/{self.state}.png").resize(size, Image.ANTIALIAS))
		self.label = tk.Label(self, image=self.pic)

		self.label.pack(side="top")
		self.label.bind("<Button-1>", func=self.reverse)

		for arg, val in kwargs.items():
			self[arg] = val
			self.label[arg] = val
			if hasattr(self, "active_label"):
				self.active_label[arg] = val

	def __repr__(self):
		return self.frame

	def set_state(self, event, new_state):
		self.state = new_state
		self.pic = ImageTk.PhotoImage(Image.open(f"customCheckbutton/{self.state}.png").resize(self.size, Image.ANTIALIAS))
		self.label["image"] = self.pic

	def reverse(self, event):
		if self.state != "disabled":
			self.state = int(not self.state)
		self.pic = ImageTk.PhotoImage(Image.open(f"customCheckbutton/{self.state}.png").resize(self.size, Image.ANTIALIAS))
		self.label["image"] = self.pic
		if hasattr(self, "active_label"):
			states = {0:["red", "Inactive"], 1:["Green", "Active"]}[self.state]
			self.active_label["fg"] = states[0]
			self.active_label["text"] = states[1]
			self.active_label.pack(side="bottom")


def main():
	root = tk.Tk()
	styledcheck = StyledCheckbutton(root)
	setattr(styledcheck, "active_label", tk.Label(styledcheck, text="Inactive", fg="red"))
	styledcheck.active_label.pack(side='bottom')
	styledcheck.pack()

	root.mainloop()

if __name__ == "__main__":
	main()

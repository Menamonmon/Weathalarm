from Weather import *
from Alarm import *

class MainWindow(tk.Frame):
	def __init__(self, master, windowSize):
		super().__init__(master)
		# sets the settings for the master window 
		self.master = master 
		self.windowSize = windowSize
		self.master.title(formatted_title())
		self.master.geometry(str(windowSize[0]) + "x" + str(windowSize[1]))
		# shows a widow that gives the user 2 options for the app (Weather or Alarm)
		# Also it gives the user the option to exit the app from the beginning
		self.mode_obj = ModeWindow(self.master, self.windowSize, self)


class ModeWindow(tk.Frame):
	# A class the represents the window that gives the user two mode for the app
	def __init__(self, master, windowSize, parent):
		# setting the font size of the text as a factor of the size of the window 
		self.font_size = round(windowSize[0]/20)
		self.master = master
		# imports the image background from the folder and resizes it based on the windowSize parameter
		self.logo = Image.open("weatherIcons\\merged_bg.jpg").resize((round(windowSize[0]*.998), round(windowSize[1]*.998)))
		self.logo = ImageTk.PhotoImage(self.logo)
		self.label = tk.Label(self.master, image=self.logo)
		self.label.grid()
		# Welcoming Label that has a basic description of the program
		self.welcome_label = tk.Label(text="Welcome To Weathalarm,\nAn App That Gives You Both A \nCustomizable Alarm System As Well As \nA Real-time Weather Forcast For Any \nCity You Choose", font="Forte 10", fg="Yellow")
		self.welcome_label.grid(row=0, column=0, sticky=tk.N)
		# A StringVar object that has a default value of "Choose the mode.."
		self.mode_var = tk.StringVar(master=self.master, value="Choose the mode..")
		# A combobox object that lists for the user the 2 possible modes that he can choose from
		self.mode_choice = ttk.Combobox(self.master, textvariable=self.mode_var, values=("Weather", "Alarm"), state="readonly")
		self.mode_choice.grid(row=0, column=0)
		# A button for choosing the option that sets the mode and exits the ModeWindow 
		# as well as another one for exiting the porgram directly
		self.confirm_button = tk.Button(self.master, text="Choose", font=f"Broadway {self.font_size} italic", fg="Blue", command=self.set_mode)
		self.confirm_button.grid(row=0, column=0, sticky=tk.SE)
		self.exit_button = tk.Button(self.master, text="Exit!", font=f"Broadway {self.font_size} italic", fg="Red", command=lambda: self.master.destroy())
		self.exit_button.grid(row=0, column=0, sticky=tk.SW)
		self.showed_false = False
		self.mode = None
		self.parent = parent
		set_all(self.master, bg="#49B7E8")

	def set_mode(self):
		# A function the checks whether the user has chosen a mode
		# if he didn't the window will show him a message telling him 
		# that he has to choose a mode to start the app
		x = self.mode_var.get()
		if x != "Choose the mode..":
			self.parent.mode = self.mode_var.get()
			self.master.destroy()
		else:
			if not self.showed_false:
				self.showed_false = True
				tk.Label(self.master, font=f"Courier {round(self.font_size*.8)} italic", bg="white", text="Wrong Input").grid(row=0, sticky=tk.S)


def main():
	root_main = tk.Tk()
	app = MainWindow(root_main, (300, 300))
	root_main.mainloop()

	if app.mode == "Weather":
		root_weath = tk.Tk()
		app = WeatherWindow(root_weath, (500, 500))
		root_weath.mainloop()

	elif app.mode == "Alarm":
		root_alarm = tk.Tk()
		app = AlarmWindow(root_alarm, (600, 500))
		root_alarm.mainloop()

if __name__ == "__main__":
	main()

# parent = tk.Tk()
# parent.title("MEna GOOGLE")
# parent.geometry("400x500")
# scrolled = ScrollFrame(parent, 400, 500)
# queue = AlarmQueue(parent)
# alarms = [Alarm(queue, "05:00AM", "Morning", 1)]
# # queue.set_alarm_list(alarms)


# queue.pack()
# # scrolled.pack()

# parent.mainloop()

# parent = tk.Tk()
# from tkinter import font
# from copy import copy

# canvas = tk.Canvas(parent)
# scroll_y = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

# frame = tk.Frame(canvas)
# # group of widgets
# for fnt in font.families():
# 	try:
# 		tk.Label(frame, text=fnt, font=fnt + " 20").pack()
# 	except:
# 		tk.Label(frame, text=fnt, font=fnt.replace(" ", "") + " 20")
# # put the frame in the canvas
# canvas.create_window(0, 0, anchor='nw', window=frame)
# # make sure everything is displayed before configuring the scrollregion
# canvas.update_idletasks()

# canvas.configure(scrollregion=canvas.bbox('all'), 
#                  yscrollcommand=scroll_y.set)
                 
# canvas.pack(fill='both', expand=True, side='left')
# scroll_y.pack(fill='y', side='right')

# parent.mainloop()

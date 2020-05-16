from StyledWidgets import *
from operator import gt, lt, ge, le, add, sub


class AlarmWindow(tk.Frame):
	def __init__(self, master, size):
		self.master = master 
		self.master.geometry(f"{size[0]}x{size[1]}")
		# self.master.resizable(0, 0)
		self.master.title("Weathalarm (Alarm Mode)")
		menu_dict = {
			"File": ("Load From File", "Save To File", "Exit"),
			"Alarm": ("Add", "Enabled", "Skip Next Alarm", "Delete", "Edit", "Clone"),
			"Options": ("Run At Windows Startup", "Snooze", "Play Sound", "Single Line")
		}
		self.menu_bar = tk.Menu(self.master)
		self.menu_list = []
		self.pics_dict = {}
		for menu_name, options in menu_dict.items():
			submenu = tk.Menu(self.menu_bar, tearoff=0)
			for option in options:
				if option in {"Load From File", "Save To File", "Exit", "Add", "Delete", "Edit", "Clone"}:
					non_resized = Image.open(f"alarmIcons/{option.split()[0].lower()}_icon.png")
					resized = non_resized.resize((15, 15), Image.ANTIALIAS)
					pic = ImageTk.PhotoImage(resized)
					itemtype = "command"
				else:
					pic = None
					if option in {"Enabled", "Skip Next Alarm", "Run At Windows Startup", "Single Line"}:
						itemtype = "checkbutton"
				self.pics_dict[option] = pic
				submenu.add(itemtype, label=option, image=pic, compound="left")
			self.menu_bar.add_cascade(menu=submenu, label=menu_name)

		self.master.config(menu=self.menu_bar)
		self.queue = AlarmQueue(self.master)
		self.queue.append(Alarm(self.queue, "05:00PM", "Good Morning", 1))
		self.queue.grid(sticky="nsew")
		# self.master.bind("<Configure>", func=self.adjust_widgets_size)

	def adjust_widgets_size(self, event):
		for slave in self.master.winfo_children():
			if slave.winfo_class() == "Frame":
				slave.adjust()

class ScrollFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=width, height=height)          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff", width=width, height=height)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width) 

    def resize(self, width, height):
    	self.config(width=width, height=height)
    	self.canvas.config(width=width, height=height)
    	self.viewPort.config(width=width, height=height)



class AlarmQueue(ScrollFrame):
	def __init__(self, master):
		self.master = master	

		self.master.update_idletasks()

		self.width = self.master.winfo_width()
		self.height = self.master.winfo_height()

		super().__init__(self.master, self.width, self.height)	
		self.resize(self.width, self.height)

		self.master.rowconfigure(0, weight=1)
		self.master.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.alarm_list = []

	def set_alarm_list(self, alarm_list):
		self.alarm_list = alarm_list
		for alarm in self.alarm_list:
			if alarm.visible:
				alarm.pack()	

	def append(self, new_alarm):
		self.alarm_list.append(new_alarm)
		if new_alarm.visible:
			new_alarm.pack()

	def adjust(self):
		# self.master.update_idletasks()
		new_width = self.master.winfo_width()
		new_height = self.master.winfo_height()
		# self.viewPort.geometry(f"{new_width}x{new_height}")
		# self.viewPort.config(width=new_width, height=new_height)
		for alarm in self.alarm_list:
			alarm.fit_in_queue()


class Alarm(tk.LabelFrame):
	def __init__(self, master, alarm_time, name, snooze_time, 
					visible=True, linear=False, tune_name="default", repeat="everyday", bg="yellow"):
		self.visible = visible
		self.linear = linear	
		self.name = name
		# init for the masters
		self.master = master.viewPort
		super().__init__(self.master, bg=bg)
		master.append(self)

		# volume and tune path, name, and label
		self.volume = 100
		self.tune_path = "alarmSounds/" + tune_name + ".mp3"
		self.tune = Sound(self.tune_path, self.volume/10)
		checkSize = (32, 32) if self.linear else (29, 29)
		# Adds an active attribute to the StyledCheckbutton class and binds it to 
		self.checkbox = StyledCheckbutton(self, size=checkSize, bg=bg)
			
		self.repeat = repeat

		# alarm and snooze timing
		self.alarm_time = AlarmTime(alarm_time[:5], alarm_time[5:].upper())
		self.snooze_time = snooze_time

		# labels
		if not self.linear:
			setattr(self.checkbox, "active_label", tk.Label(self.checkbox, text="Active", font=f"Arial {checkSize[0] - 20} bold", fg="Green", bg=bg))
			self.checkbox.active_label.pack(side='bottom')
			self.tune_label = tk.Label(self, text="Tune: " + tune_name.replace("-", " "), font="Vernada 10", bg=bg)
			self.time_label = tk.Label(self, text=repr(self.alarm_time), font="Vernada 13", bg=bg)
			self.name_label = tk.Label(self, text=self.name.capitalize(), font="Vernada 15 bold", bg=bg)
			if self.repeat != None:
				self.rep_label  = tk.Label(self, text="Repeat: " + self.repeat, font="Vernada 9", bg=bg)
		else:
			self.tune_label = tk.Label(self, text=tune_name.replace("-", " "), font="Vernada 8", bg=bg)
			self.time_label = tk.Label(self, text=repr(self.alarm_time), font="Vernada 11", bg=bg)
			self.name_label = tk.Label(self, text=self.name.capitalize(), font="Vernada 13 bold", bg=bg)
			if self.repeat != None:
				self.rep_label  = tk.Label(self, text=self.repeat, font="Vernada 9", bg=bg)
		
		# showing and placing
		self.fit_in_queue()
		self.show()

	def set_volume(self, new_vol):
		self.volume = new_vol
		self.tune.volume = self.volume / 10

	def fit_in_queue(self):
		coeff = .2 if self.linear else .13
		self.config(width=self.master["width"]*.97, height=round(self.master["height"]*coeff))

	def active(self):
		return self.checkbox.state

	def popup(self):
		popup_window = AlarmPopup(self, self.name)

	def show(self):
		if self.visible:
			if self.linear:
				self.checkbox
			else:
				self.checkbox.place(relx=0, rely=0)
				self.name_label.place(relx=.15, rely=0)
				self.time_label.place(relx=.15, rely=.5)
				self.tune_label.place(relx=.4, rely=.1)
				if hasattr(self, "rep_label"):
					self.rep_label.place(relx=.4, rely=.55)



class AlarmPopup(tk.Frame):
	def __init__(self, alarm, title):
		self.alarm = alarm
		self.master = tk.Tk(title)
		self.master.geometry("500x300")
		self.master.resizable(0, 0)
		self.ok_button = tk.Button(self.master, text="Ok!", command=lambda: self.master.destroy())
		snz_time_str = "Snooze (" + alarm.snooze_time + ")" if alarm.snooze_time > 0 else "Snooze"
		self.snooze_button = tk.Button(self.master, text=snz_time_str)
		if snz_time_str == "Snooze":
			self.snooze_button["state"] = "disabled"
		self.time_label = tk.Label(self.master, font="Impact 15 Bold")
		timestr = self.alarm.alarm_time.time_str
		self.timeCompList = [int(timestr[:2]), int(timestr[3:5]), 0, timestr[6:]]
		self.time_label.after(1000, lambda x: self.increment_secs(self.timeCompList))

	def snooze(self):
		my_alarm = self.alarm
		snooze_alarm = Alarm(my_alarm.master, my_alarm.alarm_time, "Snooze For" + my_alarm.name, 0, my_alarm.alarm_queue, False, tune_name=my_alarm.tune_name)
		self.master.destroy()

	def increment_secs(self, comp_list):
		comp_list[2] += 1
		if comp_list[2] > 59:
			comp_list[1] += 1
			if comp_list[1] > 59:
				comp_list[0] += 1
		self.time_label["text"] = formatted_time(comp_list)

	def formatted_time(comp_list):
		return  str(comp_list[0] if comp_list[0] > 9 else "0" + str(comp_list[0])) 
		+ ":" + str(comp_list[1] if comp_list[1] > 9 else "0" + str(comp_list[1])) 
		+ ":" + str(comp_list[2] if comp_list[2] > 9 else "0" + str(comp_list[2])) 
		+ comp_list[3] 


class AlarmTime(object):
	def __init__(self, time_str, am_pm, day=1):
		self.time_str = time_str
		colon_index = time_str.index(":")
		self.hour = int(self.time_str[:colon_index])
		self.minutes = int(self.time_str[colon_index+1:])
		self.am_pm = am_pm
		self.day = day

	def __repr__(self):
		return self.time_str + self.am_pm

	def change(self, minutes, hours=0, sign="+", inplace=False):
		if sign == "+":
			sn = add
			min_limit = 60
			hr_limit = 12
			operation = gt
			rev_sn = sub
		else:
			sn = sub
			min_limit = 0
			hr_limit = 1
			operation = lt
			rev_sn = add
		self.minutes = sn(self.minutes, minutes)
		if operation(self.minutes, min_limit):
			hrs = self.minutes // 60
			self.hour += hrs
			self.minutes -= (hrs) * 60
		self.hour = sn(self.hour, hours)
		am = self.am_pm
		if operation(self.hour, hr_limit):
			num_switches = self.hour//12
			self.hour = rev_sn(self.hour, (12 * num_switches))
			if num_switches%2 == 0:
				self.am_pm = {"AM":"PM", "PM":"AM"}[self.am_pm]
				am = self.am_pm
			if num_switches > 1:
				self.day = sn(self.day, num_switches//2)
		foo = str(self.hour if self.hour > 9 else "0"+str(self.hour)) + ":" + str(self.minutes if self.minutes > 9 else "0"+str(self.minutes))
		if inplace:
			self.time_str = foo
		return AlarmTime(foo, am)


def main():
	root = tk.Tk()
	app = AlarmWindow(root, (600, 500))
	root.mainloop()

if __name__ == "__main__":
	main()
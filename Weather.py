from StyledWidgets import *

class WeatherWindow(tk.Frame):
	def __init__(self, master, size):
		super().__init__(master)
		self.master = master 
		self.master.geometry(f"{size[0]}x{size[1]}")
		self.master.resizable(0, 0)
		self.master.title("Weathalarm (Weather Mode)")
		# A dictionary that has the user interface represetations of the elements of the weather 
		options = {"General":["Temperature", "Max Temperature", "Min Temperature", "Pressure", "Real Feel", "Humidity"],
				   "Wind":["Speed", "Degree"],
				   "Condition":[]}
		deg_options = ["Kelvin", "Celsius", "Fahrenhiet"]
		self.size = size
		self.submit_button = tk.Button(self.master, text="Submit Settings!", font="Impact 10", fg="Blue", command=self.save_settings)
		self.submit_button.place(relx=.835, rely=.96, anchor="c")
		self.option_list = []
		self.deg_var = tk.StringVar(value="Degree")
		self.deg_chooser = ttk.Combobox(self.master, values=deg_options, textvariable=self.deg_var, width=7, state="readonly")
		self.deg_chooser.place(relx=.001, rely=.001)
		row_count = 1
		for father, children in options.items():
			SubCategory(self.master, father, children, self.option_list).grid(row_count)
			row_count += len(children) + 1 if children != None else 1
		self.cityZipEntry = ttk.Entry(self.master, width=20)
		self.cityZipEntry.insert(0, "City/Zip Code")
		self.cityZipEntry.bind("<Button-1>", func=lambda event: on_focus(event, self.cityZipEntry, "City/Zip Code"))
		self.cityZipEntry.bind("<FocusOut>", func=lambda event: out_focus(event, self.cityZipEntry, "City/Zip Code"))
		self.cityZipEntry.place(relx=.1, rely=.9)
		self.missing_args = [0, 0, 0]
		
		
	def save_settings(self):
		deg = self.deg_var.get()
		if deg != "Degree":
			json_dict = {}
			for cat in self.option_list:
				if cat.is_checked():
					json_dict[weatherTransDict[cat.father.cget("text")]] =  [weatherTransDict[child.father.cget("text")] for child in cat.children]
			if len(list(json_dict.keys())) == 0:
				if not self.missing_args[1]:
					self.missing_args[1] = 1
					tk.Label(self.master, text="You need to choose one of the preferences..", fg="Green", font="Impact 8").place(relx=.3, rely=.45)
					return
			self.json_dict = json_dict
			self.json_deg = deg
			city = self.cityZipEntry.get()
			if city != "City/Zip Code":
				self.type = "zip" if city.isnumeric() else "q"
				self.place = city
			else:
				self.type = "q"
				self.place = locate()
			json = fetch_weathdata(self.type, deg, self.place)
			self.old_widgets = self.master.winfo_children()
			timeOfDay = jsonToLabels(json, self.option_list, self.master, self.deg_var.get(), "Forte 15", "Green")
			[slave.destroy() for slave in self.old_widgets]
			if timeOfDay == "n":
				colorMode, txtCol = "#C0C0C0", "#FBFF6C"
			else:
				colorMode, txtCol = "#3090C7", "#D83838"
			set_all(self.master, bg=colorMode, fg=txtCol)
		else:
			if not self.missing_args[0]:
				self.missing_args[0] = 1
				tk.Label(self.master, text="You need to choose a degree..", fg="Red").place(rely=.3, relx=.5)


class SubCategory(object):
	def __init__(self, master, father, children=None, total_list=None, child=False):
		self.master = master
		self.int_var = tk.IntVar(self.master)
		self.father = ttk.Checkbutton(self.master, text=father, var=self.int_var, command=self.activate_subs)
		if child:
			self.father["state"] = "disabled"
		self.children = [] if children == None else [SubCategory(self.master, child, child=True) for child in children]
		if total_list != None:
			total_list.append(self)
		self.is_child = child

	def is_checked(self):
		return self.int_var.get()

	def activate_subs(self):
		new_state = "normal" if self.int_var.get() else "disabled"
		[child.father.config(state
			=new_state) for child in self.children]

	def grid(self, prevs):
		# prevs += 1
		self.father.place(rely=(prevs)/14)
		prevs += 1
		for child in self.children:
			child.father.place(relx=.1, rely=(prevs)/14)
			prevs += 1

def main():
	root = tk.Tk()
	weather = WeatherWindow(root, (500, 500))
	root.mainloop()

if __name__ == "__main__":
	main()
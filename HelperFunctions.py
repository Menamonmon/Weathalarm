import tkinter as tk
from tkinter import  ttk
from PIL import Image, ImageTk
import requests
import calendar
import datetime
import base64
from io import BytesIO
from time import sleep
from pygame import mixer as mx

def locate():
	location = requests.get("https://ipinfo.io").json()
	return location

def fetch_weathdata(loc_type, temp_deg, location=None):
	apiKey = "549ff4cc50710433c1f48d8f3f465d59"
	deg = weatherTransDict[temp_deg] if temp_deg != "Kalvin" else None
	degForCall = f"&units={deg}" if deg != None else ""
	if location == None:
		loc = locate()
		city = loc["city"] + "," + loc["country"] if location != None else location
	else:
		city = location
	loc = location if location != None else locate()
	link = f"https://api.openweathermap.org/data/2.5/weather?{loc_type}={city}{degForCall}&appid={apiKey}"
	json_data = requests.get(link).json()
	return json_data

def fetchCondIcon(iconId):
	url = f"http://openweathermap.org/img/wn/{iconId}@2x.png" 
	response = requests.get(url, stream=True)
	imgdata = base64.encodestring(response.raw.read())
	image = Image.open(BytesIO(base64.b64decode(imgdata)))
	tkimage = ImageTk.PhotoImage(image)
	return tkimage

def set_all(master, **kwargs):
	master.configure(bg=kwargs["bg"])
	for widget in master.winfo_children():
		for key, value in kwargs.items():
			try:
				widget[key] = value
			except:
				pass	

def jsonToLabels(json, requirements, master, tempType, font, txtCol):
	rowCount = 1
	tk.Label(master, text=json["name"] + ", " + json["sys"]["country"], font=font).grid(row=1)
	for req in requirements:
		if req.int_var.get():
			father_text = req.father.cget("text")
			if father_text != "Condition":
				father_label = tk.Label(master, font=font, fg=txtCol, text=req.father.cget("text") + ": ")
				father_label.place(rely=rowCount/12)
				rowCount += 1
				for childreq in req.children:
					if childreq.int_var.get():
						child_text = childreq.father.cget("text")
						if child_text in ("Temperature", "Real Feel", "Max Temperature", "Min Temperature"):
							unit = tempType[0] + "⁰"
						else:	
							unit = units_dict[child_text] if child_text in units_dict.keys() else ""
						try:
							child_label = tk.Label(master, font=font, fg=txtCol, text=(child_text + ": " + str(json[weatherTransDict[father_text]][weatherTransDict[childreq.father.cget("text")]]) + " " + unit))
						except:
							child_label = tk.Label(master, font=font, fg=txtCol, text=(child_text + ": 0" + unit))
						child_label.place(relx=.1, rely=rowCount/12)
						rowCount += 1
			else:
				cond = json["weather"][0]
				con_label = tk.Label(master, font=font, fg=txtCol, text=father_text + ": " + cond["main"])
				con_label.place(rely=rowCount/12)
				img = fetchCondIcon(cond["icon"])
				label = tk.Label(master, image=img)
				label.image = img
				label.place(relx=.6, rely=(rowCount-1.5)/12)
				rowCount += 1
	timeOfDay = json["weather"][0]["icon"][-1]
	return timeOfDay

def formatted_title():
	# A function the returns a string that will be used as a title for the MainWindow
	# that shows the current date and time as well as the name of the app
	str_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	cd = datetime.datetime.now()
	formatted = f"Weathalarm - {str_months[cd.month-1]}, {cd.day}, {cd.year}. {cd.hour}:{cd.minute}."
	return formatted

def on_focus(event, entry, text):
	if entry.get() == text:
		entry.delete(0, "end")

def out_focus(event, entry, text):
	if entry.get() == "":
		entry.insert(0, text)

def switch_active_state(self):
	print("Funct 2 is called")
	states = {0:["red", "Inactive"], 1:["green", "Active"]}[self.state]
	self.active_label["fg"] = states[0]
	self.active_label["text"] = states[1]

superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

subscript_map = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
    "7": "₇", "8": "₈", "9": "₉", "a": "ₐ", "b": "♭", "c": "꜀", "d": "ᑯ",
    "e": "ₑ", "f": "բ", "g": "₉", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ",
    "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "q": "૧", "r": "ᵣ",
    "s": "ₛ", "t": "ₜ", "u": "ᵤ", "v": "ᵥ", "w": "w", "x": "ₓ", "y": "ᵧ",
    "z": "₂", "A": "ₐ", "B": "₈", "C": "C", "D": "D", "E": "ₑ", "F": "բ",
    "G": "G", "H": "ₕ", "I": "ᵢ", "J": "ⱼ", "K": "ₖ", "L": "ₗ", "M": "ₘ",
    "N": "ₙ", "O": "ₒ", "P": "ₚ", "Q": "Q", "R": "ᵣ", "S": "ₛ", "T": "ₜ",
    "U": "ᵤ", "V": "ᵥ", "W": "w", "X": "ₓ", "Y": "ᵧ", "Z": "Z", "+": "₊",
    "-": "₋", "=": "₌", "(": "₍", ")": "₎"}

def toScript(string, subscript=False):
	scriptMap = subscript_map if subscript else superscript_map
	ret_string = ""
	for char in string:
		ret_string += superscript_map[char]
	return ret_string

weatherTransDict = {"General":"main", "Condition":"weather", "Wind":"wind", "Speed":"speed", "Degree":"deg",
					"Temperature":"temp", "Real Feel":"feels_like", "Pressure":"pressure", "Humidity":"humidity", 
					"Kelvin":None, "Celsius":"metric", "Fahrenhiet":"imperial", "Max Temperature": "temp_max", "Min Temperature": "temp_min"}
units_dict = {"Pressure":"psi", "Humidity":"g.kg{}".format(toScript("-1", True)), "Speed":"knots", "Degree": "⁰"}
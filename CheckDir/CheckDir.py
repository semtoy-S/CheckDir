import requests
import tkinter as Tk
from tkinter import ttk
from tkinter import filedialog
from random import randint

Goodanswer = []
BadAnswer = []
Forribden = []

hints = ['Check Your terminal,\nYou can find more information there!','status 200 not a good code sometimes...','@cyber_c0mrades','check out Mac OS and Windows\nVersion of CheckDir','Do not Use This Program\nfor bad things']

random = randint(0,4)


def open_wordlist():
	global total_line_count, wordlist, strokes
	filepath = filedialog.askopenfilename()
	total_line_count = sum(1 for line in open(filepath))
	wordlist = open(filepath, 'r')
	strokes = Tk.Label(mainwindow, text = f'Lines in File: {str(total_line_count)}',font = ('Calibri Light', 12))
	strokes.place(x = 2, y = 182)
	path = Tk.Label(text = f'Path to your list: {filepath}', font = ('Calibri Light', 12))
	path.place(x = 2, y = 159)

def scan():
	global urle, total_line_count, wordlist, Forribden, BadAnswer, Goodanswer, count, isgood, isclosed, isbad, hintlabel, random
	try:
		warningwindow.destroy()
	except NameError:
		pass
	endBtn.destroy()
	askforfile.destroy()
	count = 0
	stop = Tk.Button(text = 'stop immediately', command = stopping)
	stop.place(x = 335, y = 213)
	isgood = Tk.Label(text = 'directories with code 200', font = ('Calibri Light', 12))
	isbad = Tk.Label(text = 'directories with code 404/400/401 and other', font = ('Calibri Light', 12))
	isclosed = Tk.Label(text = 'directories with code 403', font = ('Calibri Light', 12))
	hint['text'] = f'Scanning {url}'
	hintlabel = Tk.Label(text = 'hint: ' + hints[random], font = ('Arial Black', 16))
	hintlabel.place(x = 5, y = 50)
	name = wordlist.readline()
	while count <= total_line_count :
		mainwindow.update()
		req = requests.get(f"{url}{name}")
		if req.status_code == 200:
			print(f"[+] Cool find {req.status_code} --> {url}{name}")
			Goodanswer.append(f"{url}{name}")
			try:
				name = wordlist.readline()
			except ValueError:
				print("File closed? if you if you didn't close the file, try again or try other file")
				break
		elif req.status_code == 404 or req.status_code == 400:
			print(f"[-] Couldn't find {req.status_code} --> {url}{name}")
			BadAnswer.append(f'{url}{name}')
			try:
				name = wordlist.readline()
			except ValueError:
				print("File closed? if you if you didn't close the file, try again or try other file")
				break
		elif req.status_code == 403:
			print(f"Found, But Forribden --> {url}{name}")
			Forribden = [f'{url}{name}']
			try:
				name = wordlist.readline()
			except ValueError:
				print("File closed? if you if you didn't close the file, try again or try other file")
				break
		count = count + 1
		bar['value'] = round((count/total_line_count)*100)
	hint['text'] = f'Scanning Done'
	wordlist.close()
	hintlabel.destroy()
	goodList = ttk.Combobox(values = Goodanswer)
	badlist = ttk.Combobox(values = BadAnswer)
	closedlist = ttk.Combobox(values = Forribden)
	goodList.place(x = 10, y = 10 )
	badlist.place(x = 10, y = 40)
	closedlist.place(x = 10, y = 70)
	isgood.place(x = 220, y = 10)
	isbad.place(x = 220, y = 40)
	isclosed.place(x = 220, y =70)
def stopping():
	wordlist.close()
	goodList = ttk.Combobox(values = Goodanswer)
	badlist = ttk.Combobox(values = BadAnswer)
	closedlist = ttk.Combobox(values = Forribden)
	hintlabel.destroy()
	goodList.place(x = 10, y = 10 )
	badlist.place(x = 10, y = 40)
	closedlist.place(x = 10, y = 70)
	isgood.place(x = 220, y = 10)
	isbad.place(x = 220, y = 40)
	isclosed.place(x = 220, y =70)


def IwantUrl():
	global urle, urllabel, nextBtn
	urllabel = Tk.Label(text = 'Input your URL')
	urllabel.place(x = 190, y =1)
	urle = ttk.Entry()
	urle.place(x = 140, y = 31)
	nextBtn = Tk.Button(text = 'Next Step', command = askingfile)
	nextBtn.place(x = 190, y = 61)

def askingfile():
	global url, askforfile, endBtn
	url = urle.get()
	urle.delete
	urle.destroy()
	nextBtn.destroy()
	urllabel.destroy()
	askforfile = Tk.Button(text = 'Choose your Wordlist', command = open_wordlist)
	urlabel = Tk.Label(text = f'you have choosed {url} as your target', font = ('Calibri Light', 12))
	urlabel.place(x = 2, y = 135)
	askforfile.place(x = 150, y = 1)
	endBtn = Tk.Button(text = 'Start Searching', command = Prescan)
	endBtn.place(x = 170, y = 31)

def Prescan():
	global urle, wordlist, prwords, name
	count = 0
	CountAll = 0
	CountRef = 0
	hint['text'] = f'Pre-scanning {url}, wait for 5 seconds... '
	check()
	name = prwords.readline()
	while count <= 9 :
		req = requests.get(f"{url}{name}")
		if req.status_code == 200:
			CountAll = CountAll + 1
			name = prwords.readline()
			print(f'allowed {CountAll}')
			print(f"Prescaned {url}{name}: ALLOWED")
		else: #req.status_code == 404 or req.status_code == 403 or req.status_code == 400:
			CountRef = CountRef + 1
			name = prwords.readline()
			print(f'refused {CountRef}')
			print(f"Prescaned {url}{name}: REFUSED")
		count = count + 1
	if CountAll == 10:
		warn()
	else:
		scan()
def check():
	global prwords, prepath
	try:
		global prepath
		prwords = open('words.txt', 'r')
	except FileNotFoundError:
		issue1()
def issue1():
	global prwords
	FileNowindow = Tk.Toplevel()
	FileNowindow.title('issue#1 File Not Found')
	tect = Tk.Label(FileNowindow, text = "CheckDir  can't find a 'words.txt file'!\n Please choose this file in program folder.")
	tect.pack()
	choo = Tk.Button(FileNowindow, text = 'ok, i will choose', command = solve1)
	choo.pack()

def solve1():
	global prwords, prepath
	prepath = filedialog.askopenfilename()



def warn():
	global warningwindow
	warningwindow = Tk.Toplevel()
	warningwindow.title('Spirit Activity')
	text = Tk.Label(warningwindow, text = 'WAIT... PRE-SCAN SHOWED AN ANOMALY ON THE SITE!\n Perhaps, The Site Is Protected From Checking Directories', font = ('Arial Black', 18))
	text.pack()
	ok = Tk.Button(warningwindow, text = 'ОК', command = scan)
	ok.pack()
	
#Главное Окно приложения 
mainwindow = Tk.Tk()
mainwindow.geometry('483x240')
mainwindow.title('CheckDir 0.13')
mainwindow.resizable(False, False)
bar = ttk.Progressbar(orient = 'horizontal',length = 478, mode = 'determinate')
bar.place(x = 2, y = 202)
hint = Tk.Label(text = 'Waiting For Tasks...')
hint.place(x = 3, y = 217)
IwantUrl()
mainwindow.mainloop()
from tkinter import *

from random import randint
from datetime import datetime
import sys
import os
FONT = ("Verdana", 12)
class GameSetup(Tk):

    def __init__(self):
        Tk.__init__(self)
        package = Frame(self)
        package.pack(side="top", fill="both", expand=True)
        self.frames = {}
        for i in (StartPage, PageOne, PageTwo):
            frame = i(package, self)

            self.frames[i] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        menu = Menu(self)
        self.config(menu=menu)
        exitMenu = Menu(menu, tearoff=0)
        restartMenu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Exit", menu=exitMenu)
        menu.add_cascade(label="Restart", menu=restartMenu)

        restartMenu.add_command(label="Retart Application", command=self.restart)
        exitMenu.add_command(label="Exit", command=self.exit)

    def show_frame(self, x):
        frame = self.frames[x]
        frame.tkraise()

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def exit(self):
        app.destroy()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu", font=FONT)
        label.pack(pady=10, padx=10)
        label1 = Label(self, text="Please Choose your Shape and Colour :)", font=FONT)
        label1.pack(pady=10, padx=10)

        button = Button(self, text="Advanced Version", width=15,
                        command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = Button(self, text="Basic Version", width=15,
                         command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        self.shape_option = StringVar()
        self.circle = Radiobutton(self, text="Circle", command=self.choose_shape, width=15, anchor="w",
                                  variable=self.shape_option,
                                  value="circle")
        self.circle.pack()
        self.rec = Radiobutton(self, text="Rectangle", command=self.choose_shape, width=15, anchor="w",
                               variable=self.shape_option,
                               value="rec")
        self.rec.pack()

        self.can = Canvas(self)
        self.can.pack()
        self.option = StringVar()

        self.red = Radiobutton(self.can, text="Red", command=self.make_colour, bg="red", anchor="w",
                               variable=self.option, value="red", width=15)
        self.red.pack()
        self.green = Radiobutton(self.can, text="Green", command=self.make_colour, bg="green", anchor="w",
                                 variable=self.option, value="green", width=15)
        self.green.pack()
        self.pink = Radiobutton(self.can, text="Pink", command=self.make_colour, bg="pink", anchor="w",
                                variable=self.option, value="pink", width=15)
        self.pink.pack()
        self.orange = Radiobutton(self.can, text="Orange", command=self.make_colour, bg="orange", variable=self.option,
                                  value="orange", width=15, anchor="w")
        self.orange.pack()
        label2 = Label(self, text="INSTRUCTIONS", font=FONT)
        label2.pack(pady=10, padx=10)
        label3 = Label(self, text="1. Click the shape when it appears(unless its blue)", font=FONT)
        label3.pack(pady=10, padx=10, anchor="w")
        label4 = Label(self,
                       text="2. Click the cyan shape to reset the speed! and gain a life,  Its a race against the clock!",
                       font=FONT)
        label4.pack(pady=10, padx=10, anchor="w")
        label5 = Label(self, text="3. Click the gold shape to get double points :)", font=FONT)
        label5.pack(pady=10, padx=10, anchor="w")

    def choose_shape(self):
        global make_shape
        make_shape = str(self.shape_option.get())

    def make_colour(self):
        global set_colour
        set_colour = str(self.option.get())


counter = 0
missed_score = 0
highscore = 0
make_shape = None
set_colour = None
gold_shape = 0
life = 5


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.timer_tracker = 2000
        self.levelup = 100
        self.game_number = 1
        self.incriment = 1
        self.longest = 0
        self.deletions = 0
        self.total = 0
        self.blues = 0
        self.tracker = False
        self.colours = ""
        self.canvas = Canvas(self, width=600, height=600, highlightthickness=1, highlightbackground="red")
        self.canvas.pack(side=LEFT, anchor=N)

        self.reset_game = Button(self, text="RESET GAME", height=3, width=18, bg="red", command=self.reset)
        self.reset_game.pack(side=TOP, anchor=N, pady=1)
        self.restart_full_game = Button(self, text="BACK TO MAIN MENU", height=3, width=18, bg="red",
                                        command=self.restart_full)
        self.restart_full_game.pack(side=TOP, anchor=N, pady=1)
        self.quit_game = Button(self, text="QUIT", height=3, width=18, bg="red", command=self.close_window)
        self.quit_game.pack(side=TOP, anchor=N, pady=1)

        self.score = Label(self, text="Score: 0", height=3, width=18, bg="red")
        self.score.pack(side=TOP, anchor=N, pady=1)
        self.game_num = Label(self, text="Game Number: 1", height=3, width=18, bg="red")
        self.game_num.pack(side=TOP, anchor=N, pady=1)
        self.longest_game = Label(self, text="Longest Game: 0", height=3, width=18, bg="red")
        self.longest_game.pack(side=TOP, anchor=N, pady=1)
        self.lives = Label(self, text="Lives: 5", height=3, width=18, bg="red")
        self.lives.pack(side=TOP, anchor=N, pady=1)
        self.missed = Label(self, text="Missed: 0", height=3, width=18, bg="red")
        self.missed.pack(side=TOP, anchor=N, pady=1)

        self.high_score = Label(self, text="High Score: 0", height=3, width=18, bg="red")
        self.high_score.pack(side=TOP, anchor=N, pady=1)

        self.start_button = Button(self, text="Click to Start", command=self.make)

        self.start_button.pack(side=TOP, anchor=N, pady=2)

    def make(self):
        self.milliseconds2 = datetime.now()

        self.master.after(1000, self.start_button.pack_forget())
        x = randint(0, 560)
        y = randint(0, 560)

        if make_shape == "rec":
            self.button1 = self.canvas.create_rectangle(x, y, x + 40, y + 40, fill='red')
        elif make_shape == "circle":
            self.button1 = self.canvas.create_oval(x, y, x + 40, y + 40, fill='red')
        elif make_shape == None:
            self.button1 = self.canvas.create_rectangle(x, y, x + 40, y + 40, fill='red')
        if set_colour:
            self.canvas.itemconfig(self.button1, fill=set_colour)

        self.canvas.tag_bind(self.button1, '<Button 1>', self.delete)
        self.master.after(2000, self.timer_delete)
        return self.button1

    def shape_generator(self):

        x = randint(0, 560)
        y = randint(0, 560)

        self.canvas.coords(self.button1, x, y, x + 40, y + 40)
        global counter
        if counter >= 5:

            col = randint(1, 100)
            if 0 <= col <= 49:
                self.colours = "red"
            elif 50 <= col <= 79:
                self.colours = "blue"
            elif 80 <= col <= 94:
                self.colours = "gold"
            elif 95 <= col <= 100:
                self.colours = "cyan"
            self.canvas.itemconfigure(self.button1, fill=self.colours)
            self.color = self.colours
        if self.total & 5 == 0:
            self.timer_tracker = self.timer_tracker - self.levelup
            self.levelup += 100
            if self.timer_tracker <= 750:
                self.timer_tracker = 750

        else:
            self.canvas.itemconfigure(self.button1, fill=set_colour)
        self.canvas.itemconfigure(self.button1, state='normal')

        self.canvas.tag_bind(self.button1, '<Button 1>', self.delete)

        self.master.after(self.timer_tracker, self.timer_delete)
        return self.button1

    def delete(self, event):
        self.tracker = True
        self.deletions += 1
        self.canvas.itemconfigure(self.button1, state='hidden')
        global counter
        global life
        global gold_shape

        gold_shape = 0

        if counter >= 5:
            x = self.canvas.itemcget(self.button1, "fill")
            if str(x) == "blue":
                life -= 1
            elif str(x) == "cyan":
                life += 1
                self.timer_tracker = 2000
                self.levelup = 100
            elif str(x) == "gold":
                counter += 2
                gold_shape += 1


            else:
                counter += self.incriment

        else:
            counter += 1

        if life <= 0:
            self.master.after(100, lambda: self.reset())

        self.score['text'] = "Score: " + str(counter)
        self.lives['text'] = "Lives: " + str(life)
        return self.tracker

    def timer_delete(self):
        self.total += 1
        self.canvas.itemconfigure(self.button1, state='hidden')

        self.master.after(250, lambda: self.shape_generator())

        global missed_score
        global counter
        global life
        global gold_shape

        check = self.canvas.itemcget(self.button1, "fill")
        if counter >= 5:
            if str(check) == "blue":
                self.blues += 1
            else:
                if self.tracker == True:
                    life += 0
                else:

                    life -= 1
        if counter < 5:
            if self.tracker == True:
                life += 0
            elif self.tracker == False:
                life -= 1
        missed_score = self.total - self.blues - self.deletions
        if missed_score < 0:
            missed_score = 0

        self.missed['text'] = "Missed: " + str(missed_score)
        self.lives['text'] = "Lives: " + str(life)
        if life <= 0:
            self.master.after(100, lambda: self.reset())
        self.tracker = False

    def reset(self):
        # can use this for longest game
        self.timer_tracker = 2000
        if self.game_number > 1:
            if self.total >= 1:
                self.milliseconds1 = datetime.now()
                x = round((self.milliseconds1 - self.milliseconds2).total_seconds(), 2)
                if x > self.longest:
                    self.longest = x
            else:
                x = 0.00
        else:
            x = 0.00
        self.game_number += 1

        self.longest_game['text'] = "Longest Game: " + str(x) + "(s)"
        global highscore

        x = self.canvas.create_text(300, 50, text="RESET GAME...", font=30)
        self.master.after(1000, lambda: self.canvas.delete(x))
        global life
        global counter
        global highscore
        if counter > highscore:
            highscore = counter
        else:
            highscore = highscore

        self.high_score['text'] = "High Score: " + str(highscore)
        self.game_num['text'] = "Game Number: " + str(self.game_number)
        global missed_score
        missed_score = 0
        self.missed['text'] = "Missed: " + str(missed_score)

        counter = 0
        life = 5
        self.score['text'] = "Score: " + str(counter)
        self.lives['text'] = "Lives: " + str(life)

    def close_window(self):

        app.destroy()

    def restart_full(self):
        os.execl(sys.executable, sys.executable, *sys.argv)


class PageTwo(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.game_number = 0
        self.incriment = 1
        self.counter = 0

        self.canvas = Canvas(self, width=600, height=600)
        self.canvas.pack(side=BOTTOM)

        self.start_button = Button(self, text="Click to Start", command=self.make)

        self.start_button.pack(side=TOP, anchor=N)
        self.score = Label(self, text="Score: 0", height=3, width=10, bg="red")
        self.score.pack(side=LEFT, anchor=N)

    def make(self):
        self.master.after(1000, self.start_button.pack_forget())

        x = randint(0, 560)
        y = randint(0, 560)

        if make_shape == "rec":
            self.button1 = self.canvas.create_rectangle(x, y, x + 40, y + 40, fill='red')
        elif make_shape == "circle":
            self.button1 = self.canvas.create_oval(x, y, x + 40, y + 40, fill='red')
        elif make_shape == None:
            self.button1 = self.canvas.create_rectangle(x, y, x + 40, y + 40, fill='red')
        global set_colour
        if set_colour:
            self.canvas.itemconfig(self.button1, fill=set_colour)

        self.canvas.tag_bind(self.button1, '<Button 1>', self.delete)
        self.master.after(2000, self.timer_delete)
        return self.button1

    def shape_generator(self):

        x = randint(0, 560)
        y = randint(0, 560)

        self.canvas.coords(self.button1, x, y, x + 40, y + 40)

        self.canvas.itemconfigure(self.button1, state='normal')

        self.canvas.tag_bind(self.button1, '<Button 1>', self.delete)
        self.master.after(2000, self.timer_delete)

    def delete(self, event):
        self.canvas.itemconfigure(self.button1, state='hidden')
        global counter
        counter += 1

        self.score['text'] = "Score: " + str(counter)

    def timer_delete(self):
        self.canvas.itemconfigure(self.button1, state='hidden')

        self.master.after(10, lambda: self.shape_generator())


app = GameSetup()
app.mainloop()

'''
Extra Functionality
- Multiple Classes across multiple windows, there is a window to set up the game, a window for the required features, and a window with the extra features

- There is a drop down menu with the ability to quit the application and another to restart it

- On the set up menu, there is the basic instructions of how the game works, it allows you to pick your shape and colour and which  
version of the game you would like to play. 

- On the added features window there is:
~ a button to reset the current game
~ a button to return to the main menu
~ a button to quit the application
~ a label to display the score
~ a label to display the missed shapes
~ a label which will display your overall high score
~ a label to display your longest game
~ a start button 

The extra rules I have implemented
~ Click the base colour for 1 point
~ If a blue appears you must let it pass, if you click it you lose a life
~ If a gold appears you get 2 points if you click it
~ If a cyan appears it resets the timer and gives you another life
Every 5 scores the timer decreases so the user has less time to click before the shape dissappears and they miss a score, if you click too many blue squares the game will reset
'''
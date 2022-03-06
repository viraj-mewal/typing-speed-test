from tkinter import *
import time
import threading
import random

'''
Formulas :-
Gross Speed / WPM - (characters/5)/time [time in min]
Net Speed :- ((characters/5)/time) - errors
Accuracy :-  (Net Speed/Gross Speed ) * 100
'''


class Window:
    def __init__(self):
        # self.sentences = ['Try to type this if you can', 'Another try to type this sentence is here', 'Python is just cool as we can create cool things with it']
        self.words = 20
        self.runned = False
        self.errors = 0
        self.counter = 0
        self.thread_running = False
        self.font = ("Comic Sans MS",20,"bold")
        with open('sent.txt', 'r') as f: self.temp_sentences = f.read().split('\n')
        self.sentences = self.createSent()
        self.choice = random.choice(self.sentences)
        self.temp_choice = self.temp_sentences[self.sentences.index(self.choice)]
        self.win = Tk()
        self.win.title("Typing Speed Test")
        self.win.configure(bg='black')
        self.win.resizable(False, False)
        self.draw()
        self.win.mainloop()

    def draw(self):
        self.sentence = Label(self.win, text=self.choice, fg='white', bg='black', font=self.font)
        self.sentence.grid(row=0, column=0, columnspan=2, padx=20, pady=20)


        self.entry_var = StringVar()
        self.entry = Entry(self.win, textvariable=self.entry_var, font=self.font, fg='black', bg='white', width=50)
        self.entry.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        self.entry.bind('<KeyRelease>', self.event)

        self.stats = Label(self.win, text="WPM - 00\nACCURACY - 00\nERRORS - 00", fg='white', bg='black', font=self.font)
        self.stats.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        self.reset_btn = Button(self.win, text="Reset", font=("Comic Sans MS",30), bg='gold', fg='red', command=self.reset)
        self.reset_btn.grid(row=3, column=0, padx=20, pady=20)

    def event(self, event):
        if not self.thread_running and not self.runned:
            if not event.keycode in [16, 17, 18]:
                self.runned = True
                self.thread_running = True
                self.t = threading.Thread(target=self.threadEvent)
                self.t.start()

     
        if not self.sentence.cget('text').replace('\n', '').startswith(self.entry.get()):
            self.entry.config(fg='red')
            self.errors += 1
        else:
            self.entry.config(fg='black')
        if self.entry.get() == self.temp_choice:
            self.entry.config(fg='green')
            self.thread_running = False

        # print(self.t.is_alive())


    def threadEvent(self):
        while self.thread_running:
            try:
                self.counter += 0.3
                time.sleep(0.3)
                wpm = round((len(self.entry.get().split(" ")) / self.counter)*60, 2)
                net = round(wpm-self.errors, 2)
                accuracy = round((net/wpm)*100, 2)
                self.stats.config(text=f'WPM - {wpm}\n Accuracy - {accuracy}\n Errors - {self.errors}')
            except:
                pass


    def createSent(self):
        words = 10
        lst = []
        f_lst = []
        temp_str = ''
        for i in self.temp_sentences:
            temp = i.split(' ')
            for i in range(words,len(temp)+1,words):
                try:
                    temp[i] = temp[i] + '\n'
                except:
                    continue
            for i in temp:
                temp_str += i + ' '
            lst.append(temp_str)
            temp_str = ''

        return lst

    def reset(self):
        self.thread_running = False
        self.runned = False
        self.errors = 0
        self.counter = 0
        self.choice = random.choice(self.sentences)
        self.temp_choice = self.temp_sentences[self.sentences.index(self.choice)]
        self.sentence.config(text=self.choice)
        self.entry.delete(0, END)
  


if __name__ == '__main__':
    Window()
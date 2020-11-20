import tkinter as tk, random, string, contextlib
from tkinter import messagebox
with contextlib.redirect_stdout(None): import pygame

def initiateQuestions():
    global questionsUsed, allQuestions, registerSpam
    registerSpam = False
    questionsUsed = []
    file = open("questions.txt", "r")
    allQuestions = [l.split("\n") for l in file.read().split("\n\n")]
    file.close()

def userCheck(username, password):
    file = open("database.txt", "r")
    database = file.read().split("\n")
    file.close()
    for user in database:
        if user.split(",")[0] == username:
            if user.split(",")[1] == password:
                return True
    return False

def userRegister(username, password):
    global registerSpam
    validChars = list(string.ascii_lowercase) + list(string.digits) + ["."]
    if len([char for char in username.lower() if char in validChars]) != len(username):
        return (False, 0)
    if len([char for char in password.lower() if char in validChars]) != len(password):
        return (False, 0)
    if ((5<=len(username)<=15) and (5<=len(password)<=15)) == False:
        return (False, 1)
    if registerSpam == True:
        return (False, 2)
    file = open("database.txt", "a")
    file.write("\n"+username+","+password+",0")
    file.close()
    registerSpam = True
    return True

def updateScore(username, score):
    file = open("database.txt", "r")
    database = file.read().split("\n")
    file.close()
    for i in range(len(database)):
        if database[i].split(",")[0] == username:
            database[i] = ",".join(database[i].split(",")[0:2])+","+str(score)
    file = open("database.txt", "w")
    database = file.write("\n".join(database))
    file.close()

def randomQuestion():
    index = random.randint(0, len(allQuestions)-1)
    if len(questionsUsed) == len(allQuestions): return None
    while index in questionsUsed: index = random.randint(0, len(allQuestions)-1)
    questionsUsed.append(index)
    return allQuestions[index], str(index+1)

class gui:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.forceClose)
        self.menu()
        pygame.mixer.init()
        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play(-1)

            
    def menu(self):
        self.frame = tk.Frame(self.master)

        self.font = "Courier"
        self.score = 0
        
        self.lbl1 = tk.Label(self.frame, text = 'E-Safety Quiz', height=2, font=(self.font, 48)).grid(row=0, column=0, columnspan=3)       
        self.btn1 = tk.Button(self.frame, text = 'Start', command = self.login, width=15, height=2, font=(self.font, 28)).grid(row=1, column=0)
        self.space1 = tk.Label(self.frame).grid(row=1, column=1)
        self.btn2 = tk.Button(self.frame, text = 'Quit', command = self.close, width=15, height=2, font=(self.font, 28)).grid(row=1, column=2)
        self.lbl2 = tk.Label(self.frame, text = 'By Akram Ziane', height = 3, font=(self.font, 20)).grid(row=2, column=0, columnspan=3, sticky="SW")
        self.frame.pack()        

    def login(self):
        def user(event=None):
            username, password = self.entryUser.get().lower(), self.entryPass.get()
            if username == "admin" and password == "admin":
                self.lbl2.config(text="Logged in as Adminisrator!")
                self.lbl2.after(1500, self.admin)
            elif username == "" or password == "":
                self.lbl2.config(text="Fields cannot be empty!")
                self.entryUser.focus()
            else:
                if userCheck(username, password) == False:
                    self.lbl2.config(text="Invalid Credentials!")
                    self.entryUser.delete(0, tk.END)
                    self.entryPass.delete(0, tk.END)
                    self.entryUser.focus()
                else:
                    self.lbl2.config(text="Login Success!")
                    self.username = username
                    self.restart()
    
        def register(event=None):
            username, password = self.entryUser.get().lower(), self.entryPass.get()
            if username == "" or password == "":
                self.lbl2.config(text="Please enter details!")
            else:
                register = userRegister(username, password)
                if register == (False, 0):
                    self.lbl2.config(text="Invalid characters detected!")
                elif register == (False, 1):
                    self.lbl2.config(text="Length must be between 5 and 15!")
                elif register == (False, 2):
                    self.lbl2.config(text="You have already registered!")
                else:
                    self.lbl2.config(text="User Registered!")
                self.entryUser.delete(0, tk.END)
                self.entryPass.delete(0, tk.END)
                self.entryUser.focus()

        self.frame.destroy()
        self.frame = tk.Frame(self.master)

        self.lbl1 = tk.Label(self.frame, text = "Login or Register", height=2, font=(self.font, 36)).grid(row=0, column=0, columnspan=2)       

        self.lblUser = tk.Label(self.frame, text = "Username ", font=(self.font, 24)).grid(row=1, column=0)
        self.entryUser = tk.Entry(self.frame, width = 24, font=(self.font, 22))
        self.entryUser.grid(row=1, column=1)
        self.entryUser.focus()
        
        self.lblPass = tk.Label(self.frame, text = "Password ", font=(self.font, 24)).grid(row=2, column=0)
        self.entryPass = tk.Entry(self.frame, width = 24, font=(self.font, 22), show="\u2022")
        self.entryPass.grid(row=2, column=1)

        self.lbl2 = tk.Label(self.frame, text = "", height=4, font=(self.font, 18))
        self.lbl2.grid(row=3, column=0, columnspan=2, sticky="w")

        self.btn1 = tk.Button(self.frame, text = 'Login', command = user, width=8, height=2, font=(self.font, 20))
        self.btn1.grid(row=3, column=1, sticky="ne", pady = 10)
        self.master.bind("<Return>", user)

        self.btn1 = tk.Button(self.frame, text = 'Register', command = register, width=8, height=1, font=(self.font, 14), highlightthickness=0)
        self.btn1.grid(row=3, column=1, sticky="se")

        self.frame.pack()

    def quiz(self, event=None):
        self.master.unbind("<Return>")
        self.frame.destroy()
        self.frame = tk.Frame(self.master)
        self.Question = randomQuestion()
        
        if self.Question == None:
            self.end()
        else:
            self.question = self.Question[0]   
            self.master.geometry("{}x{}+{}+{}".format(windowWidth+windowHeight, windowHeight, positionRight-int(windowHeight/2), positionDown))
            self.canvas = tk.Canvas(self.frame, width = 250, height = 250)      
            self.img = tk.PhotoImage(file="images/"+self.Question[1]+".gif")
            self.canvas.pack(side = "left")
            self.canvas.create_image(0,0, anchor="nw", image=self.img)   

            words = self.question[0].split()
            para = " ".join(words[0: int(len(words)/2)+1]) + "\n" + " ".join(words[int(len(words)/2)+1: len(words)])
            self.lbl1 = tk.Label(self.frame, text = para, width=40, height=2, font=(self.font, 24, "bold"))
            self.lbl1.pack(pady=20)
            self.var1, self.var2, self.var3 = tk.IntVar(), tk.IntVar(), tk.IntVar()
            self.questionShuffle = [self.question[1], self.question[2], self.question[3]]
            random.shuffle(self.questionShuffle)
            
            self.chkbtn1 = tk.Checkbutton(self.frame, text=self.questionShuffle[0], variable=self.var1, font=(self.font, 18))
            self.chkbtn1.pack(anchor="w", padx=20)
            self.chkbtn2 = tk.Checkbutton(self.frame, text=self.questionShuffle[1], variable=self.var2, font=(self.font, 18))
            self.chkbtn2.pack(anchor="w", padx=20)
            self.chkbtn3 = tk.Checkbutton(self.frame, text=self.questionShuffle[2], variable=self.var3, font=(self.font, 18))
            self.chkbtn3.pack(anchor="w", padx=20)
            self.lbl2 = tk.Label(self.frame, text = "", height=4, font=(self.font, 18))
            self.lbl2.pack(side = "left", padx=20)
            self.btn1 = tk.Button(self.frame, text = 'Submit', command = self.sumbit, width=8, height=2, font=(self.font, 22))
            self.btn1.pack(side = "right", padx=20, pady=15)
            self.frame.pack()
            self.master.bind("<Escape>", self.quiz) # Interupt 

    def message(self):
        words = self.question[4].split()
        para = " ".join(words[0: int(len(words)/2)+1]) + "\n" + " ".join(words[int(len(words)/2)+1: len(words)])
        self.btn1.destroy()
        self.lbl2.pack_forget()
        self.lbl2.pack(padx=20, pady=15)
        self.lbl2.config(text = para)
        self.lbl2.after(5000, self.quiz)
         
    def sumbit(self):
        if self.var1.get() == self.var2.get() == 1 or self.var1.get() == self.var3.get() == 1 or self.var2.get() == self.var3.get() == 1:
            self.lbl2.config(text = "Tick only one box!")
            self.var1.set(0), self.var2.set(0), self.var3.set(0)
        elif self.var1.get() == 0 and self.var2.get() == 0 and self.var3.get() == 0:
            self.lbl2.config(text = "You must answer!") 
        else:
            if ((self.var1.get() == 1 and self.questionShuffle[0] == self.question[3]) or
            (self.var2.get() == 1 and self.questionShuffle[1] == self.question[3]) or
            (self.var3.get() == 1 and self.questionShuffle[2] == self.question[3])):
                self.lbl2.config(text = "Correct!")
                self.score += 1
                self.lbl2.after(1000, self.message)       
            else:
                self.lbl2.config(text = "Incorrect!")
                self.lbl2.after(1000, self.message)
                
    def admin(self):
        self.frame.destroy()
        admin = cp(self.master)
        #self.master.mainloop()

    def end(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.master)
        self.master.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

        updateScore(self.username, self.score)

        self.lbl1 = tk.Label(self.frame, text = 'You scored '+str(self.score)+"/"+str(len(allQuestions))+"!", height=2, font=(self.font, 40)).grid(row=0, column=0, columnspan=3)       
        self.btn1 = tk.Button(self.frame, text = 'Restart', command = self.restart, width=15, height=2, font=(self.font, 28)).grid(row=1, column=0)
        self.space1 = tk.Label(self.frame).grid(row=1, column=1)
        self.btn2 = tk.Button(self.frame, text = 'Logout', command = self.login, width=15, height=2, font=(self.font, 28)).grid(row=1, column=2)
        self.btn2 = tk.Button(self.frame, text = 'Quit', command = self.close, width=15, height=2, font=(self.font, 28)).grid(row=2, column=2, sticky="N",pady=10)
        self.lbl2 = tk.Label(self.frame, text = 'By Akram Ziane', height = 3, font=(self.font, 20)).grid(row=2, column=0, columnspan=3, sticky="SW", pady=25)
        self.frame.pack()

    def restart(self):
        initiateQuestions()
        self.score = 0
        self.quiz()

    def close(self):
        pygame.mixer.music.stop()
        self.master.destroy()
    def forceClose(self):
        if messagebox.askokcancel("Quit", "Data may not be saved!\nAre you sure you want to quit?"):
            pygame.mixer.music.stop()
            self.master.destroy()

class cp():
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.forceClose)
        self.panel()

    def panel(self):

        self.frame = tk.Frame(self.master)

        self.font = "Courier"
        self.score = 0
        
        self.lbl1 = tk.Label(self.frame, text = 'Admin Control Panel', height=2, font=(self.font, 48)).grid(row=0, column=0, columnspan=3)       
        self.btn1 = tk.Button(self.frame, text = 'Edit Questions', command = self.frame.destroy, width=15, height=2, font=(self.font, 28)).grid(row=1, column=0)
        self.space1 = tk.Label(self.frame).grid(row=1, column=1)
        self.btn2 = tk.Button(self.frame, text = 'Manage Images', command = self.master.destroy, width=15, height=2, font=(self.font, 28)).grid(row=1, column=2)
        
        self.btn3 = tk.Button(self.frame, text = 'Logout', command = self.frame.destroy, width=15, height=2, font=(self.font, 28)).grid(row=2, column=0)
        
        self.btn4 = tk.Button(self.frame, text = 'Quit', command = self.close, width=15, height=2, font=(self.font, 28)).grid(row=2, column=2)
        
        self.frame.pack()

    def logout(): pass
        

    def close(self):
        pygame.mixer.music.stop()
        self.master.destroy()
    def forceClose(self):
        if messagebox.askokcancel("Quit", "Data may not be saved!\nAre you sure you want to quit?"):
            pygame.mixer.music.stop()
            self.master.destroy()
                
def main():
    global windowHeight, windowWidth, positionRight, positionDown
    root = tk.Tk()
    screenWidth, screenHeight = root.winfo_screenwidth(), root.winfo_screenheight()
    windowWidth, windowHeight = 600, 250
    positionRight, positionDown = int(screenWidth/2 - windowWidth/2), int(screenHeight/2 - windowHeight/2)-100
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
    root.title("E-Safety Quiz")
    root.resizable(0, 0)
    app = gui(root)
    root.mainloop()
    
initiateQuestions()
if __name__ == '__main__':
    main()

from tkinter import *
from tkinter import messagebox
import tkinter.font
import re
import sqlite3 as sql
import math

root = Tk()

class Menu():
    def __init__(self):
        self.title = ("The Man Who Will Become The Pirate King!")
        self.geometry = ("750x375")
        self.image = PhotoImage(file="PirateBackground.png")
        self.font = tkinter.font.Font(family="Helvetica",size=10)
        self.fg = "white"
        self.login_counter = 0
        self.login_success = False
        self.start_success = False
        self.username_used = ""


    def Main_Menu(self):
        
        
        root.geometry(self.geometry)
        root.title(self.title)
        bg_label = Label(root, image = self.image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        Main_MenuTitle = Label(root, text = self.title, font = self.font, fg = self.fg, bg = "#40E0D0")
        Main_MenuTitle.pack(pady=0)

        #creating frame
        main_menu_frame = Frame(root)
        main_menu_frame.pack(pady=20)

        #adding buttons
        register_button = Button(main_menu_frame, text="Register", command=self.Register)
        register_button.grid(row=0, column=0)

        login_button = Button(main_menu_frame, text="Login", command=self.Login)
        login_button.grid(row=0, column=1)

    def Register(self):
        self.register_screen = Toplevel(root)
        self.register_screen.title(self.title)
        self.register_screen.geometry("750x375")

        self.username_registry = StringVar()
        self.password_registry = StringVar()

        Label(self.register_screen, text = "Please register details below:").pack()
        Label(self.register_screen, text = "").pack()

        Label(self.register_screen, text = "Username").pack()
        self.username_entry_registry = Entry(self.register_screen, textvariable = self.username_registry)
        self.username_entry_registry.pack()
        Label(self.register_screen, text = "").pack()
        Label(self.register_screen, text = "Password").pack()
        self.password_entry_registry = Entry(self.register_screen, textvariable = self.password_registry)
        self.password_entry_registry.pack()
        Label(self.register_screen, text = "").pack()

        Button(self.register_screen, text = "Register", width = 10, height = 1, command = self.CheckIfRegistryValid).pack()

    def CheckIfRegistryValid(self):
        pattern = "[A-Z]+[a-z]+[0-9]"
        if (re.search(pattern, self.password_registry.get())):
            username = self.username_registry.get()
            getUsername = (username,)
            con = sql.connect("Users.db")
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS "Users" (
            "Username"	TEXT NOT NULL,
            "Password"	TEXT NOT NULL
    );
    ''')
            con.commit()
            con.close()
            con = sql.connect("Users.db")
            cur = con.cursor()
            cur.execute('\
            SELECT Username FROM Users\
            WHERE Username = ?',getUsername)
            user = cur.fetchone()
            if getUsername == user:
                self.Error("User already exists!")
                self.register_screen.destroy()
                self.Register()
            else:
                self.RegisterUser()
                self.Success()
                self.register_screen.destroy()
        else:
            self.Error("""Password not strong enough:
password should start with a capital letter,
consist of lowercase letters
and end with a number.""")
            self.register_screen.destroy()
            self.Register()
        

    def RegisterUser(self):
        password = self.password_registry.get()
        password = self.Hash_Algorithm(password)
        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS "Users" (
	"Username"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL
        );
        ''')
        con.commit()
        con.close()
        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute("INSERT INTO Users(Username, Password) VALUES(?, ?)",(self.username_registry.get(), password))
        con.commit()
        con.close()
        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS "Scores" (
	"Username"	TEXT NOT NULL,
	"Highscore"	INTEGER NOT NULL
        );
        ''')
        con.commit()
        con.close()
        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute("INSERT INTO Scores(Username, Highscore) VALUES(?, ?)",(self.username_registry.get(), 0))
        con.commit()
        con.close()


    def CheckLoginDetails(self):
        username = self.username_login.get()
        password = self.password_login.get()


        password = self.Hash_Algorithm(password)

        getUsername = (username,)
   

        self.username_entry_login.delete(0, END)
        self.password_entry_login.delete(0, END)
        
        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute('\
        SELECT Password FROM Users\
        WHERE Username = ?',getUsername)
        try:
            getPassword = cur.fetchone()[0]
            if getPassword == password:
                self.Login_Success()
                self.login_screen.destroy()
                self.username_used = username
                self.login_success = True
            else:
                self.Error("Password Incorrect")
                self.login_counter += 1
                self.login_screen.destroy()
                self.Login()
        except:
            self.Error("User Not Found!")
            self.login_counter += 1
            self.login_screen.destroy()
            self.Login()

    def Hash_Algorithm(self, string):
        hash_string = ''
        for i in string:
            ascii_value = ord(i)
            if ascii_value % 2 == 0:
                x_value = (ascii_value)/((math.log10(ascii_value))**7.4)
            else:
                x_value = (ascii_value) * 1.18/((math.log(ascii_value))**2.9)
            numerator = x_value **(math.sin(math.tan((math.e)**x_value)))
            denominator = math.log((math.e ** (x_value * math.cos(x_value))), x_value)
            hash_number = numerator/denominator
            if hash_number < 0:
                hash_number *= -1
            for i in str(hash_number):
                try:
                    if int(i) > 0:
                        digits = int(i)
                        break
                except:
                    pass
            if digits > 6:
                digits = 6
            sum_ascii = 0
            for i in range(len(string)):
                sum_ascii += int(ord(string[i])) * i

            product_ascii = 1
            for i in range(len(string)):
                if i > 0:
                    product_ascii *= int(ord(string[i])) * i
                else:
                    product_ascii *= int(ord(string[i]))

            temp = str(sum_ascii/product_ascii)
            additive = '0.'
            for i in temp:
                if i.isdigit():
                    additive += i
            hash_number += float(additive)
            char_achieved = []
            start_index = str(hash_number).index('.') + 1
            while len(char_achieved) < digits:
                if 32 <= int(str(hash_number)[start_index:start_index+3]) <= 127:
                    char = chr(int(str(hash_number)[start_index:start_index+3]))
                    char_achieved.append(char)
                elif 32 <= int(str(hash_number)[start_index:start_index+2]) <= 99:
                    char = chr(int(str(hash_number)[start_index:start_index+2]))
                    char_achieved.append(char)
                start_index += 1
            for char in char_achieved:
                hash_string += char
        return hash_string



    def Login(self):
        if self.login_counter < 3:
            self.login_screen = Toplevel(root)
            self.login_screen.title(self.title)
            self.login_screen.geometry("750x375")
            Label(self.login_screen, text = "Please enter details below to login:").pack()
            Label(self.login_screen, text = "").pack()

            self.username_login = StringVar()
            self.password_login = StringVar()
            
            Label(self.login_screen, text = "Username").pack()
            self.username_entry_login = Entry(self.login_screen, textvariable = self.username_login)
            self.username_entry_login.pack()
            Label(self.login_screen, text = "").pack()
            Label(self.login_screen, text = "Password").pack()
            self.password_entry_login = Entry(self.login_screen, textvariable = self.password_login)
            self.password_entry_login.pack()
            Label(self.login_screen, text = "").pack()
            Button(self.login_screen, text = "Login", width = 10, height = 1, command = self.CheckLoginDetails).pack()
        else:
            self.CloseError("Login Unsuccessful Too Many Times!")
            self.login_success = False
            



    

    def Success(self):
        success_screen = Toplevel(root)
        success_screen.title("Success!")
        success_screen.geometry("375x100")

        Label(success_screen, text = "Successful!", fg="green").pack()
        Label(success_screen, text = "").pack

        Button(success_screen, text = "OK", width = 10, height = 1, command = success_screen.destroy).pack()

    def Error(self,text):
        error_screen = Toplevel(root)
        error_screen.title("Error!")
        error_screen.geometry("375x195")
        Label(error_screen, text = text).pack()
        Button(error_screen, text = "OK", width = 10, height = 1, command = error_screen.destroy).pack()

    def CloseError(self,text):
        close_error_screen = Toplevel(root)
        close_error_screen.title("Error!")
        close_error_screen.geometry("375x195")
        Label(close_error_screen, text = text).pack()
        Button(close_error_screen, text = "OK", width = 10, height = 1, command = root.destroy).pack()
        

    def run(self):
        root.mainloop()

    def Login_Success(self):
        login_success_screen = Toplevel(root)
        login_success_screen.title("Success!")
        login_success_screen.geometry("375x100")

        Label(login_success_screen, text = "Successful!", fg="green").pack()
        Label(login_success_screen, text = "").pack

        Button(login_success_screen, text = "OK", width = 10, height = 1, command = login_success_screen.destroy).pack()
        root.withdraw()
        self.Main_Game_Menu()

    def Main_Game_Menu(self):
        
        main = Toplevel(root)
        main.title(self.title)
        main.geometry(self.geometry)
        bg_label = Label(main, image = self.image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        Main_Game_MenuTitle = Label(main, text = self.title, font = self.font, fg = self.fg, bg = "#40E0D0")
        Main_Game_MenuTitle.pack(pady=10)

        #creating frame
        main_game_menu_frame = Frame(main)
        main_game_menu_frame.pack(pady=20)

        #adding buttons
        start_button = Button(main_game_menu_frame, text="Start", command = self.start)
        start_button.grid(row=0,column=0)

        leaderboard_button = Button(main_game_menu_frame, text="Leaderboard", command = self.display_leaderboard)
        leaderboard_button.grid(row=0,column=1)

        controls_button = Button(main_game_menu_frame, text="Controls", command = self.controls)
        controls_button.grid(row=0,column=2)

        exit_button = Button(main_game_menu_frame, text="Exit", command = quit)
        exit_button.grid(row=0,column=3)

    def start(self):
        root.destroy()
        self.start_success = True

    def controls(self):
        controls_screen = Toplevel(root)
        controls_screen.title(self.title)
        controls_screen.geometry(self.geometry)
        bg_label = Label(controls_screen, image = self.image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Controls_ScreenTitle = Label(controls_screen, text = ("""> - Move Right \n
< - Move left \n
SPACEBAR - Jump"""), font = self.font, fg = self.fg, bg = "#40E0D0")
        Controls_ScreenTitle.pack(pady=15)
        
        Button(controls_screen, text = "Back", width = 10, height = 1, command = controls_screen.destroy).pack()

    def display_leaderboard(self):
        score_array=[]
        user_array=[]
        
        leaderboard_screen = Toplevel(root)
        leaderboard_screen.title(self.title)
        leaderboard_screen.geometry(self.geometry)
        bg_label = Label(leaderboard_screen, image = self.image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        con = sql.connect("Users.db")
        cur = con.cursor()
        cur.execute("SELECT Highscore FROM Scores")
        records =  cur.fetchall()
        for row in records:
            for i in row:
                score_array.append(i)
        self.merge_sort(score_array)
        cur.execute("SELECT Username FROM Scores ORDER BY Highscore")
        users = cur.fetchall()
        for row in users:
            for i in row:
                user_array.append(i)

        x = len(user_array)

        Leaderboard_ScreenTitle = Label(leaderboard_screen, text = ("""1. """, user_array[x-1],""" - """, score_array[x-1],"""\n
2. """, user_array[x-2],""" - """, score_array[x-2],"""\n
3. """, user_array[x-3],""" - """, score_array[x-3]), font = self.font, fg = self.fg, bg = "#40E0D0")
        Leaderboard_ScreenTitle.pack(pady=15)

        Button(leaderboard_screen, text = "Back", width = 10, height = 1, command = leaderboard_screen.destroy).pack()
        
                                        

        
        

    def merge_sort(self, array):
        if len(array) > 1:
            left_array = array[:len(array)//2]
            right_array = array[len(array)//2:]

            #recursion
            self.merge_sort(left_array)
            self.merge_sort(right_array)

            #merge
            i = 0
            j = 0
            k = 0
            while i < len(left_array) and j < len(right_array):
                if left_array[i] < right_array[j]:
                    array[k] = left_array[i]
                    i += 1
                else:
                    array[k] = right_array[j]
                    j += 1
                k += 1

            while i < len(left_array):
                array[k] = left_array[i]
                i += 1
                k += 1

            while j < len(right_array):
                array[k] = right_array[j]
                j += 1
                k += 1





    



            
        
menu = Menu()
menu.Main_Menu()
        
        

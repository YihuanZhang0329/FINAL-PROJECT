
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import all the required  modules
import os
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from tkinter import simpledialog
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import colorchooser


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        
        # initialization
        self.avatar_path = "avatar.png" 
        self.avatar_cache = {} 
    
        # Import modules
        from PIL import Image, ImageTk, ImageDraw
        import os
    
        # Create default avatar
        try:
            if os.path.exists(self.avatar_path):
                img = Image.open(self.avatar_path).resize((40, 40))
            else:
                img = Image.new('RGB', (40, 40), color='gray')
                draw = ImageDraw.Draw(img)
                draw.text((10, 10), "?", fill='white')
            self.default_avatar = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"error in initialization: {e}")
            # create a backup image
            img = Image.new('RGB', (40, 40), color='gray')
            self.default_avatar = ImageTk.PhotoImage(img)
    
        # pre upload
        self.avatar_cache[self.sm.get_myname()] = self.default_avatar

    def login(self):
    # login window
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(bg="#F0F0F0", width=400, height=300)

    # Title Label
        self.pls = Label(self.login,
                     text="Welcome to Chat!",
                     justify=CENTER,
                     font="Helvetica 16 bold",
                     bg="#F0F0F0")
        self.pls.place(relheight=0.15, relx=0.25, rely=0.07)

    # Name Label
        self.labelName = Label(self.login,
                           text="Username:",
                           font="Helvetica 12",
                           bg="#F0F0F0")
        self.labelName.place(relheight=0.1, relx=0.15, rely=0.25)

    # Input Field
        self.entryName = Entry(self.login,
                           font="Helvetica 14")
        self.entryName.place(relwidth=0.5, relheight=0.08, relx=0.35, rely=0.25)
        self.entryName.focus()

    # Continue Button
        self.go = Button(self.login,
                     text="→ Enter Chat",
                     font="Helvetica 13 bold",
                     bg="#FFFFFF", fg="black",
                     activebackground="#ffffff",
                     relief="flat", 
                     command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.35, rely=0.5, relwidth=0.3, relheight=0.12)

        self.Window.mainloop()
  
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    def layout(self, name):
        import subprocess
        from PIL import Image, ImageTk

        self.name = name
        self.Window.deiconify()
        self.Window.title("💬 Chatroom")
        self.Window.geometry("800x600")
        self.Window.resizable(width=True, height=True)
        self.Window.configure(bg="#ECECEC")
        
    
        # Main Frame
        self.main_frame = Frame(self.Window, bg="#ECECEC")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Left Sidebar
        self.sidebar = Frame(self.main_frame, bg="#F0F0F0", width=200)
        self.sidebar.pack(side=LEFT, fill=Y)

       # Avatar
        try:
            self.avatar_image = Image.open(self.avatar_path),((80, 80))
        except:
            self.avatar_image = Image.new("RGB", (80, 80), color="gray")
        self.avatar_photo = ImageTk.PhotoImage(self.avatar_image)
        self.avatar_label = Label(self.sidebar, image=self.avatar_photo, bg="#F0F0F0")
        self.avatar_label.pack(pady=20)

        #upload button
        self.upload_button = Button(self.sidebar, text="Upload your Avatar", font="Helvetica 12",
                                    command=self.upload_avatar)
        self.upload_button.pack(pady=3,fill=X)
        
        #Chatroom title
        self.title_button = Button(self.sidebar,
                           text="💬 Chatroom Title",
                           font="Helvetica 12",
                           bg="white", fg="black",
                           command=self.prompt_new_title)
        self.title_button.pack(pady=3, fill=X)
        
        #Background color
        self.bgcolor_button = Button(self.sidebar,
                              text="🎨 Chat BG Color",
                              font="Helvetica 12",
                              bg="white", fg="black",
                              command=self.choose_chat_bg_color)
        self.bgcolor_button.pack(pady=3, fill=X)

        #Time
        self.time_button = Button(self.sidebar,
                          text="🕒 Time",
                          font="Helvetica 12",
                          bg="white", fg="black",
                          command=self.show_time)
        self.time_button.pack(pady=3, fill=X)

        #Command Area
        self.command_frame = Frame(self.sidebar, bg="#F0F0F0")
        self.command_frame.pack(pady=25, fill=X)

        Button(self.command_frame, text="Log Out", font="Helvetica 12",
            bg="white", fg="black", command=lambda: self.sendButton("q")).pack(pady=3, fill=X)
        
        Button(self.command_frame, text="Quit Chat", font="Helvetica 12",
            bg="white", fg="black", command=lambda: self.sendButton("bye")).pack(pady=3, fill=X)

        Button(self.command_frame, text="Online Users", font="Helvetica 12",
            bg="white", fg="black", command=lambda: self.sendButton("who")).pack(pady=3, fill=X)

        Button(self.command_frame, text="Connect", font="Helvetica 12",
            bg="white", fg="black", command=self.connect_user_dialog).pack(pady=3, fill=X)

        Button(self.command_frame, text="Search in Chatting History", font="Helvetica 12",
            bg="white", fg="black", command=self.search_term_dialog).pack(pady=3, fill=X)

        Button(self.command_frame, text="Shakespeare Sonnet", font="Helvetica 12",
            bg="white", fg="black", command=self.get_poem_dialog).pack(pady=3, fill=X)


        # Game button area(Vertically Arranged)
        self.game_frame = Frame(self.sidebar, bg="#F0F0F0")
        self.game_frame.pack(pady=12, fill=X)


        #Minesweeper
        self.game_button = Button(self.sidebar,
                              text="💣 Minesweeper",
                              font="Helvetica 12",
                              bg="white", fg="black",
                              command=self.launch_minesweeper)
        self.game_button.pack(pady=5, padx=4, fill=X)

        #Tic Tac Toe
        self.ttt_button = Button(self.sidebar,
                         text="🎮 Tic-Tac-Toe",
                         font="Helvetica 12",
                         bg="white", fg="black",
                         command=self.launch_tic_tac_toe)
        self.ttt_button.pack(pady=4, padx=10, fill=X)

        #Right Sidebar
        self.chat_area = Frame(self.main_frame, bg="#ECECEC")
        self.chat_area.pack(side=LEFT, fill=BOTH, expand=True) 
    
        # label head
        self.labelHead = Label(self.chat_area,
                           bg="#4A90E2", fg="white",
                           text=f"Logged in as: {self.name}",
                           font="Helvetica 14 bold", pady=10)
        self.labelHead.place(relwidth=1, rely=0)

        self.line = Label(self.chat_area, bg="#D1D1D1")
        self.line.place(relwidth=1, rely=0.08, relheight=0.005)

    #textcon
        self.textCons = Text(self.chat_area,
                         bg="#FFFFFF", fg="#333333",
                         font="Helvetica 12",
                         wrap=WORD, padx=10, pady=10)
        self.textCons.place(relheight=0.7, relwidth=0.96, rely=0.09, relx=0.02)

    #scrollbar
        scrollbar = Scrollbar(self.textCons)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textCons.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.textCons.yview)


        self.quickFrame = Frame(self.chat_area, bg="#ECECEC")
        self.quickFrame.place(relx=0.02, rely=0.78, relwidth=0.96, relheight=0.04)

    #emoji button
        self.emoji_button = Button(self.quickFrame,
                           text="Select Emoji",
                           font="Helvetica 12",
                           bg="white", fg="black",
                           command=self.open_emoji_picker)
        self.emoji_button.pack(side=LEFT, padx=6)
        
    # quick send buttons
        quick_phrases = ["Hello!", "Bye!", "Who are you?", "I love ICDS.", "Haha"]
        for phrase in quick_phrases:
            btn = Button(self.quickFrame,
                     text=phrase,
                     font="Helvetica 12",
                     bg="white", fg="black",
                     command=lambda p=phrase: self.quick_send(p))
            btn.pack(side=LEFT, padx=6)

    # entry and send button
        self.labelBottom = Frame(self.chat_area, bg="#DDDDDD")
        self.labelBottom.place(relwidth=1, rely=0.825, relheight=0.18)

        self.entryMsg = Entry(self.labelBottom,
                          bg="white", fg="#333333",
                          font="Helvetica 12")
        self.entryMsg.place(relwidth=0.74, relheight=0.5, rely=0.25, relx=0.02)
        self.entryMsg.focus()
        self.entryMsg.bind("<Return>", self.on_enter_key)

        self.buttonMsg = Button(self.labelBottom,
                            text="Send",
                            font="Helvetica 12 bold",
                            bg="#FFFFFF", fg="black",
                            activebackground="#FFFFFF",
                            highlightbackground="#FFFFFF",
                            relief="flat",
                            command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.78, rely=0.25, relheight=0.5, relwidth=0.2)

        self.textCons.config(state=DISABLED)
   
    def connect_user_dialog(self):
        user = simpledialog.askstring("Connect", "Enter Username:", parent=self.Window)
        if user:
            self.sendButton(f"c{user.strip()}")

    def search_term_dialog(self):
        term = simpledialog.askstring("Search", "Enter search keyword:", parent=self.Window)
        if term:
            self.sendButton(f"?{term.strip()}")

    def get_poem_dialog(self):
        number = simpledialog.askstring("Shakespeare Sonnet", "Enter sonnet number:", parent=self.Window)
        if number and number.isdigit():
            self.sendButton(f"p{number.strip()}")

    def prompt_new_title(self):
        from tkinter import simpledialog
        new_title = simpledialog.askstring("Edit Title", "Please enter the new Chatroom title:", parent=self.Window)
        if new_title:
            self.Window.title(new_title)
    
    def choose_chat_bg_color(self):
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Choose Chat Display Background")[1]
        if color:
            self.textCons.configure(bg=color)

    def on_enter_key(self, event):
        self.sendButton(self.entryMsg.get())
        
    def quick_send(self, text):
        self.entryMsg.delete(0, END)
        self.entryMsg.insert(0, text)
        self.sendButton(text)

    def upload_avatar(self):
        """Handle avatar upload"""
        try:
        # Open file selection dialog
            file_types = [
            ("Image files", "*.png"),
            ("Image files", "*.jpg"),
            ("Image files", "*.jpeg"),
            ("All files", "*.*")
            ]
            file_path = filedialog.askopenfilename(
                title="Select avatar image",
                filetypes=file_types
                )
        
            # User canceled selection
            if not file_path:
                return
            try:
            # Read and compress avatar
                img = Image.open(file_path)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
            
            # Save as temp file for transfer
                temp_path = "temp_avatar.png"
                img.save(temp_path, "PNG")
            
            # Read as byte data
                with open(temp_path, "rb") as f:
                    avatar_data = f.read()
            
            # Send to server
                msg = json.dumps({
                "action": "upload_avatar",
                "name": self.sm.get_myname(),
                "avatar": avatar_data.hex()  # Convert binary to hex string for transmission
                })
                self.send(msg)
            
            # Update local display
                self.avatar_photo = ImageTk.PhotoImage(img)
                self.avatar_label.config(image=self.avatar_photo)
                self.avatar_label.image = self.avatar_photo
                # Update cache
                self.avatar_cache[self.sm.get_myname()] = self.avatar_photo
            
            # Delete temp file
                os.remove(temp_path)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error processing avatar: {str(e)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload avatar: {str(e)}")

    def sendButton(self, msg):
        msg = msg.strip()
        self.textCons.config(state=NORMAL)
        if msg == "":
            return
        
        self.textCons.config(state=NORMAL)
        self.textCons.see(END)
        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)
        self.my_msg = msg 

    def display_message(self, sender, message):

        self.textCons.config(state=NORMAL)
    
    # get avatars
        if sender not in self.avatar_cache:
            if sender == self.sm.get_myname():  # own avatars
                try:
                    avatar = Image.open(self.avatar_path).resize((40, 40))
                    self.avatar_cache[sender] = ImageTk.PhotoImage(avatar)
                except:
                    self.avatar_cache[sender] = self.default_avatar
            else:  
                self.avatar_cache[sender] = self.default_avatar
    
    # import avators
        self.textCons.image_create(END, image=self.avatar_cache[sender])
    
    # import names and messages
        self.textCons.insert(END, f" {sender}: {message}\n", 
                        'right' if sender == self.sm.get_myname() else 'left')
    
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
                
    def proc(self):

        buffer = ""
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            if self.socket in read:
                buffer += self.recv()  # append new data to buffer

        # 提取完整的 JSON 消息
            messages = []
            while True:
                try:
                    if not buffer.strip():
                        break
                    obj, idx = json.JSONDecoder().raw_decode(buffer)
                    messages.append(obj)
                    buffer = buffer[idx:].lstrip()  # remove parsed part
                except json.JSONDecodeError:
                    break  # incomplete JSON, wait for more data

            for msg in messages:
                if isinstance(msg, dict):
                    action = msg.get("action")

                # 处理头像更新
                    if action == "update_avatar":
                        try:
                            sender = msg["name"]
                            avatar_data = bytes.fromhex(msg["avatar"])
                            from io import BytesIO
                            img = Image.open(BytesIO(avatar_data)).resize((40, 40))
                            avatar_img = ImageTk.PhotoImage(img)
                            self.avatar_cache[sender] = avatar_img
                        except Exception as e:
                            print(f"处理头像更新失败: {e}")

                # 处理聊天消息
                    elif "from" in msg and "message" in msg:
                        sender = msg["from"]
                        content = msg["message"]

                    # 如果该消息包含头像数据，则更新头像缓存
                        if "avatar" in msg:
                            try:
                                from io import BytesIO
                                avatar_data = bytes.fromhex(msg["avatar"])
                                img = Image.open(BytesIO(avatar_data)).resize((40, 40))
                                avatar_img = ImageTk.PhotoImage(img)
                                self.avatar_cache[sender] = avatar_img
                            except Exception as e:
                                print(f"解析消息内头像失败: {e}")

                    # 如果缓存中还没有这个用户头像，则使用默认头像
                        if sender not in self.avatar_cache:
                            self.avatar_cache[sender] = self.default_avatar

                        self.display_message(sender, content)

        # 自己发的消息处理
            if self.my_msg:
                response = self.sm.proc(self.my_msg, "")
                self.display_message(self.sm.get_myname(), self.my_msg)
                self.my_msg = ""
                if response.strip(): 
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, response + "\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

    def launch_minesweeper(self):
        import subprocess
        try:
            subprocess.Popen(["python", "minesweeper.py"])
        except Exception as e:
            print(f"error in launching minesweeper game: {e}")
    
    def launch_tic_tac_toe(self):
        from TicTacToe import TicTacToeController, LocalTicTacToeWindow
        controller = TicTacToeController()
        LocalTicTacToeWindow(controller, "X")
        LocalTicTacToeWindow(controller, "O")

    def show_time(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.textCons.config(state='normal')
        self.textCons.insert('end', f"Time is:: {now}\n")
        self.textCons.config(state='disabled')
        self.textCons.see('end')

    def open_emoji_picker(self):

        if hasattr(self, 'emoji_picker') and self.emoji_picker.winfo_exists():
            self.emoji_picker.lift()
            return

        self.emoji_picker = Toplevel(self.Window)
        self.emoji_picker.title("Select Emoji")

        emojis = [
    "😀", "😂", "😍", "😎", "🤔", "😢", "😡", "❤️", "🙏", "👍",
    "👏", "🔥", "🥳", "😴", "🤩", "😇", "🤗", "🙄", "😤", "🤐",
    "😱", "🤯", "😈", "👻", "💩", "💔", "🎉", "🌟", "🍀", "☀️",
    "🌈", "🍎", "🍕", "🎵", "🚀", "⚽", "🎲", "📚", "💡", "🔔",
    "💤", "🍺", "🎁", "📅", "✈️", "🏆", "🥇", "🧩", "🦄", "🐱",
    "🐶", "🐼", "🐸", "🌹", "🍓", "🍉", "🍔", "🍟", "🌍", "💻",
    "🎯", "🎬", "🛒", "📷", "📱", "⚡"
]
        
        cols = 6
        rows = (len(emojis) + cols - 1) // cols

        btn_width = 60 
        btn_height = 30
        padx = 5
        pady = 5

        width = cols * (btn_width + 2 * padx)
        height = rows * (btn_height + 2 * pady)

        self.emoji_picker.geometry(f"{width}x{height}")
        self.emoji_picker.resizable(True, True)

        row = 0
        col = 0
        for emoji in emojis:
            btn = Button(self.emoji_picker,
                     text=emoji,
                     font=("Helvetica", 14),
                     width=3,
                     command=lambda e=emoji: self.select_emoji(e))
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

    def select_emoji(self, emoji):
        self.entryMsg.insert(END, emoji)
        if hasattr(self, 'emoji_picker') and self.emoji_picker.winfo_exists():
            self.emoji_picker.destroy()
    
    def run(self):
        self.login()

# create a GUI class object
if __name__ == "__main__": 
    g = GUI()

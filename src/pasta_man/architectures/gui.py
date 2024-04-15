#
# This is the pmanager class file
#

# import project specific modules
import sys
from pasta_man.architectures.targets import targets
from pasta_man.encryption import Encryption
from pasta_man.utilities.pasta_menu import __menu__

# import libs
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from os.path import join as jPath
from pathlib import Path
import pyperclip
import threading

class pmanager:
    def __init__(self, master:Tk, masterpassword: bytes):
        # create a master object
        self.parent = master
        # set title
        self.parent.title('Pasta-Man')
        # set geometry
        self.parent.geometry('530x300+400+280')
        # set architecture
        self.arch = targets(masterpassword)
        
        # set menu
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        # -> add menus
        self.pasta_menu = __menu__(menuparent=menu)
        self.pasta_menu.Themes()
        
        # create Enclosing Frame
        self.EF = ttk.Frame(self.parent)
        self.EF.pack(fill=BOTH, expand=True)
        
        self.initthread = threading.Thread(target=self.arch.init).start()
    
    def _makeinitscreen_(self):
        # create two notebooks
        # -> Add and Get --> Get will have submods
        self.notebook = ttk.Notebook(self.EF)
        self.notebook.pack(expand=True, fill=BOTH)
        
        # -> create the tabs --> Add
        self.hometab = Frame(self.notebook, bg='black')
        self.addtab = ttk.Frame(self.notebook)
        self.gettab = ttk.Frame(self.notebook)
        
        # -> add the tabs under notebook
        self.notebook.add(self.hometab, text='Home')
        self.notebook.add(self.addtab, text='Add')
        self.notebook.add(self.gettab, text='Fetch')
        
        # -> invoke _makeHome)=_ to create Home screen
        self._makeHome_()
        
        # -> invoke _makeAdd_ to create Add Screen
        self._makeAdd_()
        
        # -> invoke _makeFetch_ to create Fetch Screen
        self._makeFetch_()
    
    def _makeHome_(self):
        # -> create Enclosing frame
        self.HEF = Frame(self.hometab, bg='black')
        self.HEF.pack(expand=True, fill=BOTH)
        
        # -> Create gif frames OR LABEL
        self.homelabel = Label(self.HEF, text="Pasta-Man is your very own Password Manager\nWith tripple layer security and the all new search.", font=('Verdana', 18))
        self.homelabel.place(anchor='center', relx=0.5, rely=0.35)
        
        self.homelabel.config(bg='black', fg='white')
        
        # -> create a button
        self.homeNextLabel = Label(self.HEF, text="Next >", bg='black', fg='white', font=('Verdana', 15))
        self.homeNextLabel.place(anchor='center', relx=0.5, rely=0.67)
        
        # -> bind command
        self.homeNextLabel.bind('<Button-1>', lambda e: self.homenext())
    
    def homenext(self):
        self.notebook.select(1)
        # -> set focus to targetEntry
        self.targetEntry.focus()
    
    def _makeFetch_(self):
        # -> create eclosing frame under Fetch
        self.FEF = ttk.Frame(self.gettab)
        self.FEF.pack(fill=BOTH, expand=True)
        
        # # -> find targets and fetch it later
        # t1 = threading.Thread(target=self.arch.targets)
        # t1.start()
        
        # -> create search Entry and label
        self.searchLabel = ttk.Label(self.FEF, text='Search:', font=('Verdana', 14))
        self.searchLabel.place(anchor='center', relx=0.12,rely=0.16 )
        
        # ---> Entry
        self.varsearch = StringVar()
        self.varsearch.set('hint: search keywords')
        self.searchEntry = ttk.Entry(self.FEF, textvariable=self.varsearch, width=24)
        self.searchEntry.place(anchor='center', relx=0.295, rely=0.3)
        
        # -> create search button
        self.searchbutton_var = StringVar()
        self.searchbutton_var.set('[ Search ]')
        self.searchbutton = ttk.Button(self.FEF, text='[ Search ]', default=ACTIVE, command=self.search, textvariable=self.searchbutton_var)
        self.searchbutton.place(anchor='center', relx=0.5, rely=0.65)
        
        # -> create target type label
        self.tarLabel = ttk.Label(self.FEF, text='Type:', font=('Verdana', 14))
        self.tarLabel.place(anchor='center', relx=0.67,rely=0.16)
        
        # -> create dropdown menu.
        # ----> create a var for option
        self.varoption = StringVar()
        # t1.join()
        self.targtypelist = ttk.OptionMenu(self.FEF, self.varoption, *['target', 'target-type', 'username'])
        self.targtypelist.place(anchor='center', relx=0.75, rely=0.3, relwidth=0.35)
        
        # -> create a status label
        self.fetchstatusvar = StringVar()
        self.fetchstatus = ttk.Label(self.FEF, textvariable=self.fetchstatusvar)
        self.fetchstatus.place(anchor='center', relx=0.5, rely=0.79)
    
    def search(self):
        # -> fetch value and search:
        t1 = threading.Thread(target=self.arch.search, args=(self.varsearch.get(), self.varoption.get()))
        t1.start()
        t1.join()
        
        if self.arch.__searchresult__!=None:
            self.fetchstatusvar.set('Match Found!')
            self.fetchstatus.after(5000, self.updatefetch)
        else:
            self.fetchstatusvar.set('No Match!')
            self.fetchstatus.after(4000, self.fetchstatusReset)
    
    def updatefetch(self):
        # -> forget fetch status
        self.fetchstatus.place_forget()
        self.fetchstatus.place(anchor='center', relx=0.5, rely=0.5)
        # -> rename search button and forget it
        # self.searchbutton_var.set('[ Re-Search ]')
        self.searchbutton.place_forget()
        # self.searchbutton.place(anchor='center')
        
        # -> create 3 buttons => copy to clipboard, Remove, Re-search
        self.copyToClipboardButton = ttk.Button(self.FEF, text='[ Copy To Clipboard ]', default=ACTIVE, command=self.copyToClipboard)
        self.removeButton = ttk.Button(self.FEF, text='[ Remove ]', command=self.remove)
        self.researchButton = ttk.Button(self.FEF, text='[ Re-Search ]', command=self.research)
        
        self.copyToClipboardButton.place(anchor='center', relx=0.24, rely=0.62)
        self.removeButton.place(anchor='center', relx=0.54, rely=0.62)
        self.researchButton.place(anchor='center', relx=0.8, rely=0.62)
    
    def research(self):
        # reinit the _makeFetch_ to refresh newly added Entries
        for widget in self.gettab.winfo_children():
            widget.destroy()
        
        self._makeFetch_()
    
    def remove(self):
        dump = self.arch.data.pop(self.arch.data.index(self.arch.__searchresult__))
        dump = None
        
        # reinit the _makeFetch_ to refresh newly added Entries
        for widget in self.gettab.winfo_children():
            widget.destroy()
        
        self._makeFetch_()
    
    
    def copyToClipboard(self):
        
        # prepare alleged pass
        allegedpass = simpledialog.askstring("Master Password", "Enter Master Password to copy password to clipboard: ")
        
        # get masterpass
        with open(jPath(str(Path.home()), '.pastaman', '.m'), 'rb') as m:
            masterpassword = m.read() # this is encrypted
        
        def decryptthread(masterpassword: str):
            denc = Encryption("pastaman".encode('ascii'), masterpassword.encode('ascii'))
            denc.unlock()
            self.den = denc.__unencryptedstring__
            sys.exit(0)
        
        
        t1 = threading.Thread(target=decryptthread, args=(masterpassword.decode('ascii'),))
        t1.start()
        t1.join()
        
        
        if allegedpass == self.den.decode('ascii'):
            t = threading.Thread(target=self.arch.decrypt, args=(self.arch.__searchresult__['password'],))
            t.start()
            t.join()
            
            pyperclip.copy(self.arch._dec_)
            spam = pyperclip.paste()
            self.arch._dec_ = None
        else:
            messagebox.showwarning("Wrong Master Password", "The master password entered by you is wrong!")
        
    def _makeAdd_(self):
        # -> create enclosing frame under Add
        self.AEF = ttk.Frame(self.addtab)
        self.AEF.pack(expand=True, fill=BOTH)
        
        # -> create target label and input
        self.targetLabel = ttk.Label(self.AEF, text='Target:')
        self.targetLabel.place(anchor='center', relx=0.24, rely=0.16)
        # --> textvar for targetEntry
        self.vartarget = StringVar()
        self.targetEntry = ttk.Entry(self.AEF, width=25, textvariable=self.vartarget)
        self.targetEntry.place(anchor='center', relx=0.57, rely=0.16)
        
        # -> create target-type label and input
        self.targtypeLabel = ttk.Label(self.AEF, text='Target Type:')
        self.targtypeLabel.place(anchor='center', relx=0.235, rely=0.28)
        # --> textvar for targtypeEntry
        self.vartargtype = StringVar()
        self.targtypeEntry = ttk.Entry(self.AEF, width=25, textvariable=self.vartargtype)
        self.targtypeEntry.place(anchor='center', rely=0.28, relx=0.57)
        
        # -> create username label and input
        self.usernameLabel = ttk.Label(self.AEF, text='Username:')
        self.usernameLabel.place(anchor='center', relx=0.235, rely=0.4)
        # --> textvar for usernameEntry
        self.varuser = StringVar()
        self.usernameEntry = ttk.Entry(self.AEF, width=25, textvariable=self.varuser)
        self.usernameEntry.place(anchor='center', rely=0.4, relx=0.57)
        
        # -> create password label and input
        self.passLabel = ttk.Label(self.AEF, text='Password:')
        self.passLabel.place(anchor='center', relx=0.235, rely=0.52)
        # --> textvar for passEntry
        self.varpass = StringVar()
        self.passEntry = ttk.Entry(self.AEF, width=25, show="-", textvariable=self.varpass)
        self.passEntry.place(anchor='center', rely=0.52, relx=0.57)
        
        # -> create Add button
        self.addbutton = ttk.Button(self.AEF, text='[ Add ]', default=ACTIVE, command=self.add)
        self.addbutton.place(anchor='center', relx=0.5, rely=0.76)
        
        # -> create status label
        self.status = StringVar()
        self.statusbar = ttk.Label(self.AEF, textvariable=self.status)
        self.statusbar.place(anchor='center', relx=0.5, rely=0.88)
        
        # -> bind pass entry with enter
        self.passEntry.bind('<Return>', self.add)
    
    def fetchstatusReset(self):
        self.fetchstatusvar.set('')
    
    def add(self, event = None):
        # create thread for add
        threading.Thread(target=self.arch.add, args=(self.targetEntry.get().strip(), self.targtypeEntry.get().strip(), self.usernameEntry.get().strip(), self.passEntry.get().strip().encode('ascii'))).start()
        
        # clean entries
        self.varpass.set('')
        self.vartarget.set('')
        self.vartargtype.set('')
        self.varuser.set('')
        
        # set status bar
        self.status.set('Added.')
        
        # reinit the _makeFetch_ to refresh newly added Entries
        for widget in self.gettab.winfo_children():
            widget.destroy()
        
        self._makeFetch_()
        
        # after 3 sec clear status bar
        self.statusbar.after(3000, self.clearstatus)
    
    def clearstatus(self):
        self.status.set('')
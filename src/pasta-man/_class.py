#
# This is the pmanager class file
#

# import project specific modules
from targets import targets

# import libs
from tkinter import *
from tkinter import ttk
import threading

class pmanager:
    def __init__(self, master:Tk, masterpassword: bytes):
        self.parent = master
        self.parent.title('Pasta-Man')
        self.parent.geometry('530x300+400+280')
        self.arch = targets(masterpassword)
        
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
        self.addtab = ttk.Frame(self.notebook)
        self.gettab = ttk.Frame(self.notebook)
        
        # -> add the tabs under notebook
        self.notebook.add(self.addtab, text='Add')
        self.notebook.add(self.gettab, text='Fetch')
        
        # -> invoke _makeAdd_ to create Add Screen
        self._makeAdd_()
        
        # -> invoke _makeFetch_ to create Fetch Screen
        self._makeFetch_()
    
    def _makeFetch_(self):
        # -> create eclosing frame under Fetch
        self.FEF = ttk.Frame(self.gettab)
        self.FEF.pack(fill=BOTH, expand=True)
        
        # -> find targets and fetch it later
        t1 = threading.Thread(target=self.arch.targets)
        t1.start()
        
        # -> create search Entry and label
        self.searchLabel = ttk.Label(self.FEF, text='Search:', font=('Verdana', 14))
        self.searchLabel.place(anchor='center', relx=0.12,rely=0.16 )
        
        # ---> Entry
        self.varsearch = StringVar()
        self.searchEntry = ttk.Entry(self.FEF, textvariable=self.varsearch, width=24)
        self.searchEntry.place(anchor='center', relx=0.295, rely=0.3)
        
        # -> create search button
        self.searchbutton = ttk.Button(self.FEF, text='[ Search ]', default=ACTIVE, command=self.search)
        self.searchbutton.place(anchor='center', relx=0.5, rely=0.65)
        
        # -> create target type label
        self.tarLabel = ttk.Label(self.FEF, text='Target Type:', font=('Verdana', 14))
        self.tarLabel.place(anchor='center', relx=0.67,rely=0.16)
        
        # -> create dropdown menu.
        # ----> create a var for option
        self.varoption = StringVar()
        t1.join()
        self.targtypelist = ttk.OptionMenu(self.FEF, self.varoption, *self.arch.__target_types__)
        self.targtypelist.place(anchor='center', relx=0.75, rely=0.3, relwidth=0.35)
    
    def search(self):
        pass
        
        
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
        self.passEntry = ttk.Entry(self.AEF, width=25, show="!", textvariable=self.varpass)
        self.passEntry.place(anchor='center', rely=0.52, relx=0.57)
        
        # -> create Add button
        self.addbutton = ttk.Button(self.AEF, text='[ Add ]', default=ACTIVE, command=self.add)
        self.addbutton.place(anchor='center', relx=0.5, rely=0.76)
        
        # -> create status label
        self.status = StringVar()
        self.statusbar = ttk.Label(self.AEF, textvariable=self.status)
        self.statusbar.place(anchor='center', relx=0.5, rely=0.88)

        # -> set focus to targetEntry
        self.targetEntry.focus()
        
        # -> bind pass entry with enter
        self.passEntry.bind('<Return>', self.add)
    
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
import tkinter, ARINC429
from tkinter import ttk, messagebox

def bin2logical():
    A429Frame=ARINC429.Frame()
    Check = A429Frame.Decode(TxtArincFrame.get())
    if Check.Code != 0:
        messagebox.showerror(title=Check.title,message=Check.message)
    else: 
        messagebox.showinfo(message=A429Frame.GetLogicalData())

home = tkinter.Tk()
home.title("ARINC 429 Translator")

LblArincFrame=ttk.Label(master=home,text="Arinc frame",justify="center")
LblArincFrame.grid(row=0,column=0,columnspan=2)
TxtArincFrame=ttk.Entry(master=home,width=32)
TxtArincFrame.grid(row=1,column=0,columnspan=2)

CmdBin2Logical=ttk.Button(master=home,text="Translate to logical",
                          command=bin2logical)
CmdBin2Logical.grid(row=2,column=0)
home.mainloop()
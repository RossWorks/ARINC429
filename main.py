import tkinter, ARINC429
from tkinter import ttk, messagebox

def bin2logical():
    A429Frame=ARINC429.Frame()
    Check = A429Frame.Decode(TxtArincFrame.get())
    if Check.Code != 0:
        messagebox.showerror(title=Check.title,message=Check.message)
        return 
    LogicalText=A429Frame.GetLogicalData()
    TxtLabel.delete(0,'end')
    TxtLabel.insert(0,LogicalText["LABEL"])
    TxtSSM.delete(0,'end')
    TxtSSM.insert(0,LogicalText["SSM"])
    TxtSDI.delete(0,'end')
    TxtSDI.insert(0,LogicalText["SDI"])
    TxtPayload.delete(0,'end')
    TxtPayload.insert(0,LogicalText["PAYLOAD"])
home = tkinter.Tk()
home.title("ARINC 429 Translator")

LblArincFrame=ttk.Label(master=home,text="Arinc 429 frame",justify="center")
LblArincFrame.grid(row=0,column=0,columnspan=2)
TxtArincFrame=ttk.Entry(master=home,width=32)
TxtArincFrame.grid(row=1,column=0,columnspan=2)

CmdBin2Logical=ttk.Button(master=home,text="Translate to logical",
                          command=bin2logical)
CmdBin2Logical.grid(row=2,column=0)

LblLabel=ttk.Label(master=home,text="Label\t=> ")
LblLabel.grid(row=3,column=0,sticky='w')
TxtLabel=ttk.Entry(master=home,justify='center')
TxtLabel.grid(row=3,column=1)

LblSSM=ttk.Label(master=home,text="SSM\t=> ")
LblSSM.grid(row=4,column=0,sticky='w')
TxtSSM=ttk.Entry(master=home,justify='center')
TxtSSM.grid(row=4,column=1)

LblSDI=ttk.Label(master=home,text="SDI\t=> ")
LblSDI.grid(row=5,column=0,sticky='w')
TxtSDI=ttk.Entry(master=home,justify='center')
TxtSDI.grid(row=5,column=1)

LblPayload=ttk.Label(master=home,text="Payload\t=> ")
LblPayload.grid(row=6,column=0,sticky='w')
TxtPayload=ttk.Entry(master=home,justify='center')
TxtPayload.grid(row=6,column=1)
home.mainloop()
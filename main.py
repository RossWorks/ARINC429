import tkinter, ARINC429
from tkinter import ttk, messagebox, filedialog

IcdTable = ARINC429.ICD()

def bin2logical():
    A429Frame=ARINC429.Frame()
    Check = A429Frame.Decode(Frame   = TxtArincFrame.get(),
                             ICD     = IcdTable,
                             Channel = CmbChannel.get())
    if Check.Code != 0:
        messagebox.showerror(title   = Check.title,
                             message = Check.message)
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

def LoadICD():
    FileName = filedialog.askopenfilename()
    ErrorCode = IcdTable.Load(FileDir=FileName)
    if ErrorCode.Code != 0:
        messagebox.showerror(title=ErrorCode.title,
                             message= ErrorCode.message)
        return
    CmbChannel.config(values=IcdTable.GetChannelList())

home = tkinter.Tk()
home.title("ARINC 429 Translator")

LblArincFrame=ttk.Label(master=home,text="Arinc 429 frame",justify="center")
LblArincFrame.grid(row=0,column=0,columnspan=2)
TxtArincFrame=ttk.Entry(master=home,width=32)
TxtArincFrame.grid(row=1,column=0,columnspan=2)

CmdBin2Logical=ttk.Button(master=home,text="Translate to logical",
                          command=bin2logical)
CmdBin2Logical.grid(row=2,column=0)
CmdLoadICD=ttk.Button(master=home,text="Load ICD",command=LoadICD)
CmdLoadICD.grid(row=2,column=1)

LblChannel=ttk.Label(master=home,text="Channel\t=> ")
LblChannel.grid(row=3,column=0,sticky='w')
CmbChannel=ttk.Combobox(master=home,justify='center',
                        values=("no channels avaiable",),
                        state='readonly')
CmbChannel.grid(row=3,column=1)

LblLabel=ttk.Label(master=home,text="Label\t=> ")
LblLabel.grid(row=4,column=0,sticky='w')
TxtLabel=ttk.Entry(master=home,justify='center')
TxtLabel.grid(row=4,column=1)

LblSSM=ttk.Label(master=home,text="SSM\t=> ")
LblSSM.grid(row=5,column=0,sticky='w')
TxtSSM=ttk.Entry(master=home,justify='center')
TxtSSM.grid(row=5,column=1)

LblSDI=ttk.Label(master=home,text="SDI\t=> ")
LblSDI.grid(row=6,column=0,sticky='w')
TxtSDI=ttk.Entry(master=home,justify='center')
TxtSDI.grid(row=6,column=1)

LblPayload=ttk.Label(master=home,text="Payload\t=> ")
LblPayload.grid(row=7,column=0,sticky='w')
TxtPayload=ttk.Entry(master=home,justify='center')
TxtPayload.grid(row=7,column=1)
home.mainloop()
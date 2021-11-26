from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from main import signEval, apkSignFile, addCertificate
from authority import Authority
from entity import Entity
from functions import does_containt, entities_authorities_name_list


root = Tk()
root.title('Signature')
root.iconbitmap('favicon.ico')
root.geometry('800x400')
tabControl = ttk.Notebook(root)

sign_tab = Frame(tabControl)
check_tab = Frame(tabControl)
add_tab = Frame(tabControl)
certificate_tab = Frame(tabControl)

tabControl.add(sign_tab, text='Sign file')
tabControl.add(check_tab, text='Check sign')
tabControl.add(add_tab, text='Add Entity/Authority')
tabControl.add(certificate_tab, text="Add certificate")
tabControl.pack(expand=1, fill="both")


#################### sign tab #########################
#TODO refresh dropdown menu
authList = entities_authorities_name_list(True)
entList = entities_authorities_name_list(False)


def choseInputSign():
    filename = filedialog.askopenfilename\
        (initialdir="C:", title="Select a file", filetypes=[('pdf files', '*.pdf'), ('txt files', '*.txt')])
    signInputFile.config(text=filename)


def signDocument():
    file_path = signInputFile.cget()
    ent = chosenEnt
    apkSignFile(file_path, ent)
    messagebox.showinfo("File succesfully signed")


signInputFile = Label(sign_tab, text="Path to file", width=40, height=2, borderwidth=1, relief="sunken")
signInputButton = Button(sign_tab, text="Chose file", command=choseInputSign, width=15, height=2)

entLabel = Label(sign_tab, text="Chose Entity:", width=40, height=2, borderwidth=1, relief="sunken")
chosenEnt = StringVar()
chosenEnt.set(entList[0])
dropMenuEnt = OptionMenu(sign_tab, chosenEnt, *entList)

signButton = Button(sign_tab, text="Sign Chosen File", command=signDocument)

signInputFile.grid(row=0, column=0)
signInputButton.grid(row=0, column=1)
entLabel.grid(row=2, column=0)
dropMenuEnt.grid(row=2, column=1)
signButton.grid(row=3, column=0, pady=30)


################### certificate tab ####################


def create_certificate():
    addCertificate("Entity1", "eeeee")
    messagebox.showinfo("Success certificate creation")

authLabel = Label(certificate_tab, text="Chose Authority:")
chosenAut = StringVar()
chosenAut.set(authList[0])
dropMenuAut = OptionMenu(certificate_tab, chosenAut, *authList)

entLabel = Label(certificate_tab, text="Chose Entity:")
chosenEnt = StringVar()
chosenEnt.set(entList[0])
dropMenuEnt = OptionMenu(certificate_tab, chosenEnt, *entList)

signButton = Button(certificate_tab, text="Create Certificate", command=create_certificate)


entLabel.grid(row=4, column=0)
dropMenuEnt.grid(row=4, column=1)
authLabel.grid(row=5, column=0)
dropMenuAut.grid(row=5, column=1, )
signButton.grid(row=10, column=1, pady=30)


#################### check tab #########################


checkFile = Label(check_tab, text="Path to file", width=50, height=2, borderwidth=1, relief="sunken")


def choseInputCheck():
    checkFileName = filedialog.askopenfilename\
        (initialdir="C:", title="Select a file", filetypes=[('pdf files', '*.pdf'),('txt files','*.txt')])
    checkFile.config(text=checkFileName)
    checkButton["state"]= NORMAL


def choseSignCheck():
    signEval()
    if (signEval() != None):
        #if(signEval().sign["Authority"]==None):
        #checkAnswer = Label(check_tab,text="Dokument je: \nPodepsán entitou: " + signEval().sign["Entity"] + "\nPodpis: "
                                    #+ signEval().sign["EntitySign"] + "\nDokument není certifikován žádnou autoritou ",relief="sunken")
        #elif(signEval().sign["Authority"]!=None):
        checkAnswer = Label(check_tab,text= "Dokument je: \nPodepsán entitou: "+str(signEval().sign["Entity"])+"\nPodpis: "
                                                +str(signEval().sign["EntitySign"])+ "\nCertifikován autoritou: "
                                                +str(signEval().sign["Authority"])+"\nCertifikát: "+str(signEval().sign["Certificate"]),relief="sunken")
    elif(signEval()== None):
        checkAnswer = Label(check_tab, text= "Dokument není podepsán!",relief="sunken")
    checkAnswer.grid(row=2, column=0)


checkInputButton = Button(check_tab, text="Chose file", command=choseInputCheck, width=20, height=2)

checkButton = Button(check_tab, text="Check sign", command= choseSignCheck,state= DISABLED, width=20, height=2)


checkFile.grid(row=0, column=0)
checkInputButton.grid(row=0, column=1)
checkButton.grid(row=1, column=1)


####################entity tab #########################


radioValue = IntVar()
userInput = Entry(add_tab)

authorityRadio = Radiobutton(add_tab, text="Authority", variable=radioValue, value=1)
entityRadio = Radiobutton(add_tab, text="Entity", variable=radioValue, value=2)

def creation():
    userInput.update()
    if (not userInput.get()):
        messagebox.showerror("Error", "Vyplňte název")
    else:
        file = open("keypairs.json", "r")
        if(radioValue.get()==1):
            print("jsemtu")
            if (userInput.get()):
                if(does_containt(userInput.get(), file)):
                    messagebox.showinfo("Error!", "Authority/Entity already exists")
                    return
                authority = Authority(str(userInput.get())) 
                messagebox.showinfo("Success", "Succesfull creation of authority: " + userInput.get())
        elif(radioValue.get()==2):
            if (userInput.get()):
                if(does_containt(userInput.get(), file)):
                    messagebox.showinfo("Error!", "Authority/Entity already exists")
                    return
                entity = Entity(str(userInput.get()))
                messagebox.showinfo("Success", "Succesfull creation of entity: " + userInput.get())
        file.close()

textEnt = Label(add_tab, text="Zadejte název entity/ autority:")
addButton = Button(add_tab, text="Vytvořit",command = creation)

textEnt.grid(row=1, column=0)
addButton.grid(row=3, column=0)
userInput.grid(row=1, column=1)
authorityRadio.grid(row=0, column=0)
entityRadio.grid(row=0, column=1)


root.tk.mainloop()


"""
def autClick():
    authority = ""
    eAut.update()
    if (not name.get()):
        messagebox.showerror("Error", "Vyplňte název")
    elif (eAut.get()):
        authority = Authority(str(eAut.get()))
        messagebox.showinfo("Success authority creation", "Vytvořili jste entitu: " + eAut.get())
"""





"""
root = Tk()
root.title('Certificate apk')
eAut= Entry(root)

#def signClick():
#    signText= Label(root,text="Vytvořili jste autoritu:"+ e.get())
#    signText.grid(row=2,column=0)

eSign= Entry(root)
def open():
    root.filename = filedialog.askopenfilename(initialdir="C:", title="Select a file", filetypes=[('pdf files', '*.pdf'),('txt files','*.txt')])
    eSign.insert(0,root.filename)

def autClick():
    authority= ""
    eAut.update()
    if(not eAut.get()):
        messagebox.showerror("Error","Vyplňte název")
    elif(eAut.get()):
        authority= Authority(str(eAut.get()))
        messagebox.showinfo("Success authority creation","Vytvořili jste autoritu: "+ eAut.get())
        buttonSign["state"]= NORMAL


def signClick():
    eSign.update()
    if(not eSign.get()):
        messagebox.showerror("Error","Vyplňte umístění")
    elif(eSign.get()):
        if (Entity(eSign.get()).certificate== None):
            #entity = Entity(str(eSign.get()))
            if entityCall()== True:
                messagebox.showinfo("Success signing", "Podepsali jste dokument\n Vydaný certifikát")


textAut= Label(root,text="Zadejte název autority:")
textSep= Label(root,text= "                ")
textEnt= Label(root,text="Podpis dokumentu:")
buttonFile= Button(root,text="Open File", command= open)
buttonAut= Button(root,text="Vytvořit autoritu", command=autClick)
buttonSign= Button(root, text="Vytvořit podpis",state= DISABLED, command= signClick)



textAut.grid(row=0,column=0)
textSep.grid(row=0,column=1)
textEnt.grid(row=0,column=2)
buttonAut.grid(row=2,column=0)
eAut.grid(row=1,column=0)
eSign.grid(row=1,column=2)
buttonSign.grid(row=2,column=2)
buttonFile.grid(row=1,column=3)


root.mainloop()

"""


"""
Vstupy uživatele:
Autorita:
    název

Soubor:
    lokalita
"""


"""
import PySimpleGUI as sg

authority_half= [
    [
        sg.Button("Vytvořit autoritu"),
    ]
]

sign_half= [

    [sg.Text("Podpis dokumentu:")],
    [sg.Text("Vyberte dokument PDF:"),
    sg.In(size=(25,1), enable_events= True,key= "-FOLDER-"),
    sg.FolderBrowse()],

]
layout = [
    [
        sg.Column(authority_half),
        sg.VSeparator(),
        sg.Column(sign_half),
    ]
]
window = sg.Window("Certificate apk",layout, size=(600,400))

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event== "-FOLDER-":
        folder = values["-FOLDER-"]
    if folder.lower().endswith((".pdf")):
        try:

        except:

window.close() """

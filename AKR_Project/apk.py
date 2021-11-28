from tkinter import *
from tkinter import filedialog
import tkinter as tk
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

authList = entities_authorities_name_list(True)
entList = entities_authorities_name_list(False)


def resreshValues():
    dropMenuEnt['menu'].delete(0, 'end')
    new_menu = entities_authorities_name_list(False)
    for choice in new_menu:
        dropMenuEnt['menu'].add_command(label=choice, command=tk._setit(chosenEnt, choice))

    dropMenuEntSign['menu'].delete(0, 'end')
    new_menu = entities_authorities_name_list(False)
    for choice in new_menu:
        dropMenuEntSign['menu'].add_command(label=choice, command=tk._setit(chosenEntSign, choice))

    dropMenuAut['menu'].delete(0, 'end')
    new_menu = entities_authorities_name_list(True)
    for choice in new_menu:
        dropMenuAut['menu'].add_command(label=choice, command=tk._setit(chosenAut, choice))


def choseInputSign():
    path, filename = filedialog.askopenfilename\
        (title="Select a file", filetypes=[('pdf files', '*.pdf'), ('txt files', '*.txt')]).rsplit("/", 1)
    signInputFile.config(text=filename)


def signDocument():
    file_name = str(signInputFile.cget("text"))

    ent = chosenEntSign.get()
    apkSignFile(file_name, ent)
    messagebox.showinfo("Signature", "File succesfully signed")


signInputFile = Label(sign_tab, text="Path to file", width=40, height=2, borderwidth=1, relief="sunken")
signInputButton = Button(sign_tab, text="Chose file", command=choseInputSign, width=15, height=2)

entLabelSign = Label(sign_tab, text="Chose Entity:", width=40, height=2, borderwidth=1, relief="sunken")
chosenEntSign = StringVar()
chosenEntSign.set(entList[0])
dropMenuEntSign = OptionMenu(sign_tab, chosenEntSign, *entList)

signButton = Button(sign_tab, text="Sign Chosen File", command=signDocument)

signInputFile.grid(row=0, column=0)
signInputButton.grid(row=0, column=1)
entLabelSign.grid(row=2, column=0)
dropMenuEntSign.grid(row=2, column=1)
signButton.grid(row=3, column=0, pady=30)


################### certificate tab ####################


def create_certificate():
    addCertificate(chosenEnt.get(), chosenAut.get())
    messagebox.showinfo("Create Certificate", "Success certificate creation")


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

        if radioValue.get()==1:
            print("jsemtu")

            if userInput.get():

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
        resreshValues()


textEnt = Label(add_tab, text="Zadejte název entity/ autority:")
addButton = Button(add_tab, text="Vytvořit", command=creation)

textEnt.grid(row=1, column=0)
addButton.grid(row=3, column=0)
userInput.grid(row=1, column=1)
authorityRadio.grid(row=0, column=0)
entityRadio.grid(row=0, column=1)


root.tk.mainloop()

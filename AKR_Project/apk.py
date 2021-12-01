from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import main
from main import apkSignFile, addCertificate
from functions import does_containt, entities_authorities_name_list, getPDFFileSignature, getPDFFileCertificate, VerifySignature


root = Tk()
root.title('Signature')
#root.iconbitmap('favicon.ico')
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


def refreshValues(): #method for updating all dropDown menus
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

    dropMenuEntCheck['menu'].delete(0, 'end')
    new_menu = entities_authorities_name_list(False)
    for choice in new_menu:
        dropMenuEntCheck['menu'].add_command(label=choice, command=tk._setit(chosenEntCheck, choice))


def choseInputSign(): #method for chosing files from system
    path, filename = filedialog.askopenfilename\
        (title="Select a file", filetypes=[('pdf files', '*.pdf')]).rsplit("/", 1)
    signInputFile.config(text=filename)


def signDocument(): #method connecting UI and method signing files
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


def create_certificate(): #method for creating certificates
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


def choseInputCheck():  #function opening new window which allows us to select txt/pdf files
    path, filename = filedialog.askopenfilename \
        (title="Select a file", filetypes=[('pdf files', '*.pdf')]).rsplit("/", 1)
    checkFile.config(text=filename)


def signCheck():    #function for checking signature and certificate
    file_name = str(checkFile.cget("text"))     #path to file
    ent = main.entDic[chosenEntCheck.get()]
    if(file_name[-3:] == "pdf"):
        signatue = getPDFFileSignature(file_name)
        file_certificate = getPDFFileCertificate(file_name)
        if signatue == None:    #checking if file is signed
            messagebox.showinfo("Signature Check", "File is not signed")
        else:                   #if file is signed we verify its signature
            if VerifySignature(file_name, signatue, ent.keyPair.e, ent.keyPair.n):
                if file_certificate == None:    #this conditions check if certificate is present
                    messagebox.showinfo("Signature Check", "File has not been changed, but entity hasn't certificate")

                else:
                    messagebox.showinfo("Signature Check", "File has not been changed, and is signed by certificated person,...\n" + file_certificate)
            else:
                messagebox.showinfo("Signature Check", "File was not signed by this person or file has been changed")
    else:
        file_name = str(checkFile.cget("text"))
        ent = main.entDic[chosenEntCheck.get()]
        signatue = getPDFFileSignature(file_name)
        file_certificate = getPDFFileCertificate(file_name)
        if signatue == None:
            messagebox.showinfo("Signature Check", "File is not signed")
        else:
            if VerifySignature(file_name, signatue, ent.keyPair.e, ent.keyPair.n):
                if file_certificate == None:
                    messagebox.showinfo("Signature Check", "File has not been changed, but entity hasn't certificate")

                else:
                    messagebox.showinfo("Signature Check",
                                        "File has not been changed, and is signed by certificated person,...\n" + file_certificate)
            else:
                messagebox.showinfo("Signature Check", "File was not signed by this person or file has been changed")


entLabel = Label(check_tab, text="Chose Entity:")
chosenEntCheck = StringVar()
chosenEntCheck.set(entList[0])
dropMenuEntCheck = OptionMenu(check_tab, chosenEntCheck, *entList)


checkInputButton = Button(check_tab, text="Chose file", command=choseInputCheck, width=20, height=2)


checkButton = Button(check_tab, text="Check sign", command=signCheck, width=20, height=2)


entLabel.grid(row=1, column=0)
dropMenuEntCheck.grid(row=1, column=1)
checkFile.grid(row=0, column=0)
checkInputButton.grid(row=0, column=1)
checkButton.grid(row=2, column=0)


####################entity tab #########################


radioValue = IntVar()
userInput = Entry(add_tab)

radioValue.set(2)

authorityRadio = Radiobutton(add_tab, text="Authority", variable=radioValue, value=1)
entityRadio = Radiobutton(add_tab, text="Entity", variable=radioValue, value=2)


def creation():     #function takes value from users input and calls method which creates entity or authority
    userInput.update()
    if (not userInput.get()):
        messagebox.showerror("Error", "Vyplňte název")

    else:

        file = open("keypairs.json", "r")

        if radioValue.get()==1:     #creating authority
            print("jsemtu")

            if userInput.get():

                if(does_containt(userInput.get(), file)):
                    messagebox.showinfo("Error!", "Authority/Entity already exists")
                    return

                name = str(userInput.get())
                main.create_auth_ent(True, name)
                messagebox.showinfo("Authority", "Authority successfully added")


        elif(radioValue.get()==2):    #creating entity

            if (userInput.get()):

                if(does_containt(userInput.get(), file)):
                    messagebox.showinfo("Error!", "Authority/Entity already exists")
                    return

                name = str(userInput.get())
                main.create_auth_ent(False, name)
                messagebox.showinfo("Entity", "Entity successfully added")
        file.close()
        refreshValues()


textEnt = Label(add_tab, text="Zadejte název entity/ autority:")
addButton = Button(add_tab, text="Vytvořit", command=creation)

textEnt.grid(row=1, column=0)
addButton.grid(row=3, column=0)
userInput.grid(row=1, column=1)
authorityRadio.grid(row=0, column=0)
entityRadio.grid(row=0, column=1)


root.tk.mainloop()

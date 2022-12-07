
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import os
import tkinter as tk
import os
import requests
import asyncio
import glob
import xml.etree.ElementTree as ET
#####################################
filename_km="/datalogs/"
Processlist_km=os.listdir(filename_km)
import itertools
ab = itertools.chain(Processlist_km)
Processlist=list(ab)
Processlist=list(dict.fromkeys(Processlist))
Processlist=[s for s in Processlist if s.isdigit()]

######################################################################







top = Tk()
p1 = PhotoImage(file = 'MIZALA_Logo.png')
top.iconphoto(False, p1)
top.title("MIZALA KM")
top.geometry("1000x1000")
top.config(cursor="hand2",bg="skyblue")
def LoadFile():
   #msg = messagebox.showinfo(E_Lot_L.get())
   path_KM="/datalogs/"
   operation_input=9999
   Process=clicked.get()
   Lot_input=E_Lot_L.get()
   Tray_input=E_Tray_L.get()
   Process_Lot_Path=path_KM+str(Process)+"/prod/"+str(Lot_input)+"_"+str(operation_input)+"/SOD_UPLOAD/"
   Process_Lot_Path_ENG = path_KM + str(Process) + "/eng/" + str(Lot_input) + "_" + str(
                operation_input) + "/SOD_UPLOAD/"
   
   dirExist = os.path.isdir(Process_Lot_Path)
   if dirExist == True:
    
        list_of_files = glob.glob(Process_Lot_Path+str(Lot_input) + "_" + str(Tray_input)+'_SORTBIN_*')
        
        if len(list_of_files) != 0:
            latest_file = max(list_of_files, key=os.path.getctime).replace("\\", '/')
            
            list_of_files_DISPO = glob.glob(Process_Lot_Path + str(Lot_input) + "_" + str(Tray_input) + '_DISPO_TRAY_*')
            if len(list_of_files_DISPO) != 0:
                
                latest_file_DISPO = max(list_of_files_DISPO, key=os.path.getctime).replace("\\", '/')
                
                destination_folder=Process_Lot_Path_ENG
                btn_process['state'] = tk.NORMAL
                btn_process['bg'] = "green"
                
            else:
                destination_folder=Process_Lot_Path_ENG
                
                latest_file_DISPO="DISPO File Not Found!"
                btn_process['state'] = tk.DISABLED
                btn_process['bg'] = "beige"
            
            
        else:
            
            latest_file=""
            latest_file_DISPO="Please Validate the SORTBIN file in PROD Datalog! "
            destination_folder="Please Validate the SORTBIN file in PROD Datalog! "
            btn_process['state'] = tk.DISABLED
            btn_process['bg'] = "beige"
            
            
        
   else:
       
       latest_file="Lot Not Found"
       latest_file_DISPO="Lot Not Found"
       destination_folder="Lot Not Found"
       btn_process['state'] = tk.DISABLED
       btn_process['bg'] = "beige"
       
   
   
   
   
   lbl_SORTBIN.config(text = latest_file)
   lbl.config(text = latest_file_DISPO)
   lbl_Des.config(text = destination_folder )

def processsortbin_copy():
    path_KM="/datalogs/"
    operation_input=119325
    Process=clicked.get()
    Lot_input=E_Lot_L.get()
    Tray_input=E_Tray_L.get()

    Process_Lot_Path_ENG = path_KM + str(Process) + "/eng/" + str(Lot_input) + "_" + str(
                 operation_input) + "/SOD_UPLOAD/"

    btn_process['state'] = tk.DISABLED
    btn_process['bg'] = "beige"
    EngdirExqist=os.path.isdir(Process_Lot_Path_ENG)
    if EngdirExqist == True:
        print("ENG Folder Exist")
    else:
        os.makedirs(Process_Lot_Path_ENG)
        
    def register_all_namespaces(filename):
        namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
        for ns in namespaces:
            ET.register_namespace(ns, namespaces[ns])
            
    xml_file = lbl_SORTBIN.cget("text")
    with open(xml_file, "r") as myfile:
        data = myfile.readlines()
        first_line = data[0]
        second_line = data[1]
        #print(data[0])
    
    tree = ET.parse(xml_file)
    paragraphs = tree.findall('.//T')
    register_all_namespaces(xml_file)
    mytree = ET.parse(xml_file)
    myroot = mytree.getroot()
    tmp = 1
    while tmp <= len(paragraphs):
    
        results = myroot[tmp].findall('DTB')
        results_93 = myroot[tmp].findall('FTB')
    
        if results:
            date = results[0].text
            # print(date)
    
        else:
            # there is no element,
            # do what you want in this case
    
            if results_93[0].text == '9399':
    
                for SLUCH in myroot[tmp].iter('T'):
                    VIDPOM = SLUCH.find('FTB')
                    new_tag = ET.Element('DTB')
                    new_tag.text = '939900'
                    new_tag.tail = VIDPOM.tail  # copy text after `tag`
    
                    index = list(SLUCH).index(VIDPOM)
                    # index = SLUCH.getchildren().index(VIDPOM)  # deprecated
                    SLUCH.insert(index + 1, new_tag)
    
                # print(ET.tostring(myroot[tmp]).decode())
    
            print("nodata")
    
        tmp = tmp + 1
        
        eng_latest_file=lbl_SORTBIN.cget("text").replace("prod", 'eng')
        mytree.write(eng_latest_file)

        with open(eng_latest_file) as modify:
            replace_text = modify.readlines()
            replace_text[0] = first_line
            replace_text[1] = second_line

        with open(eng_latest_file, "w") as f:
            f.writelines(replace_text)

        import shutil
        shutil.copyfile(lbl.cget("text"), lbl.cget("text").replace("prod", 'eng'))
        
    messageinfo="Lot :" + E_Lot_L.get() +"      Tray : "+ Tray_input +"\n"+"Please find your file at ENG folder ! \n" #+ lbl.cget("text").replace("prod", 'eng') +"\n" + eng_latest_file
    msg = messagebox.showinfo("MIZALA",messageinfo)

##################################################################################

info_mizala = Label(top, text="MIZALA - KM", bg="skyblue",font=('Helvatical bold',20))
info_mizala.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

Lot_L = Label(top, text = "Lot",bg="skyblue")
Lot_L.grid(row = 1,column = 0)
E_Lot_L = Entry(top, bd = 3,name='entry_lot', cursor='xterm')
E_Lot_L.grid(row = 1,column = 1,padx=10,pady=10)

Tray_L = Label(top, text = "Tray",bg="skyblue")
Tray_L.grid(row = 2,column = 0)
E_Tray_L = Entry(top, bd = 3,name='entry_tray', cursor='xterm')
E_Tray_L.grid(row = 2,column = 1,padx=10,pady=10)

 
Process_L = Label(top, text = "Process",bg="skyblue")
Process_L.grid(row = 1,column = 4) 
# datatype of menu text
clicked = StringVar()
# initial menu text
clicked.set( "Please Choose Process" )
# Create Dropdown menu
drop = OptionMenu( top , clicked , *sorted(Processlist) )
drop.grid(row = 1,column = 5,padx=10,pady=10)

Operation_L = Label(top, text = "Operation", bg="skyblue")
Operation_L.grid(row = 2,column = 4)

mystr_operation = StringVar()
mystr_operation.set('119325')
E_Operation_L = Entry(top, bd = 3, bg= 'yellow',name='entry_Operation', cursor='xterm',textvariable=mystr_operation,state=DISABLED)
E_Operation_L.grid(row = 2,column = 5,padx=10,pady=10)
buttonFont = font.Font(size=18)

B = Button(top, text = "Load", command = LoadFile,bg='#45b592',
    fg='#ffffff',
    bd=0,
    height=2,
    width=10,font=buttonFont)
B.grid(row = 1,column = 6,columnspan = 2, rowspan = 2)

frame = LabelFrame(
    top,
    text='Detail',
    bg='#f0f0f0',
)
frame.grid(column=0, row=3, padx=20, pady=20,columnspan=7,sticky="WE",ipadx=7, ipady=7)
#left_frame = Frame(frame, width=750, height=100, bg='lightgreen')
#left_frame.grid(row=3, column=0, columnspan=7,padx=5)
Label_Source=Label(frame, text="Source File : ",anchor="w")
Label_Source.grid(row = 0,column = 0,columnspan=7,sticky='w')
lbl = tk.Label(frame,text="DISPO_Tray File Path",anchor="c")
lbl.grid(row = 1,column = 0,columnspan=7,sticky='w',padx=50)
lbl_SORTBIN = tk.Label(frame,text="SORTBIN File Path",anchor="c")
lbl_SORTBIN.grid(row = 2,column = 0,columnspan=7,sticky='w',padx=50)

Label_Des=Label(frame, text="Destination Folder : ",anchor="w")
Label_Des.grid(row = 3,column = 0,columnspan=7,sticky='w')
lbl_Des = tk.Label(frame,text="Destination Path")
lbl_Des.grid(row = 4,column = 0,columnspan=7,sticky='w',padx=50)


btn_process = tk.Button(frame,text = "Process", state = DISABLED,command = processsortbin_copy,bg = "beige")
btn_process.grid(row = 5,column = 1,columnspan=7,sticky='ew',padx=50)




top.mainloop()








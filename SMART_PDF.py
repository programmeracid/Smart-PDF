
from os import listdir as ld
from os import remove as rem
from os import path
from PyPDF2 import PdfReader, PdfWriter
all_pages = True
def com1():
    global all_pages
    all_pages = False
def com2():
    global all_pages
    all_pages = True
    


    
entryval = ''
customer = []
xml_path = []
pdf_path = []
extra = []
xml_display = ['None']
voliss_display = ['None']
cust_selected =  False
xml_selected = False
voliss_selected = False
cus = open('customer.txt').readlines()

for line in cus :
    L=line.split('|')
    customer.append(L[0].rstrip('\n'))
    xml_path.append(L[1].rstrip('\n'))
    pdf_path.append(L[2].rstrip('\n'))
    extra.append(L[3].rstrip('\n'))

from tkinter import *
from tkinter import ttk

window=Tk()
window.geometry('500x450')
window.title('PDF Merge Tool')
note1 = ttk.Notebook(window)
note1.pack()

root = Frame(note1,width=500,height=450)
root2 = Frame(note1,width=500,height=500)
root3 = Frame(note1,width=500,height=450)

root.pack(fill='both',expand = 1)
root2.pack(fill='both',expand = 1)
root3.pack(fill='both',expand = 1)

note1.add(root,text = 'PDF Merger')
note1.add(root2,text = 'Page Count')
note1.add(root3,text = 'Split PDF')

cusclicked=StringVar()
#entry=StringVar()
volclicked=StringVar()


def sel_customer(*event) :
    global cust_selected
    
    
    
    cust_selected = True
    print('ys')
    global xml_display
    Cust = cusclicked.get()
    x = customer.index(Cust)
    path = xml_path[x]
    print('yoo')
    xml_display=[]
    for file in ld(path) :
        if file[-3:] == 'xml' :
            name = file[:file.index('_')]
            
            xml_display.append(name)
    xml_display = list(set(xml_display))
    xml_display.sort()
    Update(xml_display)
    
    
    
    

def sel_xml(*event) :
    global xml_selected
    if xml_selected :
        
        volclicked.set(' '*15)
        voliss_selected = False
        menu = Oc['menu']
        menu.delete(0,'end')
    if cust_selected : xml_selected = True
    #entry.set()
    global voliss_display
    Cust = cusclicked.get()
    x = customer.index(Cust)
    path = xml_path[x]
    print(entry.get())
    voliss_display = []
    for file in ld(path) :
        #print(file)
        #xmlname = file[:file.index('_')+1]
        if file.endswith('xml') and file.startswith(entry.get()) :
            #print(file)
            volname = file[file.index('_')+1:-4]
            voliss_display.append(volname)
    voliss_display = list(set(voliss_display))
    voliss_display.sort()
    menu = Oc['menu']
    menu.delete(0,'end')
    if 'None' in voliss_display : voliss_display.remove('None')
    for vol in voliss_display :
        menu.add_command(label = vol , command = lambda a = vol : volclicked.set(a))
    

def sel_voliss(*args) :
    print('oi')
    global voliss_selected
    if cust_selected and xml_selected : voliss_selected = True
    


def clear():
    cusclicked.set('Sage')
    entry.delete(0,'end')
    volclicked.set('               ')
    voliss_selected = cust_selected = xml_selected = False

def Scankey(event):
    global entryval
    if entryval != event.widget.get() :
        val = event.widget.get()
        print(val)
        

        if val == '':
            sel_customer()
            data = xml_display
        else:
            data = []
            for item in xml_display:
                if val in item :
                    data.append(item)
                
        
        Update(data)
        print(len(val))
        if len(val) == 3 :
            print(True)
            sel_xml()
    


def Update(data):


    listbox.delete(0, 'end')

    # put new data
    for item in data:
        listbox.insert('end', item)
    
def go(*args) :
    cs = listbox.get(ACTIVE)
    entry.delete(0,'end')
    entry.insert(0,cs)
    sel_xml()

def ask1(*args) :
    filepath = filedialog.askopenfilename()
    EN1.delete(0,'end')
    EN1.insert(0,filepath)
def ask2(*args) :
    filepath = filedialog.askopenfilename()
    EN2.delete(0,'end')
    EN2.insert(0,filepath)
def ask3(*args) :
    filepath = filedialog.askdirectory()
    EN3.delete(0,'end')
    EN3.insert(0,filepath)      


def SPLIT_PDF_RUN() :

    try :
        
        reader = PdfReader(EN2.get())


        print(len(reader.pages))

        f = open(EN1.get())
        L = [x for x in f.read().split('\n')]
        print(L)
        i = 0; start = 0
        for page_num in range(len(reader.pages)) :
            page = reader.pages[page_num]
            text = page.extract_text()
            print(text)
            print(page_num)
            fr = False
            line_count = 0
            for line in text.split('\n') :
                #print(i)
                line_count += 1
                if L[i+1] in line :
                    
                    if line_count ==1 : end = page_num - 1
                    if line_count >1 : end = page_num
                    if L[i+1][:4] != L[i][:4] : end = page_num - 1
                    
                    with open(f"{EN3.get()}\\{L[i]}.pdf","wb") as f :
                        
                        new_PDF = PdfWriter()
                        for j in range(start,end+1) :
                            new_PDF.add_page(reader.pages[j])
                        new_PDF.write(f)
                    i += 1
                    start = page_num
                    if i == len(L)-1 :
                        with open(f"{EN3.get()}\\{L[i]}.pdf","wb") as f :
                        
                            new_PDF = PdfWriter()
                            for j in range(start,len(reader.pages)) :
                                new_PDF.add_page(reader.pages[j])
                            new_PDF.write(f)
                    if i == len(L) -1 :
                        fr = True
                        break
            if fr == True : break
            lb = Label(root3,text = 'Completed',font=(16),fg='green')
            lb.place(x = 300,y=130)
    except Exception as e:
        print(e)
        lb = Label(root3,text = 'Error',font=(16),fg='red')
        lb.place(x = 300,y=130)
    

entry = Entry(root)
entry.place(x=150,y=80)
entry.bind('<KeyRelease>', Scankey)

listbox = Listbox(root)
listbox.place(x=150,y=100)
listbox.bind('<Double-1>',go)
Update(xml_display)



Label(root,text='Customer:',font=(16),fg='red').place(x=30,y=30)
Label(root,text='Journals:',font=(16),fg='red').place(x=30,y=80)
Label(root,text='Vol_Iss:',font=(16),fg='red').place(x=30,y=280)

EN1 = Entry(root3,font = ('calibri',16))
EN1.place(x=100,y=80,width = 350,height = 23)
EN2 = Entry(root3,font = ('calibri',16))
EN2.place(x=100,y=180,width = 350,height = 23)
EN3 = Entry(root3,font = ('calibri',16))
EN3.place(x=100,y=280,width = 350,height = 23)
B1 = Button(root3, text = 'Select file',font = 13,command = ask1, activebackground = 'green',activeforeground = 'white')
B1.place(x=100,y=20)
B2 = Button(root3, text = 'Select PDF file',font = 13,command = ask2, activebackground = 'green',activeforeground = 'white')
B2.place(x=100,y=120)
B3 = Button(root3, text = 'Select Output Path',font = 13,command = ask3, activebackground = 'green',activeforeground = 'white')
B3.place(x=100,y=220)
B4 = Button(root3, text = 'RUN',font = 13,command = SPLIT_PDF_RUN, activebackground = 'green',activeforeground = 'white')
B4.place(x=100,y=350)

cusclicked.set('Sage')

volclicked.set('               ')
cusclicked.trace('w',sel_customer)
ch1 = IntVar(value = 1)
ch2 = IntVar()
rad = IntVar()
volclicked.trace('w',sel_voliss)
Oa = OptionMenu(root,cusclicked,*customer)
Oa.place(x=150,y=30)

Oc = OptionMenu(root,volclicked,*voliss_display)
Oc.place(x=150,y=280)
#OptionMenu(root,clicked,L1).place(x=150,y=180)
sel_customer()
C1 = Checkbutton(root,text='First page combine',variable = ch1).place(x=340,y=30)
C2 = Checkbutton(root,text='All pages combine',variable = ch2).place(x=340,y=80)
R1 = Radiobutton(root,text = 'WEB',variable = rad,value = 0).place(x = 340,y = 200)
R2 = Radiobutton(root,text = 'PRESS',variable = rad,value = 1).place(x = 340,y = 250)



Statuslabel = Label(root,text = '')
def run(all_pages) :
     
    Statuslabel.config(text = '')    
    pdf_files = []
    if rad.get() : wp = '\\PRESS\\PDF' ; WP = 'PRESS'
    else : wp = '\\WEB\\PDF' ; WP = 'WEB'
    PDF_FINAL_PATH = pdf_path[customer.index(cusclicked.get())] + '\\' + entry.get()+'\\'+volclicked.get()+wp
    xpath = xml_path[customer.index(cusclicked.get())] + '\\'
    
    print(PDF_FINAL_PATH)
    xml = xpath + entry.get() + '_' + volclicked.get()+'.xml'
    print(xml)
    if not (path.exists(xml) and path.exists(PDF_FINAL_PATH)) :
        Statuslabel.config(text = 'Incorrect Selection',fg = 'red')
        
    else : 
        x = customer.index(cusclicked.get())
        with open(xml,encoding='UTF-8') as f :
            L=f.read().split('aid')[1::2]
            for i in L :
                pdf_name = extra[x] + i[1:-2] + '.pdf'
                pdf_files.append(pdf_name)

        

        writer = PdfWriter()
        
        Statuslabel.place(x=340,y=150)
        for file_path in pdf_files:
            print(file_path)
            Statuslabel.config(text = file_path)
            g = PDF_FINAL_PATH +'\\' + file_path
            #print(g)
            
            if file_path in ld(PDF_FINAL_PATH) :
                
                reader = PdfReader(g)
                if all_pages : n = len(reader.pages)
                else : n = 1
                writer.append(reader,(0,n))
            elif file_path.lower() in ld(PDF_FINAL_PATH) :
                
                reader = PdfReader(g[:len(g)-len(file_path)]+file_path.lower())
                if all_pages : n = len(reader.pages)
                else : n = 1
                writer.append(reader,(0,n))
            elif file_path.upper() in ld(PDF_FINAL_PATH) :
                
                reader = PdfReader(g[:len(g)-len(file_path)]+file_path.upper())
                if all_pages : n = len(reader.pages)
                else : n = 1
                writer.append(reader,(0,n))
        
        new_file_name = entry.get()+'_'+volclicked.get()
        if all_pages : new_file_name += '_ALLpage_'+WP+'.pdf'
        else : new_file_name += '_Fpage_'+WP+'.pdf'
        Statuslabel.config(text = 'writing...')
        with open(new_file_name, "wb") as output:
            writer.write(output)
        Statuslabel.config(text='Completed!',fg = 'green')
        #root.after(2000,lambda : Statuslabel.destroy())
        reader = PdfReader(new_file_name)
        if len(reader.pages) == 0 :
            Statuslabel.config(text = 'No PDFs Found',fg = 'red')
            rem(new_file_name)
    

def checkrun(*args) :
    print(ch1.get(),ch2.get())
    if ch1.get() : run(False)
    if ch2.get() : run(True)
root.bind('<Return>',checkrun)
Button(root,text='CLEAR',font=(16),command=clear,activebackground='green',activeforeground='white').place(x=50,y=330)
Button(root,text='GENERATE',font=(16),command = checkrun,activebackground='green',activeforeground='white').place(x=200,y=330)
Button(root,text='EXIT',font=(16),command=window.destroy,activebackground='green',activeforeground='white').place(x=385,y=330)    

import PyPDF2,os,csv
from tkinter import filedialog

L = Label(root2,text = 'Path : ',font = ('calibri',16))
L.place(x=30,y=75)
E = Entry(root2,font = ('calibri',16))
E.place(x=100,y=80,width = 350,height = 23)
ch3 = IntVar()





def Part_Run() :
    PDF_path = E.get()
    fake = ''
    for i in PDF_path :
        if i == '/' : fake += '\\'
        else : fake += i
    PDF_path = fake
    print(PDF_path)
    if PDF_path == '' : PDF_path = '.'
    
    f=open('report.csv','w',newline='')
    w=csv.writer(f)
    for i in os.listdir(PDF_path):
        if i[-3:]=='pdf':
            # creating a pdf file object
            if PDF_path == '.' : 
                pdfFileObj = open(i, 'rb')
            else : pdfFileObj = open(PDF_path + '\\' + i, 'rb')
          
            # creating a pdf reader object
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
          
            # printing number of pages in pdf file
            print(i, len(pdfReader.pages))
            w.writerow([i, len(pdfReader.pages)])
    f.close()
    print('done')
    
def completerun(*args) :
    PDF_path = E.get()
    fake = ''
    for i in PDF_path :
        if i == '/' : fake += '\\'
        else : fake += i
    PDF_path = fake
    print(PDF_path)
    if PDF_path == '' : PDF_path = '.'
    
    f=open('report.csv','w',newline='')
    w=csv.writer(f)
    for root,dire,files in os.walk(PDF_path):
        for i in files : 
            if i[-3:]=='pdf':
                # creating a pdf file object
                
                pdfFileObj = open(root + '\\' + i, 'rb')
              
                # creating a pdf reader object
                pdfReader = PyPDF2.PdfReader(pdfFileObj)
              
                # printing number of pages in pdf file
                print(i, len(pdfReader.pages))
                w.writerow([i, len(pdfReader.pages)])
    f.close()
    print('done')
    

def ask(*args) :
    filepath = filedialog.askdirectory()
    E.delete(0,'end')
    E.insert(0,filepath)
    

    
def Run(*args) :
    if ch3.get() : completerun()
    else : Part_Run()
    
    

    
B1 = Button(root2,text= 'Run',font = 16,command = Run,activebackground='green',activeforeground='white')
B1.place(x=100,y = 200)
B2 = Button(root2, text = 'Select path',font = 13,command = ask, activebackground = 'green',activeforeground = 'white')
B2.place(x=100,y=20)
CB1 = Checkbutton(root2,text = "Include Sub Folders",variable = ch3)
CB1.place(x=100,y = 150)

window.mainloop()
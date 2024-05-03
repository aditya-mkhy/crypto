import os
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
from time import sleep , time
from tkinter import Tk , Button , Label ,Text ,Entry ,StringVar ,PhotoImage, Frame, Canvas
from ctypes import windll
from tkinter.filedialog import  askdirectory ,askopenfilename
from threading import Thread
from colorama import init
from termcolor import colored
from threading import Thread
import socket, os, sys
from webbrowser import open as open_file
from tkinter import messagebox
from PIL import ImageTk, Image 
import subprocess
from requests import get as requests_get
from json import loads



class Crypto():
    file_key=b'KrYYijUjcf4GUQfxOhk_6fq9KkQcl48MbGvd0CZosCA='
    def __init__(self,name=None):
        self.author='Aditya'
        self.version='2.0v __24/aug/2022'
        pass

    def _fileKeyGen(self, passwd):
        p = "Hfn4"+str(passwd)[::3]+"$^hhd324hrGnfh&"
        return self.key_gen(p)
        
        
    def ext(self,filename=None,ext=None):
        if not os.path.exists(filename):
            raise ValueError("This file doesn't exists")
        if ext == None:
            raise ValueError("Please Enter Extension")
        
        if os.path.isdir(filename):
            all_file_list=self.all_file_in_folder(filename)
            n=0
            for files in all_file_list:
                name , ext_ =os.path.splitext(files)
                n+=1
                os.rename(files,(name+'.'+ext))
                        
        else:
            name , ext_ =os.path.splitext(filename)
            os.rename(filename,(name+'.'+ext))
        return True
        
        
    def key_gen(self,passwd):
        password = passwd.encode() 
        salt = b'hackerknenon83jknc/8493834' 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key =urlsafe_b64encode(kdf.derive(password))
        return key
        
    def all_file_in_folder(self,folder_name):
        all_file_list=[]        
        def folder_dec(folder_name):
            if os.path.exists(folder_name):
                try:
                    folder_content=os.listdir(folder_name)
                    for file in folder_content:
                        file=folder_name+'/'+file
                        if os.path.isfile(file):
                            nonlocal all_file_list
                            all_file_list.append(file)
                        elif os.path.isdir(file):
                            folder_dec(file)
                        else:
                            pass
                except:
                    pass
            else:
                pass
        folder_dec(folder_name)
        return all_file_list
    
                
        
    def encrypt(self,filename=None,passwd=None,ext=None,chunk=None,rename=False):
        def encrypt__data(data,key):
            f = Fernet(key)
            encrypted = f.encrypt(data)
            return encrypted
        def encode(filename,key,rename,ext,chunk):
            file_size=os.stat(filename).st_size
            dir_name=os.path.dirname(filename)
            base_name=os.path.basename(filename)
            tem_file=dir_name+'/'+base_name+'temp_crypto.crypt'
            try:
                f=open(filename,'rb')
            except Exception as e:
                raise e
            f2=open(tem_file,'wb')
            data=f.read(chunk)
            while data:                
                data=encrypt__data(data,key)
                f2.write(data)
                f2.write(b'\r\n')
                data=f.read(chunk)
            f.close()
            f2.close()
            org_filename=filename

            if rename ==True:
                if ext==None:
                    ext='crypt'


                name ,ex =os.path.splitext(base_name)
                a=''
                if ex=='.mkv':
                    a='@'
                elif ex=='.webm':
                    a='a'
                elif ex=='.mp3':
                    a='w'
                elif ex=='.mp4':
                    a='s'
                elif ex==".jpg":
                    a='h'
                elif ex==".png":
                    a='n'
                elif ex==".txt":
                    a='b'
                elif ex==".py":
                    a='d'
                elif ex==".pdf":
                    a='t'
                elif ex==".zip":
                    a='u'
                else:
                    pass
                
                
                if a !='':
                    rn_name=(encrypt__data((name+'_'+a).encode(),self._fileKeyGen(key)).decode())+'.'+ext
                else:
                    rn_name=(encrypt__data(name.encode(),self._fileKeyGen(key)).decode())+ex

                filename=dir_name+'/'+rn_name
                ext=None
                
            try:
                os.remove(org_filename)
                os.rename(tem_file,filename)
                print(colored(' Done___{ '+org_filename+' }\n', 'cyan'))
                
                if ext !=None:
                    self.ext(filename=filename,ext=ext)
            except Exception as e:
                print(colored(' Error_{'+str(e)+'}', 'red'))


            

        #main______________checking
        st_time=time()
        if filename == None:
            raise ValueError('Please enter File Name')
        
        if passwd==None:
            raise ValueError('Please enter PASSWORD')
        if not os.path.exists(filename):
            raise ValueError("This file doesn't exist")
        #run_____________
        if chunk==None:
            chunk=1024*128
        else:
            chunk=1024*chunk
            
        key=self.key_gen(passwd)        
        if os.path.isdir(filename):
            all_file_list=self.all_file_in_folder(filename)
            for files in all_file_list:
                try:
                    encode(files,key,rename,ext,chunk)
                except Exception as e:
                    print(colored(' Error_{'+str(e)+'}', 'red'))
        else:
            try:
                encode(filename,key,rename,ext,chunk)
            except Exception as e:
                print(colored(' Error_{'+str(e)+'}', 'red'))
        end_time=time()
        return (True,end_time-st_time)


    #______________________next__________________________________________                

    def decrypt(self,filename=None,passwd=None,ext=None):
        def decrypt_data(data,key):
            f = Fernet(key)
            decrypted = f.decrypt(data)
            return decrypted
        
        def decode(filename,key,ext):
            dir_name=os.path.dirname(filename)
            base_name=os.path.basename(filename)
            tem_file=dir_name+'/'+base_name+'temp_crypto.crypt'
            f=open(filename,'rb')
            f2=open(tem_file,'wb')
            data=f.readline()
            error_status=False
            while data:
                try:
                    data=decrypt_data(data,key)
                except:
                    f.close()
                    f2.close()
                    os.remove(tem_file)
                    error_status=True
                    break
                    
                f2.write(data)
                data=f.readline()
            if error_status==True:
                raise ValueError('Password is __Incorrect__')
                
            else:
                f.close()
                f2.close()
        
                org_filename=filename
                name ,ex =os.path.splitext(base_name)
                try:
                    ex__=ex
                    rn_name=(decrypt_data((name).encode(),self._fileKeyGen(key)).decode())
                    
                    l=len(rn_name)
                    ex=rn_name[l-1]
                    a=''
                    if ex=='@':
                        a='.mkv'
                    elif ex=='a':
                        a='.webm'
                    elif ex=='w':
                        a='.mp3'
                    elif ex=='s':
                        a='.mp4'
                    elif ex=="h":
                        a='.jpg'
                    elif ex=="n":
                        a='.png'
                    elif ex=="b":
                        a='.txt'
                    elif ex=="d":
                        a='.py'
                    elif ex=="t":
                        a='.pdf'
                    elif ex=="u":
                        a='.zip'
                    else:
                        pass
                    
                    if a !='':
                        rn_name=rn_name[:l-2]+a
                    else:
                        rn_name=rn_name+ex__
                    ext=None
                except:
                    if ext !=None:
                        rn_name=name+'.'+ext
                    else:
                        rn_name=base_name
                                        
                try:
                    os.remove(org_filename)
                    os.rename(tem_file,dir_name+'/'+rn_name)
                    print(colored(' Done__{ '+dir_name+'/'+rn_name+'\n', 'yellow'))
                    
                except Exception as e:
                    print(colored('Error_{'+str(e)+'}', 'red'))


            

        #main______________checking
        error_status=True
        st_time=time()
        if filename == None:
            raise ValueError('Please enter File Name')
        
        if passwd==None:
            raise ValueError('Please enter PASSWORD')
        if not os.path.exists(filename):
            raise ValueError("This file doesn't exist")
        #run_____________
    
        key=self.key_gen(passwd)        
        if os.path.isdir(filename):
            all_file_list=self.all_file_in_folder(filename)
            for files in all_file_list:
                try:
                    decode(files,key,ext)
                except Exception as e:
                    print(colored(' Error_{'+str(e)+'}', 'red'))
                    error_status=e
        else:
            try:
                decode(filename,key,ext)
            except Exception as e:
                print(colored(' Error_{'+str(e)+'}', 'red'))
                error_status=e
        end_time=time()
        
        return (error_status,end_time-st_time)

class Crypto_App():
    def __init__(self):
        self.author='Aditya'
        self.version='1.0v __11/jan/2021'
        global crypto
        crypto=Crypto()
        self.root=Tk()
        self.tymes=1    
        self.val=0    
        self.passwd=""
        self.passwdv="5181"
        self.but1value='Encode'
        self.but2value="Decode"
        self.stop='f'

        windll.shcore.SetProcessDpiAwareness(1)      
        self.root.title('En/De%crypter...')
        self.root.geometry('1210x250')
        self.root.resizable(False,False)
        self.passwd=StringVar()
        self.filepath=StringVar()
        self.exvalue=StringVar()

        self.photo = PhotoImage(file =resource_path("data/lock1.png"), master=self.root)
        self.root.iconphoto(False, self.photo)
        self.photo1 = PhotoImage(file = resource_path("data/lockbg.png"), master=self.root)        
        self.img=Label(self.root,text='',image=self.photo1)
        self.img.pack(expand=True,fill='both')
        self.filent=Entry(self.img,textvariable=self.filepath,bg="mint cream",fg="navy",
                          width=60,font=('',24)
                     ,highlightthickness=2,highlightbackground = "dark orange",
                          highlightcolor= "lawn green")
        self.filepath.set(" Enter file path")
        self.filent.pack(pady=20,padx=0)
        self.pasent=Entry(self.img,textvariable=self.passwd,bg="floral white",fg="dark violet",width=60,
                          font=('',24)
                     ,highlightthickness=2,highlightbackground = "maroon1",
                          highlightcolor= "dark green")
        self.passwd.set(" Enter Password")
        self.pasent.pack(pady=20,padx=0)
        self.but1=Button(self.img,height=1,width=8,text=self.but1value,
                         bg="wheat",fg='blue',font=('',19)
                    ,bd=0,command=self.encode_file).pack(padx=60,side='left')
        self.but2=Button(self.img,text=self.but2value,width=8,bg="wheat1",fg='green',font=('',19),
                    bd=0,command=self.decode_file).pack(padx=60,side='left')
        self.but3=Button(self.img,text="clear",width=8,bg="plum1",fg='orange',font=('',19)
                    ,bd=0,command=self.clear)
        self.but3.pack(padx=48,side='left')
        
        self.l=Label(self.img,text='Enter File Extension-',bg="lightcyan2",fg="black",font=('',19)).pack(padx=25,side='left')
        self.exent=Entry(self.img,textvariable=self.exvalue,width=8,bg="white",fg="green",font=('',19)
                    ,highlightthickness=4,highlightbackground = "cyan2", highlightcolor= "red")
        self.exent.pack(padx=15,side='left')
        
        #_______bind___________
        self.root.bind('<Control-o>',self.ask_file )
        self.root.bind('<Control-f>',self.ask_dir_file )
        self.root.bind('<Control-c>',self.clear)
        self.filent.bind("<FocusIn>", self.focus_in_filent)
        self.pasent.bind("<FocusIn>", self.focus_in_pasent)

        self.root.mainloop()            

        
    def focus_in_filent(self,event=None):
        file=self.filepath.get()
        try:
            if file[0]==' ':
                self.filepath.set('')
        except:
            pass
            
         
    def focus_in_pasent(self,event=None):
        password=self.passwd.get()
        try:
            if password[0]==" ":
                self.passwd.set('')
        except:
            pass
            
        
        
    def encode_file(self):
        thr=Thread(target=self.encode_file_thread)
        thr.start()

    def encode_file_thread(self):
        file=self.filepath.get()
        if os.path.exists(file):
            password=self.passwd.get()
            if password != "":
                if "Enter Password"  not in password:
                    ext=self.exvalue.get()
                    if ext == '':
                        ext=None
                    try:
                        self.filepath.set(" Encrypting , Please wait")
                        t=crypto.encrypt(filename=file,passwd=password,ext=ext,rename=False,chunk=None)
                        t=(str(t[1])).split('.')
                        self.filepath.set(" Encrypted ,please remember password  In__{"+((str(t[0])+'.'+((t[1])[:2])))+'} Sec')

                    except Exception as e:
                        print(colored(e, 'red'))
                            
                        
                else:
                    self.passwd.set(" Please enter a  PASSWORD")
                    
            elif password == "" and self.exvalue.get() != "":
                
                dirname=(os.path.dirname(file))
                filename=os.path.basename(file)
                ext=self.exvalue.get()
                filename ,ex =os.path.splitext(filename)
                if "." in ext:
                    filename=filename+ext
                else:
                    filename=filename+"."+ext
                change_dirname=dirname+'/'+filename
                os.rename(file,change_dirname)
                self.filepath.set(" File extension changed")
            else:
                self.passwd.set(" Please enter a PASSWORD")

        else:
            if file=="" or file==' ':
                self.filepath.set(" Please enter File Path ")
            else:
                self.filepath.set(" This file doesn't exist ")

            
    def decode_file(self):            
        thr=Thread(target=self.decode_file_thread)
        thr.start()        
    def decode_file_thread(self):
        file=self.filepath.get()
        if os.path.exists(file):
            password=self.passwd.get()
            if password != "":
                if "Enter Password"  not in password:
                    ext=self.exvalue.get()
                    if ext == '':
                        ext=None
                    try:
                        self.filepath.set(" Decrypting , Please wait")
                        t=crypto.decrypt(filename=file,passwd=password,ext=ext)
                        error_status=t[0]
                        t=(str(t[1])).split('.')
                        if error_status==True:
                            self.filepath.set(" Decrypted ,please remember password In__{"+((str(t[0])+'.'+((t[1])[:2])))+'} Sec')
                        else:
                            self.filepath.set(" "+str(error_status))
                    except Exception as e:
                        print(colored(e, 'red'))
                            
                        
                else:
                    self.passwd.set(" Please enter a  PASSWORD")
            else:
                self.passwd.set(" Please enter a PASSWORD")

        else:
            if file=="" or file==' ':
                self.filepath.set(" Please enter File Path ")
            else:
                self.filepath.set(" This file doesn't exist ")
            
    def clear(self,event=None):
        self.passwd.set('')
        self.filepath.set('')
        self.exvalue.set('')

    def ask_file(self,event=None):
        path=askopenfilename(title='Open file')
        self.filepath.set(path)
        
    def ask_dir_file(self,event=None):
        path=askdirectory(title='Open directory ')
        self.filepath.set(path)
        
  
    

class __Main__():
    def __init__(self):
        self.cmd_value=False    
        try:
            sys.argv[1]
            self.cmd_value=True
        except:
            pass


    def run(self):
        if self.cmd_value==True:
            self.CLS_Mode()
        else:
            self.GUI_Mode()

    def GUI_Mode(self):
        Crypto_App()
        
    def CLS_Mode(self):
        global crypto
        crypto=Crypto()
        command=sys.argv
        file=None
        passwd=None
        ext=None
        type_=None
        chunk=None
        rename=False 

        ft = None
        init()
        print('')

        try:
            path=sys.argv[1]
            if os.path.exists(path):
                if os.path.splitext(path)[1] == '.crypt':
                    ft = True
                else:
                    ft = False
                    print(f" Type { colored('1','green') } for { colored('encrypt','green') } and { colored('2','yellow') } for { colored('decrypt','yellow') } (1 or 2) ", end="")
                    t = input(" : ").strip()
                    if t ==  "1":
                        type_ = "enc"
                    elif t == "2":
                        type_ = "dec"
                    else:
                        type_ = "enc"

                for i in range(3):
                    print(colored(" Enter Password", 'green'), end="")
                    passwd = input(" : ")
                    if len(passwd) >= 5 :
                        break
                    else:
                        print(colored("\n Please enter password that is at least 5 characters in length ", "red"))
                rename = True
                file = path
                if ft == True:
                    print(colored(" Please wait file is decrypting.....", "cyan"))
                    type_ = "dec"

                else:
                    print(colored(" Please wait file is encrypting.....", "cyan"))

            else:
                raise ValueError("Enter a file to encode...")
                  
        except Exception as e:
            try:
                type_=(command[1])
            except:
                pass
            n=0
            for cmd in command:
                if cmd=="-f" or cmd=='-file' or cmd=='-F':
                    file=(command[n+1])
                elif cmd=="-p" or cmd=='-P':
                    passwd=(command[n+1])
                elif cmd=="-ext" or cmd=='-e' or cmd=='-E' or cmd=='-EXT':
                    ext=(command[n+1])
                elif cmd=="-rn" or cmd =='-RN' or cmd=='-rename':
                    rename=True
                elif cmd=="-chunk":
                    chunk=(command[n+1])
                else:
                    pass
                n+=1

        if type_ == None:
            type_ = "-h"

        if type_ =='-h' or type_ =='-help' or type_ == 'help' or type_ =='h':
            p=('\n Commands :\n'+'  enc       : To encrypt file/folder\n'+'  dec       : To decrypt file/folder\n'+'  -p        : Password Eg.{ -p mahadev }\n'+'  -f        : file/folder path Eg.{ -f C:/user/..}'+'  -ext      : change file extention Eg.{ -ext mkv }\n''  -rn       : To encode name of files\n'+'  -chunk    : bytes_per_line_to_decode  Eg.{ -chunk 1024}\n'+' \n')
            print(colored(p, 'green'))
            print(colored(' Examples :- \n', 'cyan'))
            p='      1) crypto -enc -p mahadev -f c:/user../ -rn \n'+'      2) crypto -dec -p mahadev -f c:/user../ \n'+'      3) crypto -ext mp4   -f c:/user../ \n'
            print(colored(p, 'yellow'))
            print('\n')
            print(colored(' @_Aditya_Mukhiya_', 'magenta'))
            
            sys.exit(1)
        if file == None:
            raise  ValueError("Please Enter File/Path")
            
        if not os.path.exists(file):
            raise ValueError("This file/Path/folder doesn't exist")
        
        if type_ =='enc' or type_ =='-enc' or type_ =='encode' or type_ =='ENCODE' or type_ =='Encode':
            if passwd==None:
                raise ValueError("Please enter PASSWORD")
                
            if chunk != None:
                try:
                    chunk=int(chunk)
                except:
                    chunk=None
            try:
                t=crypto.encrypt(filename=file,passwd=passwd,ext=ext,rename=rename,chunk=chunk)
                p=(' Time_taken__enc__{ '+str(t[1])+' } Sec')
                print(colored(p, 'magenta'))
                
            except Exception as e:
                print(colored(e, 'red'))
            input()
        elif type_ in ['ext','-ext','EXT','Ext','-Ext','-EXT']:
            if ext== None:
                raise ValueError('Please enter EXTENTION')
            else:
                t=crypto.ext(filename=file,ext=ext)
                if t==True:
                    print(colored(' ____Done____________', 'green'))
            input()

        elif type_ in ['dec','-dec','-DEC','-Dec','Dec','DEC']:
            
            
            if passwd==None:
                raise ValueError("Please enter PASSWORD")
            
            try:
                t=crypto.decrypt(filename=file,passwd=passwd,ext=ext)
                p=(' Time_taken__dec_{ '+str(t[1])+' } Sec')
                print(colored(p, 'magenta'))
            except Exception as e:
                print(colored(e, 'red'))
            input()
                
        elif type_ =='all_file_in_folder':
            t=crypto.all_file_in_folder(file)
            n=0
            for f in t:
                n+=1
                if n%2 ==0:
                    col='magenta'
                else:
                    col='yellow'
                print(colored(str(n)+'}__ '+f,col))


def resource_path(relative_path):
    path=os.path.dirname(sys.executable)    
    return path+'/'+relative_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

                


if __name__ == "__main__":
    windll.shcore.SetProcessDpiAwareness(True)
    Application=__Main__()
    Application.run()

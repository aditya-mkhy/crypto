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
                print(colored(' Done :  '+org_filename+'', 'cyan'))
                
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
                    print(colored(' Done : '+dir_name+'/'+rn_name+'', 'yellow'))
                    
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
    
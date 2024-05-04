import os, sys
from colorama import init
from termcolor import colored
from crypto import Crypto

# def resource_path(relative_path):
#     path=os.path.dirname(sys.executable)    
#     return path+'/'+relative_path

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

def time_cal(sec):
    if sec < 60:
        return f"{sec} Sec"
    elif sec < 3600:
        return f"{sec//60}:{ str(sec%60)[:2]} Mint"
    elif sec < 216000:
        return f"{sec//3600}:{ str(sec%3600)[:2]} Hrs"
    elif sec < 12960000:
        return f"{sec//216000}:{ str(sec%216000)[:2]} Days"
    else:
        return "CE"
    



class Main:
    def __init__(self):
        self.arg = sys.argv[1:]

        if len(self.arg) == 0:
            self.help_text()

        self.file = None
        self.passwd = None
        self.ext = None
        self.cmd_type = None
        self.chunk = None
        self.rename = None

        self.crypto = Crypto()

        self.argparse(self.arg)
        self.handle_commads()
    


    def argparse(self, arg):

        # check if it is a encrypteed file path
        path = self.arg[0]
        if os.path.exists(path):
            # file is open by open_with
            self.handle_open_with(path=path)
            return True

        self.cmd_type = self.arg[0]

        count = 0
        for cmd in self.arg:
            if cmd == "-f" or cmd == '-file' or cmd == '-F':
                self.file = (self.arg[count + 1])
                
            elif cmd =="-p" or cmd == '-P':
                self.passwd = (self.arg[count + 1])

            elif cmd == "-ext" or cmd == '-e' or cmd == '-E' or cmd == '-EXT':
                self.ext=(self.arg[count + 1])

            elif cmd == "-rn" or cmd == '-RN' or cmd == '-rename':
                self.rename = True

            elif cmd == "-chunk":
                self.chunk = (self.arg[count + 1])

            count += 1


    def handle_open_with(self, path):
        if os.path.splitext(path)[1] == '.crypt': # if file is encrypted
            self.cmd_type = 'dec'

        else:
            print(f" Type { colored('1', 'green') } for { colored('encrypt', 'green') } and { colored('2', 'yellow') } for { colored('decrypt','yellow') } (1 or 2) ", end="")
            choice = input(" : ").strip()

            if choice == '1':
                self.cmd_type = 'enc'

            elif choice == '2':
                self.cmd_type = 'dec'
            
            else:
                self.cmd_type = 'enc'

        # input password
        for i in range(3):
            print(colored(" Enter Password", 'green'), end="")
            self.passwd = input(" : ").strip()
            if len(self.passwd) >  7:
                break
            else:
                print(colored(" Please enter password that is at least 8 characters in length ", "red",), end='\n\n')
                if i == 2:
                    exit()

        self.rename = True
        self.file = path
        print("file is ititn")


    def handle_commads(self):

        self.cmd_type = self.cmd_type.lower()
        #for help
        if self.cmd_type =='-h' or self.cmd_type =='-help' or self.cmd_type == 'help' or self.cmd_type =='h':
            self.help_text()

        if self.file == None:
            raise  ValueError("Please Enter File/Path")
        
        if not os.path.exists(self.file):
            raise ValueError("This file/Path/folder doesn't exist")


        if self.cmd_type in ['enc', '-enc', 'encode']:
            if self.passwd == None:
                raise ValueError("Please enter PASSWORD")
                
            if self.chunk != None:
                try:
                    self.chunk = 1024 * int(self.chunk)
                except:
                    self.chunk = 1024 * 128
            try:
                t = self.crypto.encrypt(filename = self.file, passwd = self.passwd, ext = self.ext, rename = self.rename, chunk = self.chunk)

                msg = f" ( encrypted in { time_cal( int(t[1]) ) } )"
                print(colored(msg, 'magenta'))
                
            except Exception as e:
                print(colored(e, 'red'))

        
        elif self.cmd_type in ['ext','-ext']:
            if self.ext == None:
                raise ValueError('Please enter Extension')
            else:
                t = self.crypto.ext(filename = self.file, ext = self.ext)
                if t==True:
                    print(colored(' Extentions changed', 'green'))

        elif self.cmd_type in ['dec','-dec']:
            
            if self.passwd == None:
                raise ValueError("Please enter PASSWORD")
            
            try:
                out = self.crypto.decrypt(filename = self.file, passwd = self.passwd, ext = self.ext)
                msg = f"( Time taken in decryption :  {time_cal( int(out[1]) )} )"
                print(colored(msg, 'magenta'))

            except Exception as e:
                print(colored(e, 'red'))
                
        elif self.cmd_type =='all_file_in_folder':
            files = self.crypto.all_file_in_folder(self.file)
            n = 0
            for file in files:
                n += 1
                if n%2 ==0:
                    col='magenta'
                else:
                    col='yellow'
                print(colored( f"{n}) {file}", col))


    def help_text(self):
        p=('\n Commands :\n'+'  enc       : To encrypt file/folder\n'+'  dec       : To decrypt file/folder\n'+'  -p        : Password Eg.{ -p mahadev }\n'+'  -f        : file/folder path Eg.{ -f C:/user/..}'+'  -ext      : change file extention Eg.{ -ext mkv }\n''  -rn       : To encode name of files\n'+'  -chunk    : bytes_per_line_to_decode  Eg.{ -chunk 1024}\n'+' \n')
        print(colored(p, 'green'))
        print(colored(' Examples :- \n', 'cyan'))
        p='      1) crypto -enc -p mahadev100 -f c:/user../ -rn \n'+'      2) crypto -dec -p mahadev100 -f c:/user../ \n'+'      3) crypto -ext mp4   -f c:/user../ \n'
        print(colored(p, 'yellow'))
        sys.exit(1)
        


        
if __name__ == "__main__":
    main = Main()
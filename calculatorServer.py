import socket
import sys
import time
import errno
import math         
from multiprocessing import Process

ok_message = '\nHTTP/1.0 200 OK\n\n'
nok_message = '\nHTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
    s_sock.send(str.encode("Python Calculator (LOGARITHM, SQUARE ROOT, EXPONENTIAL)\n Type 'exit' to close"))
    while True:
        data = s_sock.recv(2048)                        
        data = data.decode("utf-8")
        
        
        try:
            operation, value = data.split()
            opr = str(operation)
            num = int(value)
        
            if opr[0] == 'l':
                opr = 'Log'
                calc = math.log10(num)
            elif opr[0] == 's':
                opr = 'Square root'
                calc = math.sqrt(num)
            elif opr[0] == 'e':
                opr = 'Exponential'
                calc = math.exp(num)
            else:
                calc = ('ERROR')
        
            answer = (str(opr) + '(' + str(num) + ') = ' + str(calc))
            print ('Calculation successful!')
        except:
            print ('Invalid input')
            answer = ('Invalid input')
    
       
        
        if not data:
            break
            
        s_sock.send(str.encode(answer))
        
    s_sock.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",8888))                                   
    print("listening...")
    s.listen(88)                                         
    
    try:
        while True:
            try:
                s_sock, s_addr = s.accept()
                p = Process(target=process_start, args=(s_sock,))
                p.start()

            except socket.error:

                print('got a socket error')

            except Exception as e:        
                print("an exception occurred!")
                print(e)
                sys.exit(1)
    finally:
     	   s.close()
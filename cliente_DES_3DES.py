import socket
from Crypto.Cipher import DES

def scarSeparador(texto):
    contador = 0
    for i in range(1,len(texto)+2):
        if texto[-i] == 32:
            contador +=1
        else:
            break
    return texto[0:len(texto)-contador]

Cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Cliente.connect(("LocalHost", 8000))

llave_1 = b'sluceroj' #  des
llave_2 = b'nicolasc' #  3des
llave_3 = b'edmondmo' #  3des

Recibir = Cliente.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")
public_P,public_G,public_B = Recibir.split(",")

while True:
    try:
        priv_a = int(input("Ingrese un valor entre 0 y "+str(int(public_P)-1)+": "))
    except:
        print("Numero invalido, intente nuevamente")
    else:
        if(0<priv_a and priv_a<(int(public_P)-1)):
            break
        else:
            print("El valor debe estar entre 0 y "+str(int(public_P)-1))

public_A = (int(public_G)**priv_a)%int(public_P)

Enviar = str(public_A)
Cliente.send(Enviar.encode(encoding = "ascii", errors = "ignore"))

comun_K = (int(public_B)**priv_a)%int(public_P)

Enviar = str(comun_K)
Cliente.send(Enviar.encode(encoding = "ascii", errors = "ignore"))

try:
    Recibir = Cliente.recv(1024)
    
    print("Desencriptando mensaje con 3DES...\n")
    des1 = DES.new(llave_1, DES.MODE_ECB)
    des2 = DES.new(llave_2, DES.MODE_ECB)
    des3 = DES.new(llave_3, DES.MODE_ECB)
    
    textoplano = des1.decrypt(Recibir)
    textoplano = des2.encrypt(Recibir)
    textoplano = des3.decrypt(Recibir)
    
    print("DESENCRIPTANDO CON DES Y 3DES...\n") 
    textoplano = scarSeparador(textoplano)
    print("MENSAJE DESCRIFRADO:") 
    print(textoplano)
    archivo = open('mensajerecibido.txt','w+')
    archivo.writelines(textoplano.decode('ascii'))
    archivo.close()
    
except:
    pass

Cliente.close()
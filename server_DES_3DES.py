import socket
from Crypto.Cipher import DES

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(("LocalHost", 8000))
Server.listen(1)
Conexion, Addr = Server.accept()

llave_1 = b'sluceroj' #  des
llave_2 = b'nicolasc' #  3des
llave_3 = b'edmondmo' #  3des

def is_prime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

while True:
    try:
        public_P=int(input("Ingrese un numero primo para establecer conexión segura: "))
    except:
        print("Numero invalido, intente nuevamente")
    else:
        if(is_prime(public_P)):
            while True:
                try:
                    public_G=int(input("Ingrese un numero entre 0 y "+str(public_P)+" para establecer conexión segura: "))
                except:
                    print("Numero invalido, intente nuevamente")
                else:
                    if(0<public_G and public_G<public_P):
                        while True:
                            try:
                                priv_b=int(input("Ingrese un numero privado que este entre 0 y "+str(public_P-1)+": "))
                            except:
                                print("Numero invalido, intente nuevamente")
                            else:
                                if(0<priv_b and priv_b<(public_P-1)):
                                    break
                                else:
                                    print("El numero debe estar entre 0 y "+str(public_P-1)+"")
                        break
                    else:
                        print("El numero debe estar entre 0 y "+str(public_P)+"")
            break
        else:
            print("El numero ingresado debe ser un numero primo")

public_B = (public_G**priv_b)%public_P

Enviar = str(public_P) + "," + str(public_G) + "," +str(public_B)
Conexion.send(Enviar.encode(encoding = "ascii", errors = "ignore"))
  
Recibir = Conexion.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")

 
comun_K = (int(Recibir)**priv_b)%public_P

Recibir = Conexion.recv(1024)
Recibir = Recibir.decode(encoding = "ascii", errors = "ignore")

if comun_K == int(Recibir):


    print("Leyendo el mensaje...\n")
    archivo = open("mensajeentrada.txt","r+")
    lineas = archivo.readlines() 
    archivo.close()
    
    lineas = "".join(lineas) 
    lineas = lineas.encode("ASCII") 
    

    n = len(lineas)%8
    lineas = lineas+b' '*(8-n) if n!= 0 else lineas+ b''
 

    des1 = DES.new(llave_1, DES.MODE_ECB)
    des2 = DES.new(llave_2, DES.MODE_ECB)
    des3 = DES.new(llave_3, DES.MODE_ECB)
    
    encrypted_text = des1.encrypt(lineas)
    encrypted_text = des2.decrypt(lineas)
    encrypted_text = des3.encrypt(lineas)
    
    

    print("Enviando mensaje seguro...\n")
    Conexion.send(encrypted_text)
    print(lineas)
    #print(encrypted_text)
    
else:
    print("Las llaves no coinciden")

Conexion.close()
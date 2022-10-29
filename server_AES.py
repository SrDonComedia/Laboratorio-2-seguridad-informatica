from Crypto.Cipher import AES
import socket

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(("LocalHost", 8000))
Server.listen(1)
Conexion, Addr = Server.accept()

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
    llave_K = b"labseguridadnro2"

    print("LLAVES COINCIDEN, ENVIANDO MENSAJE...")
    archivo = open("mensajeentrada.txt","r+")
    lineas = archivo.readlines()
    archivo.close()
    
    lineas = "".join(lineas)
    lineas = lineas.encode("ASCII") 
    
    n = len(lineas)%16
    lineas = lineas+b' '*(16-n) if n!= 0 else lineas+b''
    
    aes = AES.new(llave_K, AES.MODE_ECB)   

    ciphertext = aes.encrypt(lineas)
    
    Conexion.send(ciphertext)
    print(lineas)
    print("\nMensaje encriptado enviado correctamente.")
Conexion.close()
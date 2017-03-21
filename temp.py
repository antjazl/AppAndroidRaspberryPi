# Importa librerias
import os
import glob
import time
import serial

os.system('sudo chmod a+rw /dev/ttyAMA0')
puerto= serial.Serial('/dev/ttyAMA0',baudrate=9600)

# Inicializa los pines GPIO
os.system('modprobe w1-gpio') #Activa el modulo GPIO
os.system('modprobe w1-therm') #Activa el modulo de temperatura

#Encuentra el archivo de dispositivo correcto que contiene datos de temperatura
base_dir= '/sys/bus/w1/devices/'
device_folder= glob.glob(base_dir + '28*')[0]
device_file= device_folder + '/w1_slave'

#Una funcion que lee datos del sensor
def read_temp_raw():

    f= open(device_file,'r') #Abre el archivo del dispositivo de temperatura
    lines= f.readlines() #Devuelve el texto
    f.close()
    
    return lines

#Convierte el valor del sensor en temperatura
def read_temp():
    lines= read_temp_raw() #Lee la temperatura del archivo de dispositivo

    #Mientras que la primera linea no contenga 'YES', espera 0,2 s
    #y luego lee el archivo de dispositivo de nuevo
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines= read_temp_raw()

    #Busca la posicion del '=' en la segunda linea del archivo del dispositivo
    equals_pos= lines[1].find('t=')

    #Si se encuentra '=' convierte el resto de la linea despues de '='
    #en grados centigrados
    
    if equals_pos != -1:
        temp_string= lines[1][equals_pos+2:]
        temp_c= float(temp_string)/1000.0
        temperatura=int(temp_c)
                
    return temperatura
  
    #Imprime la temperatura hasta que el programa se detenga
while True:
    print(read_temp())
    puerto.write(str(read_temp()))

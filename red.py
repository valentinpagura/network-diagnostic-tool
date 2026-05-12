#Script Python que dado un dominio/IP: resuelva DNS, compruebe puertos abiertos, mida latencia HTTP, valide certificado SSL.abs

from datetime import datetime
import socket
import time
import ssl
import subprocess
import requests
import json

dominio_input = input("ingrese un dominio: ")

def resolver_dns(dominio_input):
    try:
        #resolucion DNS
        ip_interna=socket.gethostbyname(dominio_input)
        return ip_interna

    except Exception as e:
        print(f"Error: {e}")
        return None

def comprobar_puertos(ip):
    puertos = [21, 22, 80, 443]     #Lista de puertos a comprobar
    resultados = {}                 #Diccionario para guardar los puertos abiertos y cerrados
    try:
        for x in puertos:  #Recorro la lista de puertos
            sock = socket.socket()
            sock.settimeout(1)
            resultado = sock.connect_ex((ip, x))
            resultados[x] = "abierto" if resultado == 0 else "cerrado"
            sock.close()                       #Cierro el socket despues de cada loop
    except Exception as e:
        print(f"Error: {e}")
    return resultados


def medir_latencia(dominio):
    try:
        inicio =time.time() #guardo la fecha y hora al arrancar
        respuesta = requests.get(f"https://{dominio}")
        fin = time.time() #guardo la fecha y hora al terminar
        
        latencia = fin - inicio
        return {"status_code": respuesta.status_code, "latencia": latencia}

    except Exception as e:
        print(f"Error: {e}")
        return None


def validar_ssl(dominio):
    
    try:
        contexto = ssl.create_default_context()
        sock = socket.create_connection((dominio, 443))
        
        ssl_socket = contexto.wrap_socket(sock, server_hostname=dominio)
        cert = ssl_socket.getpeercert()

        vencimiento = cert["notAfter"]
        fecha_vencimiento = datetime.strptime(vencimiento, "%b %d %H:%M:%S %Y %Z")
        hoy = datetime.now()

        dias_restantes = (fecha_vencimiento - hoy).days
        
        return {"valido": dias_restantes >= 0, "proximo a vencer": dias_restantes <= 30}
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def pasar_a_json(dominio, ip, puertos, latencia, ssl):
    resultado = {
        "dominio": dominio,
        "ip": ip,
        "puertos": puertos,
        "latencia": latencia,
        "ssl": ssl
    }
    print(json.dumps(resultado, indent=4))
    return resultado
        

resultado_ip = resolver_dns(dominio_input)
resultado_puertos = comprobar_puertos(resultado_ip)  #recibe la ip pero de forma interna gracias a la funcion
resultado_latencia = medir_latencia(dominio_input)
resultado_ssl = validar_ssl(dominio_input)
resultado_json = pasar_a_json(dominio_input, resultado_ip, resultado_puertos, resultado_latencia, resultado_ssl)


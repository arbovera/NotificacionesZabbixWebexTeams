#!/usr/bin/python 
# coding: utf-8

# 1ra linea: Dirección donde esta colocado python
# 2da linea: codificación a usar para el contenido del archivo

import requests  #Libreria para manjar solicitudes HTTP
import sys #Libreria para obtener parametros pasados desde la terminal de comandos
import json #Librería para manejar datos en formato json

token = 'ZWRmYWU1ZmUtOWY1OC00YTk1LWJkMjgtM2I2ZTJlOTM1NTBkNWIwYTlmMGEtMWNh_PF84_07151a94-b16f-4b3a-8ae0-aa812b9c4d88' #Token-Bot: Notificador de Zabbix (Modificar por el Acces Token de tu BOT)

def postMessage(messageAlert, id, accessToken, markdown):
    """
        Función para hacer POST del mensaje a traves de la API de Cisco Webex Teams
        Parametros:
            messageAlert: Mensaje a enviar
            markdown: Estilos del mensaje
            id: Identificador del receptor del mensaje
            accessToken: Token-Bot Notificador de Zabbix
        Retorna:
            La respuesta del POST ejecutado
    """

    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'Authorization': 'Bearer ' + accessToken, 'Content-type': 'application/json;charset=utf-8'}
    post_data = {'toPersonId': id, 'text': messageAlert, 'markdown': markdown}
    response = requests.post(url, json=post_data, headers=headers)
    return response

def getRoomId(email, accessToken):
    """
        Función que retorna el id del Correo solicitado, necesario para poder enviarle un mensaje directo
        Parametros:
            email: correo electronico
            accessToken: Token-Bot Notificador de Zabbix
        Retorna:
            Respuesta del GET ejecutado
    """

    url = 'https://api.ciscospark.com/v1/people'
    headers = {'Authorization': 'Bearer ' + accessToken, 'Content-type': 'application/json;charset=utf-8'}
    get_data = {'email': email}
    response = requests.get(url, params=get_data, headers=headers)
    return response
   
def buildMessage(subject, body):
    """
        Función para concatenar el cuerpo y el título del mensaje en uno solo texto
        Parametros:
            Subject: Título del mensaje
            body: Cuerpo del mensaje
        Retorna:
            mensaje unificado en un solo texto
    """

    messageAlert = subject + body 
    print(messageAlert)
    return messageAlert

def buildMessageMarkdown(subject, body):
    """
        Función para dar estilos al mensaje
        Parametros:
            Subject: Título del mensaje
            body: Cuerpo del mensaje
        Retorna:
            mensaje unificado con estilos en un solo texto
    """

    messageAlert = "**" + subject + ":** \n --- \n " + body
    return messageAlert
    
def getCodeRequest(req):
    """
        Función analiza el codigp de respuesta y nos regresa el significado de tal codigo
        Parametros:
            req: respuesta de solicitud
        Retorna:
            codigo de reespuesta
    """
    if (req.status_code == 401):
        print(str(req.status_code) + ":Authentication credentials were missing or incorrect.")
    elif (req.status_code == 200):
        print(str(req.status_code) + ":Successful request with body content.")
    elif (req.status_code == 403):
        print(str(req.status_code) + ":The request is understood, but it has been refused or access is not allowed")
    elif (req.status_code == 400):
        print(str(req.status_code) + ":The request was invalid or cannot be otherwise served. An accompanying error message will explain further.")
    return req.status_code

#Obteniendo Argumentos pasados desde la terminal de comandos
args = sys.argv
zbxTo = args[1] #Correo Electronico
zbxSubject = args[2] #Título del Mensaje
zbxBody = args[3] #Cuerpo del Mensaje

#Construyendo Mensaje
messageAlert = buildMessage(zbxSubject, zbxBody)
markdown = buildMessageMarkdown(zbxSubject, zbxBody)

#Obteniendo room id
responseGetRoom = getRoomId(zbxTo, token)
content = responseGetRoom.json()
id = str(content["items"][0]["id"])

#Checando repuesta de getRoomId
resGetRoom = getCodeRequest(responseGetRoom)

#Posteando mensaje
responsePostMessage = postMessage(messageAlert, id, token, markdown)

#Checando repuesta del post                                                                                             
resPostMessage = getCodeRequest(responsePostMessage)    
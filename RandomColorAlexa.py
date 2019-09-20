"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import random
import boto3
import os


#Info to connect to broker
user="broker user"
password="broker password"
host="broker host"
port="broker port"

# Topics Mqtt
random_topic="RandomColor"
color_blanco="BLANCO"
color_amarillo="AMARILLO"
color_magenta="MORADO"
color_morado="MORADO"
color_rojo="ROJO"
color_azul="AZUL"
color_rosado="ROSADO"
color_verde="VERDE"
color_naranja="NARANJA"
#Connecting to MQTT Broker
mqttc = mqtt.Client()
mqttc.username_pw_set(user,password)
mqttc.connect(host,port)
all_colors=['rojo','azul','blanco','rosado','morado','negro','magenta','amarillo','verde','naranja']
file="/tmp/color.txt"
flag=0 

#Guardar la partida esta funcion guarda en un bucket el archivo de color
def GuardarPartidaEnBucket():
    s3=boto3.client("s3")
    s3.upload_file(file,"colores","colorPartidas.txt")

# function thatgives wich elemnts las in the array 
def diff(first,second):
	second=set(second)
	return[item for  item in first if item not in second]

#function that give a random color
def fromFileToArray():
    text_file = open(file, "r")
    file_colors = text_file.read().split(',')
    file_colors=file_colors[:-1]
    return file_colors

def WriteNewColor(colors):
	# debe agregarse un color que no este escrito en el archivo de texto
	number  = random.randint(0,len(colors)-1)
	f = open(file,"a")
	f.write(colors[number]+",")
	f.close()
	mqttc.connect(host,port)
	if colors[number] == "verde":
	    mqttc.publish(random_topic,color_verde)
	if colors[number]=="azul":
	    mqttc.publish(random_topic,color_azul)
	if colors[number] == "blanco":
	    mqttc.publish(random_topic,color_blanco)
	if colors[number]=="rojo":
	    mqttc.publish(random_topic,color_rojo)
	if colors[number] == "magenta":
	    mqttc.publish(random_topic,color_magenta)
	if colors[number]=="morado":
	    mqttc.publish(random_topic,color_morado)
	if colors[number] == "naranja":
	    mqttc.publish(random_topic,color_naranja)
	if colors[number]=="amarillo":
	    mqttc.publish(random_topic,color_amarillo)
	if colors[number]=="rosado":
	    mqttc.publish(random_topic,color_rosado)
	return colors[number]

def verifyColorPick():
    
    file_colors_array=fromFileToArray()
    print(file_colors_array)
    color_complement=diff(all_colors,file_colors_array)
    return color_complement


def AddNewparticipant():
    #cojemos lo que haya en el bucket y lo escribimos en el archivo temporal
    
	s3=boto3.client("s3")
	data = s3.get_object(Bucket="colores", Key='colorPartidas.txt')
	contents = data['Body'].read()
	contents=contents.decode("utf-8")
	if contents=='':
	    print('el content esta vacio')
	    EndSession()
	    flag=1
	    
	else:
	    flag=0
	   
	    split_contents=contents.split(',')
	    print(type(split_contents))
	    print(split_contents)

	    EndSession()
	    for x in range(0, len(split_contents)-1):
	        f = open(file,"a")
	        f.write(split_contents[x]+",")
	        f.close()
	        
	        print('Agregado al archivo temporal, color '+ split_contents[x])
    
	try:
	    if flag==1:
	        print(0/0)
	        
	    fromFileToArray()
	    color_complement=verifyColorPick()
	    print(color_complement)
	    if len(color_complement) <1:
	        print('ya se acabaron los colores')
	        return 'se acabaron los colores'
	    added_color=WriteNewColor(color_complement)
	    GuardarPartidaEnBucket()
	    return "Nuevo color agregado .." + added_color

	except:
		#print('No se iniciado una partida')
		#Aqui caera en el primer color que se agrege
		added_color=WriteNewColor(all_colors)
		# Lo guardo en el bucket
		GuardarPartidaEnBucket()
		return "Primer color agregado .." + added_color
		

def chooseParticipant():
    s3=boto3.client("s3")
    data = s3.get_object(Bucket="colores", Key='colorPartidas.txt')
    contents = data['Body'].read()
    contents=contents.decode("utf-8")
    if contents=='':
        print('el content esta vacio')
        return 'No hay jugadores en esta partida '
    else:
        split_contents=contents.split(',')
        print(type(split_contents))
        print(split_contents)
        EndSession()
        for x in range(0, len(split_contents)-1):
            f = open(file,"a")
            f.write(split_contents[x]+",")
            f.close()
            print('Agregado al archivo temporal, color '+ split_contents[x])
    try:
        colors_in_file=fromFileToArray()
        number  = random.randint(0,len(colors_in_file)-1)
        chossed_color=colors_in_file[number]
        print(chossed_color)
        mqttc.connect(host,port)
        if chossed_color == "verde":
            mqttc.publish(random_topic,color_verde)
        if chossed_color=="azul":
            mqttc.publish(random_topic,color_azul)
        if chossed_color == "blanco":
            mqttc.publish(random_topic,color_blanco)
        if chossed_color=="rojo":
            mqttc.publish(random_topic,color_rojo)
        if chossed_color == "magenta":
            mqttc.publish(random_topic,color_magenta)
        if chossed_color=="morado":
            mqttc.publish(random_topic,color_morado)
        if chossed_color == "naranja":
            mqttc.publish(random_topic,color_naranja)
        if chossed_color=="amarillo":
            mqttc.publish(random_topic,color_amarillo)
        if chossed_color=="rosado":
            mqttc.publish(random_topic,color_rosado)
    
            
        return 'el color es ...'+chossed_color
    except:
        print('Aun no hemos iniciado partida')
        return 'Aun no hemos iniciado una partida'


def WhosPlaying():
    
	colors_string='los colores jugando son: '
	#llamamos al archivo del bucket
	s3=boto3.client("s3")
	data = s3.get_object(Bucket="colores", Key='colorPartidas.txt')
	contents = data['Body'].read()
	contents=contents.decode("utf-8")
	if contents=='':
	    print('el content esta vacio')
	    return 'No hay jugadores en esta partida'
	else:
	    split_contents=contents.split(',')
	    print(type(split_contents))
	    print(split_contents)
	    EndSession()
	    for x in range(0, len(split_contents)-1):
	        f = open(file,"a")
	        f.write(split_contents[x]+",")
	        f.close()
	        print('Agregado al archivo temporal, color '+ split_contents[x])
	try:
	    colors_in_file=fromFileToArray()
	    for x in range(0, len(colors_in_file)):
	        colors_string+=colors_in_file[x]
	        colors_string+=' '
	    print(colors_string)
	    return colors_string
	except:
	    print('Nadie esta Jugando')
	    return('Parece que no hay colores')

		
def EndSession():
    try:
        print("borramos el archivo temporal")
        open(file, 'w').close()
        
    except:
	    print('No habia que eliminar')
	    
def FinalSession():
    try:
        print("borramos el archivo temporal")
        open(file, 'w').close()
        GuardarPartidaEnBucket()
        
        os.remove(file)
        
    except:
	    print('No habia que eliminar')
	


# --------------- Helpers that build all of the responses ----------------------


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_PARTICIPANT_response():
    respuesta=AddNewparticipant()
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"
    speech_output = respuesta
    reprompt_text = " "
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
def get_JUGADORES_response():
    respuesta=WhosPlaying()
    session_attributes = {}
    card_title = "Test"
    speech_output = respuesta
    reprompt_text = " "
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_RANDOM_response():
    respuesta= chooseParticipant()
    session_attributes = {}
    card_title = "Test"
    speech_output = respuesta
    reprompt_text = " "
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    

def get_TERMINARJUEGO_response():

    FinalSession()
    session_attributes = {}
    card_title = "Test"
    speech_output = "Se ha terminado la partida"
    reprompt_text = " "
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    



def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Bienvenido a RandomColor el juego"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Gracias, simepre presente  "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
        
    if intent_name == "participante":
        return get_PARTICIPANT_response()
        
    elif intent_name == "jugadores":
        return get_JUGADORES_response()
        
    elif intent_name == "random":
        return get_RANDOM_response()
        
    elif intent_name == "terminarJuego":
        return get_TERMINARJUEGO_response()
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
    



# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Escuchar microfono y devolver audio como texto

def transformar_audio_en_texto():

    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print('Ya puedes hablar...')

        # Guardar audio
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language="es-co")

            # Prueba ingreso
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido

        # En caso de error de comprension
        except sr.UnknownValueError:

            # Prueba de que no comprendio el
            print("No entendí")

            # devolver error
            return "Sigo esperando"

        # En caso de no resolver pedido
        except sr.RequestError:

            # Prueba de que no comprendio el
            print("Ups, no hay servicio")

            # devolver error
            return "Sigo esperando"

        # Error inesperado
        except:

            # Prueba de que no comprendio el
            print("Ups, algo ha salido mal")

            # devolver error
            return "Sigo esperando"

# Funcion voz del asistente
def hablar(mensaje):

    # Encender el motor de pyttsx3
    engine = pyttsx3.init()

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el día de la semana
def pedir_dia():

    # Variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # Variable día semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombres de días
    calendario = {0: 'Lunes',
                  1: 'Mares',
                  2: 'Miercoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # Decir día semana
    hablar(f'Hoy es {calendario[dia_semana]}')

# Informar que hora es
def pedir_hora():

    # Datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # Decir hora
    hablar(hora)


# Saludo inicial
def saludo_inicial():

    # Variable de datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif hora.hour >= 6 and hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas Tardes'

    # Decir saludo
    hablar(f'{momento} Jorge, soy Marce, tu asistente personal. ¿En qué te puedo ayudar?')

# Fucion central del asistente
def pedir():

    # Activar saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # Loop central
    while comenzar:

        # Activar el microfono y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, abriendo navegador web')
            webbrowser.open('https://www.google.com')
            continue
        elif 'Qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'Qúe hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Estoy trabajando en ello')
            pedido = pedido.replace('busca en internet', 'nada')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Reproduciendo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL',
                       'amazon':'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, pero no la he encontrado')
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break

pedir()
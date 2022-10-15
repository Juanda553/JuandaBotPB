'''
Por favor, no edites nada de este código para que sirva todo perfectamente.
Tampoco robes ni modifiques nada del codigo. Solo para uso PROPIO.
Tampoco elimines ni edites ningun archivo de la carpeta assets para evitar errores.
Si tienes algun problema, puedes decirmelo por el Discord de JuandaBot.
Estare constantemente tratando de mejorar este programa, asi que estar algo pendiente al Discord <3
© JuanDa553 2020 • @JuandaLeaks553 | @JuanDa553YT | Juanda553#9543 
'''

from traceback import print_tb
import requests, time, PIL, math, os, json, shutil, datetime, twitter

from datetime import date, datetime
from PIL import Image, ImageFont, ImageDraw
from os import listdir, system
from colorama import *
from assets.JuandabotUtiles import *
from pypresence import Presence

################################################################################################################################################################################

print('Cargando...')

# Cargado inicial de configuraciones por el usuario

jdbFile = open("assets/config.json"); jdbData = json.load(jdbFile); jdbFile.close()

botVersion = '1.1.1'
fnapikey = jdbData["general"]["fortniteapiio"]
tituloCustomItemShop = jdbData["tienda"]["titulo"]
fondoCustomItemShop = jdbData["tienda"]["colorDeFondo"]
tiendaOGdias = jdbData["tienda"]["diasOG"]
bgCustomImage = jdbData["tienda"]["fondoImagen"]

twitterIniciar = jdbData["twitter"]["activo"]
key = jdbData["twitter"]["key"]
secret_key = jdbData["twitter"]["secret_key"]
token = jdbData["twitter"]["token"]
secret_token = jdbData["twitter"]["secret_token"]

twtBodyTienda = jdbData["twitter"]["tweetsCuerpos"]["tienda"]
twtBodyOg = jdbData["twitter"]["tweetsCuerpos"]["itemsOg"]
twtBodySecciones = jdbData["twitter"]["tweetsCuerpos"]["secciones"]

headers = {'Authorization': fnapikey}
fuente = f'assets/fuentes/Fortnite.otf'

os.system("cls")
os.system(f"TITLE JuandaBot {botVersion}")

# Comprobar version actual de JuandaBot
juandaBotAPI = requests.get('https://pastebin.com/raw/P0nLHktg')
juandaBotApiData = juandaBotAPI.json()

if botVersion != juandaBotApiData["public"]["version"]:
    windowsBox('JuandaBot', f'La version actual de JuandaBot que estas usando, es una version antigua, estas usando actualmente la {botVersion} y la ultima version es la {juandaBotApiData["public"]["version"]}', 0)

linkDiscord = juandaBotApiData["public"]["linkDiscord"]
rpcImage = juandaBotApiData["public"]["RPC"]["RPCimage"]
rpcBotones = juandaBotApiData["public"]["RPC"]["RPCbuttons"]
JuandaFortUser = juandaBotApiData["owner"]

hoy = datetime.now(); fechaHoy = date(hoy.year, hoy.month, hoy.day)
fechaHoySTR = f"{hoy.year}-{hoy.month}-{hoy.day}"

################################################################################################################################################################################

# Autentificar con twitter
if twitterIniciar:
    try:
        print("Conectando a Twitter")
        twitterAPI = twitter.Api(consumer_key=key, consumer_secret=secret_key, access_token_key=token, access_token_secret=secret_token);twitterAPI.VerifyCredentials()
        twitterConnect = True
        print('Twitter Conectado con éxito.')
    except Exception as Error:
        twitterConnect = False
        twtConectionErrorMsg = Error
        jdbconsole.warning('No se pudo conectar a Twitter. Revise las keys')
else: #Si está desactivado en las configuraciones
    jdbconsole.warning('La conexión a Twitter está desactivada en config.json')
    twitterConnect = False
    twtConectionErrorMsg = "Desactivado en sus configuraciones"

# RCP de Discord
try:
    print("Conectando RPC de Discord...")
    RPC = Presence(919501199428976641); RPC.connect()
    RPC.update(state="Cargando...", large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones)
    rcpConnect = True
    print('Discord Conectado con éxito.')
except Exception as Error:
    rcpConectionErrorMsg = Error
    rcpConnect = False
    jdbconsole.warning('No se pudo conectar a Discord.')

################################################################################################################################################################################

# Funcion - Obtener la tienda actual
def tienda():
    print(Fore.YELLOW + f"Tienda Diaria.\nLOGGER\n\n")
    if rcpConnect: RPC.update(state='Tienda de objetos BR', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())

    # Limpiando Carpeta
    start = time.time(); x = 1
    jdbconsole.log('Limpiando carpeta de items...')
    try:
        shutil.rmtree('./output/tiendaHoy')
        os.makedirs('./output/tiendaHoy')
    except:
        os.makedirs('./output/tiendaHoy')

    # Consumiendo API
    try:
        jdbconsole.log('Obteniendo información de la tienda...')
        response = requests.get('https://fortniteapi.io/v2/shop?lang=es', headers=headers); new = response.json()
        y = len(new["shop"])
        jdbconsole.log('Información de tienda obtenida con exito.')
        jdbconsole.log(f'Se encontraron {y} items en la tienda de hoy.\n')
    except Exception as error:
        jdbconsole.error('Error al obtener la tienda.')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)
        jdbconsole.tip('Revisa que tengas la key de FortniteApi.io en config.json en la carpeta assets')
        jdbconsole.exitMsg()
    
    jdbconsole.log('Preparando para empezar a generar items...')
    print('')
    for i in new["shop"]:
        try:
            tipopopo = i["mainType"]
            imgUrl = i["displayAssets"][0]["full_background"]
            id = i["mainId"]

            # Descargando imagen del item
            img = requests.get(imgUrl, allow_redirects=True); open(f'./assets/cache/{id}.png', 'wb').write(img.content)
            cosImg=Image.open(f'./assets/cache/{id}.png'); cosImg=cosImg.resize((512,512)); cosImg.save(f'./assets/cache/{id}.png')

            img = Image.open(f'./assets/cache/{id}.png').convert('RGBA')
    
            draw=ImageDraw.Draw(img)
    
            # Comprobar días sin salir
            try:
                itemUltimaSalida = i["previousReleaseDate"]
                a = datetime.strptime(itemUltimaSalida, '%Y-%m-%d').date(); b = a - fechaHoy
                itemDiasSinSalir = f'{b.days} días'; itemDiasSinSalir = itemDiasSinSalir.replace("-", "")
            except:
                itemDiasSinSalir = 'Nuevo!'

            # Dibujar nombre, precio y días sin salir en la imagen
            font=ImageFont.truetype(fuente,24)
            draw.text((4,487),itemDiasSinSalir,font=font,fill="white")

            # Guardando imagen generada completa, en orden de tipo de item -- Porcentaje de generación
            if tipopopo == 'bundle':
                img.save(f'./output/tiendaHoy/a{id}.png')
            elif tipopopo == "outfit":
                img.save(f'./output/tiendaHoy/b{id}.png')
            else:
                img.save(f'./output/tiendaHoy/{id}.png')
            os.remove(f'./assets/cache/{id}.png')
            porcentaje = x/y; porcentaje = porcentaje * 100

            jdbconsole.log(f'Imagen de {i["displayName"]} generada. ({x}/{y} - {int(round(porcentaje, 0))}%)')
            x=x+1
        except Exception as error:
            jdbconsole.error(f'Error al generar la imagen de {i["displayName"]}, ignorando item. - {error}')

    # Merge de la tienda pe xd
    try:
        jdbconsole.log('Juntando Imágenes y creando la tienda...')
        
        # Conteo de items, y creacion de la imagen png de todos los items a medida
        imagenes = [file for file in listdir(f'./output/tiendaHoy')]
        imagenesContadas = int(round(math.sqrt(len(imagenes)+0.5), 0))
        imagenCosmeticos = Image.new("RGBA", (519*imagenesContadas, 519*imagenesContadas), color=(0, 0, 0, 0))
        x = 6; y = 6
        contador = 0

        # Pegando las imagenes en la imagen PNG principal
        for img in imagenes:
            cosmetico = Image.open(f"./output/tiendaHoy/{img}").convert("RGBA")
            if contador >= imagenesContadas:
                y += 518; x = 6
                contador = 0
            imagenCosmeticos.paste(cosmetico, (x, y), cosmetico)
            x += 518
            contador += 1

        # Guardando imagen PNG con todos los items
        imagenCosmeticos.save("./assets/cache/items.png"); xCosmeticos,yCosmeticos = imagenCosmeticos.size
        # Creando una imagen para toda la tienda con las medidas
        imagenFinal = Image.new("RGBA", (xCosmeticos, yCosmeticos+590), color="#"+fondoCustomItemShop)
        xFinal, yFinal = imagenFinal.size

        # Pegando la imagen de fondo personalizada
        if bgCustomImage:
            customBgImg = Image.open('assets/imgs/fondo.png').convert('RGBA')
            customBgImg = customBgImg.resize((xFinal, yFinal))
            imagenFinal.paste(customBgImg, (0,0), customBgImg)

        # Pegando la imagen PNG de todos los items, en la imagen de la tienda
        imagenFinal.paste(imagenCosmeticos, (0, 517), imagenCosmeticos)
        draw=ImageDraw.Draw(imagenFinal)

        # Escribiendo en la imagen titulo, fecha y CC de JuandaBot
        font=ImageFont.truetype(fuente,240)
        draw.text((xFinal/2, 44),tituloCustomItemShop,font=font,fill='white', anchor="mt")
        font=ImageFont.truetype(fuente,140)
        draw.text((xFinal/2, 339),fechaHoySTR,font=font,fill='white', anchor="mt")
        font=ImageFont.truetype(fuente,60)
        draw.text((xFinal-7, 458),"Generado con JuandaBot",font=font,fill='white', anchor="rt")

        # Comprimiendo imagen y guardando
        xComprimida, yComprimida = math.floor(xFinal/2), math.floor(yFinal/2)
        imagenFinal = imagenFinal.resize((xComprimida, yComprimida),Image.ANTIALIAS); imagenFinal.save(f"output/tienda.png",quality=65)
        jdbconsole.log('Imagen Generada en la carpeta output!')

        # Subir a Twitter en caso que esté activado + su Exception en caso de error
        if twitterConnect:
            jdbconsole.log('Subiendo a Twitter.')
            try:
                twitterAPI.PostUpdate(twtBodyTienda, media='output/tienda.png')
                jdbconsole.log('Tweet Subido con éxito!')
            except Exception as error:
                jdbconsole.error('Ha ocurrido un error al intentar subir el tweet')
                jdbconsole.error(error)
                jdbconsole.errTip(linkDiscord)
                jdbconsole.exitMsg()
        else:
            jdbconsole.warning('Twitter desconectado o no se encontraron las keys.')
        end = time.time()
        jdbconsole.tip('Bot hecho por @JuanDa553YT')
        jdbconsole.tip(f'Tiempo de generación: {round(end - start, 2)} segundos.')

        input(Fore.GREEN + '\nTodo listo! Presiona ENTER para volver al menú, o si lo deseas puedes cerrar ya el programa...'); menu()
    except Exception as error:
        jdbconsole.error('Hubo un error al juntar los items y crear la imagen completa de la tienda')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)


# Función - Generar items OG
def itemsOg():
    if rcpConnect: RPC.update(state='Tienda OG', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())
    print(Fore.YELLOW + f"Items OG\nDías para OG: {tiendaOGdias}\nLOGGER\n\n")

    # Inicializando variables
    x = 0
    y = 0
    start = time.time()

    # Literal el print de abajo dice lo que hace este bloque de código xd
    jdbconsole.log('Limpiando carpeta de items...')
    try:
        shutil.rmtree('./output/tiendaOg')
        os.makedirs('./output/tiendaOg')
    except:
        os.makedirs('./output/tiendaOg')

    # Consumiendo API
    try:
        jdbconsole.log('Obteniendo informacion de tienda actual...')
        api = "https://fortniteapi.io/v2/shop?lang=es"; 
        resp = requests.get(api, headers=headers); data = resp.json()["shop"]
    except Exception as error:
        jdbconsole.error('Hubo un error al obtener la informacion de la tienda actual!')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)
        jdbconsole.exitMsg()

    # Literal el print de abajo dice lo que hace este bloque de código xd x2
    try:
        jdbconsole.log('Contando items Og de la tienda actual...')
        for i in data:
            itemUltimaFecha = i["previousReleaseDate"]
            try:
                a = datetime.strptime(itemUltimaFecha, '%Y-%m-%d').date()
                c = a - fechaHoy; d = abs(c.days)
            except:
                d = 0
            if d >= tiendaOGdias and i["mainType"] != 'bundle':
                y += 1

        if y >=1:
            jdbconsole.log(f'Se encontraron {y} items og de la tienda actual!')
        else:
            print('No se encontró ningún item "OG" en la tienda actual.')
            jdbconsole.log(Fore.GREEN + '\nTodo listo! Presiona ENTER para volver al menú, o si lo deseas puedes cerrar ya el programa...'); menu()

    except Exception as error:
        jdbconsole.error('Error al contar los items OG de hoy')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)

    # Generando item por items OG de la tienda
    print('')
    jdbconsole.log('Preparando para empezar a generar items...')
    print('')
    for i in data:
        itemUltimaFecha = i["previousReleaseDate"]

        # Obteniendo días sin sales pe
        try:
            a = datetime.strptime(itemUltimaFecha, '%Y-%m-%d').date()
            c = a - fechaHoy; d = abs(c.days)
        except:
            d = 0

        # Comprobar que los días que tiene sin salir son igual o mayores que los días predefinidos en config.json. Y que no sea un bundle. Para generar ese item
        if d >= tiendaOGdias and i["mainType"] != 'bundle':
            try:
                x+=1
                tipopopo = i["mainType"]
                imgUrl = i["displayAssets"][0]["full_background"]
                id = i["mainId"]

                # Descargando imagen
                img = requests.get(imgUrl, allow_redirects=True)
                open(f'./assets/cache/{id}.png', 'wb').write(img.content)
                img=Image.open(f'./assets/cache/{id}.png')
                img=img.resize((512,512))
                img.save(f'./assets/cache/{id}.png')
                img = Image.open(f'./assets/cache/{id}.png')
                draw = ImageDraw.Draw(img)

                # Pintando días sin salir ne la imagen
                itemUltimaSalida = i["previousReleaseDate"]
                a = datetime.strptime(itemUltimaSalida, '%Y-%m-%d').date(); b = fechaHoy - a
                itemDiasSinSalir = f'{b.days} días'

                font=ImageFont.truetype(fuente,24)
                draw.text((4,487),itemDiasSinSalir,font=font,fill="white")

                # Guardando item en orden de tipo de objeto
                if tipopopo == "outfit":
                    img.save(f'./output/tiendaOg/b{id}.png')
                else:
                    img.save(f'./output/tiendaOg/{id}.png')
                os.remove(f'assets/cache/{id}.png')
                porcentaje = x/y; porcentaje = porcentaje * 100

                jdbconsole.log(f'Imagen de {i["displayName"]} generada. ({x}/{y} - {int(round(porcentaje, 0))}%)')
            except Exception as error:
                jdbconsole.error(f'Error al generar la imagen de {i["displayName"]}, ignorando item. - {error}')

    # Merge de los items og
    if x >= 1:
        jdbconsole.log('Juntando items...')
        try:
            # Conteo de items y creando imagen PNG con los items
            imagenes = [file for file in listdir(f'./output/tiendaOg')]
            imagenesContadas = int(round(math.sqrt(len(imagenes)), 0))
            imagenCosmeticos = Image.new("RGBA", (519*imagenesContadas, 519*imagenesContadas), color=(0, 0, 0, 0))
            x = 6; y = 6
            contador = 0

            # Pegando los items en la imagen PNG
            for img in imagenes:
                cosmetico = Image.open(f"./output/tiendaOg/{img}").convert("RGBA")
                if contador >= imagenesContadas:
                    y += 518; x = 6
                    contador = 0
                imagenCosmeticos.paste(cosmetico, (x, y), cosmetico)
                x += 518
                contador += 1
            imagenCosmeticos.save("./assets/cache/itemsOg.png"); xCosmeticos,yCosmeticos = imagenCosmeticos.size

            # Generando nueva imagen principal
            imagenFinal = Image.new("RGBA", (xCosmeticos, yCosmeticos+181), color="#"+fondoCustomItemShop)
            xFinal, yFinal = imagenFinal.size

            # Fondo personalizado
            if bgCustomImage:
                customBgImg = Image.open('assets/imgs/fondo.png').convert('RGBA')
                customBgImg = customBgImg.resize((xFinal, yFinal))
                imagenFinal.paste(customBgImg, (0,0), customBgImg)

            # Pegando PNG en la imagen de tienda y guardando.
            imagenFinal.paste(imagenCosmeticos, (0, 108), imagenCosmeticos)
            draw=ImageDraw.Draw(imagenFinal)

            font=ImageFont.truetype(fuente,60)
            draw.text((xFinal-7, 49),"Generado con JuandaBot",font=font,fill='white', anchor="rt")

            imagenFinal.save(f"output/itemsOg.png")

            jdbconsole.log('Imagen Generada en la carpeta output!')
        except Exception as error:
            jdbconsole.error('Error al juntar items')
            jdbconsole.error(error)
            jdbconsole.errTip(linkDiscord)
 
        # Subir a Twitter en caso de tenerlo activo
        if twitterConnect:
            jdbconsole.log('Subiendo a Twitter...')
            try:
                twitterAPI.PostUpdate(twtBodyOg, media='output/itemsOg.png')
                jdbconsole.log('Tweet subido con éxito!')
            except Exception as error:
                jdbconsole.error('Error al subir el Tweet')
                jdbconsole.error(error)
                jdbconsole.errTip(linkDiscord)
                jdbconsole.exitMsg()
        else:
            jdbconsole.warning('Twitter desconectado o no se encontraron las keys.')
    end = time.time()
    jdbconsole.tip('Bot hecho por @JuanDa553YT')
    jdbconsole.tip(f'Tiempo de generación: {round(end - start, 2)} segundos.')
    input(Fore.GREEN + '\nTodo listo! Presiona ENTER para volver al menú, o si lo deseas puedes cerrar ya el programa...'); menu()

# Función - Secciones de tienda actuales en la API
def secciones():
    if rcpConnect: RPC.update(state='Secciones de Tienda', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())
    print(Fore.YELLOW + f'Secciones de tienda.\nLOGGER\n\n')

    # Literal el print de abajo dice lo que hace este bloque de código xd x3
    jdbconsole.log('Conectando con la API')
    try:
        response = requests.get('https://fn-api.com/api/shop/br/sections?lang=es')
        data = response.json()['data']['sections']
        print('API conectada con éxito')
    except Exception as error:
        jdbconsole.error('Ha ocurrido un error al intentar conectar con la API')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)
        jdbconsole.exitMsg()
    secciones = "" # Inicializando variable de secciones

    # Literal el print de abajo dice lo que hace este bloque de código xd x4
    jdbconsole.log('Generando secciones')
    for i in data:
        secciones += f'• {i["name"]}. x{i["quantity"]}\n'

    jdbconsole.log('Secciones obtenidas con éxito!\n')
    print(Fore.CYAN + "Secciones de la tienda de Fortnite para esta noche.:\n\n"+ secciones)

    # # Literal el print de abajo dice lo que hace este bloque de código xd x5
    if twitterConnect:
        print('Subiendo a Twitter')
        try:
            twitterAPI.PostUpdate(twtBodySecciones+secciones)
            print('Tweet subido con éxito!')
        except Exception as error:
            jdbconsole.error('Error al subir el Tweet')
            jdbconsole.error(error)
            jdbconsole.errTip(linkDiscord)
            jdbconsole.exitMsg()
    else:
        jdbconsole.warning('Twitter desconectado o no se encontraron las keys.')

    jdbconsole.tip('Bot hecho por @JuanDa553YT')
    input(Fore.GREEN + '\nTodo listo! Presiona ENTER para volver al menú, o si lo deseas puedes cerrar ya el programa...'); menu()

# Función Automatica - Secciones de tienda actuales de la API
def autoSecciones():
    if rcpConnect: RPC.update(state='Secciones de Tienda AUTO', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())
    print(Fore.YELLOW + f'Secciones de tienda - MODO AUTOMATICO.\nLOGGER\n\n')

    # Literal el print de abajo dice lo que hace este bloque de código xd x6
    jdbconsole.log("Conectando con la API")
    try:
        data1 = requests.get("https://fn-api.com/api/shop/br/sections?lang=es").json()['data']['hash']
        jdbconsole.log('API conectada con éxito')
    except Exception as error:
        jdbconsole.error('Ha ocurrido un error al intentar conectar con la API')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)
        jdbconsole.exitMsg()
        
    # Inicializando variable de secciones e intentos
    secciones = "" 
    att = 1

    # Bucle "Infinito"
    while 1:
            resp2 = requests.get("https://fn-api.com/api/shop/br/sections?lang=es")
            
            if resp2:
                data2 = resp2.json()
                jdbconsole.log(f"Detectando cambios en las secciones | Intento #{att}")
                att += 1

                # Detectar si data1 y data 2 no son iguales
                if data1['data']['hash'] != data2['data']['hash']:
                    # Generar las nuevas secciones llamando a la funcion de secciones
                    jdbconsole.tip("Cambio de secciones!")
                    secciones()
            
            else:
                jdbconsole.error("Actualmente, la API está caída. Espere mientras se intenta reconectar con la API...")
                att += 1


################################################################################################################################################################################

# Menú principal V1
def menu():
    print('Cargando')
    time.sleep(1)
    system("cls")
    if rcpConnect: RPC.update(state='En el menú', large_image=rpcImage, large_text="Código: JuanDa553", buttons=rpcBotones, start=time.time())
    print(Fore.RED + "• • • • • MENÚ • • • • •\n")
    if checkFNapiIO(JuandaFortUser, fnapikey):
        print(Fore.CYAN + '(1) • Tienda Diaria')
        print(Fore.CYAN + '(2) • Items OG de hoy')
        print(Fore.CYAN + '(3) • Secciones de Tienda\n')
    elif checkFNapiIO(JuandaFortUser, fnapikey) == False:
        print(Fore.RED + '(1) • Tienda Diaria [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.RED + '(2) • Items OG de hoy [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.CYAN + '(3) • Secciones de Tienda\n')
    elif fnapikey == '':
        print(Fore.RED + '(1) • Tienda Diaria [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.RED + '(2) • Items OG de hoy [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.CYAN + '(3) • Secciones de Tienda\n')

    if twitterConnect:
        print(Fore.GREEN + 'Twitter Conectado!')
    else:
        print(Fore.RED + f'Twitter Desconectado! ({twtConectionErrorMsg})')
    if fnapikey == '':
        print(Fore.RED + 'No se introdujo ninguna key de FortniteAPI.io')
    elif checkFNapiIO(JuandaFortUser, fnapikey):
        print(Fore.GREEN + 'FortniteAPI.io Conectado!')
    elif checkFNapiIO(JuandaFortUser, fnapikey) == False:
        print(Fore.RED + 'La key de FortniteAPI.io que se introdujo, es invalida!')

    print(''); optionChoice = input(Fore.GREEN + '>> ')

    if optionChoice == '1':
        system("cls")
        tienda()
    elif optionChoice == '2':
        system("cls")
        itemsOg()
    elif optionChoice == '3':
        system("cls")
        secciones()

    else:
        system("cls")
        menu()

# Si el bot no está en la version actual, chao pescao
if botVersion == juandaBotApiData["public"]["version"]:
    menu()
else:
    system("cls")
    jdbconsole.error('Estas usando una version antigua de JuandaBot.')
    print(Fore.CYAN + f'\nEstas usando: v{botVersion}\nLa nueva version es: v{juandaBotApiData["public"]["version"]}\n')
    jdbconsole.exitMsg()

while True: time.sleep(1)
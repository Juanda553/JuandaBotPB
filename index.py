botVersion = '1.1.1'
'''
Por favor, no edites nada de este código para que sirva todo perfectamente.
Tampoco robes ni modifiques nada del codigo. Solo para uso PROPIO.
Tampoco elimines ni edites ningun archivo de la carpeta assets para evitar errores.
Si tienes algun problema, puedes decirmelo por el Discord de JuandaBot.
Estare constantemente tratando de mejorar este programa, asi que estar algo pendiente al Discord <3
© JuanDa553 2020 • @JuandaLeaks553 | @JuanDa553YT | Juanda553#9543 
'''

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
with open ("assets/config.json", "r") as tempConfigData:
    jdbData = json.load(tempConfigData)

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
seccionesImg = jdbData["twitter"]["tweetsCuerpos"]["seccionesImagen"]

headers = {'Authorization': fnapikey}
fuente = f'assets/fuentes/Fortnite.otf'

os.system("cls")
os.system(f"TITLE JuandaBot {botVersion}")

# Comprobar version actual de JuandaBot
juandaBotAPI = requests.get('https://pastebin.com/raw/P0nLHktg').json()

if botVersion != juandaBotAPI["public"]["version"]:
    windowsBox('JuandaBot', f'La version actual de JuandaBot que estas usando, es una version antigua, estas usando actualmente la {botVersion} y la ultima version es la {juandaBotAPI["public"]["version"]}', 0)

linkDiscord = juandaBotAPI["public"]["linkDiscord"]
rpcImage = juandaBotAPI["public"]["RPC"]["RPCimage"]
rpcBotones = juandaBotAPI["public"]["RPC"]["RPCbuttons"]
JuandaFortUser = juandaBotAPI["owner"]

hoy = datetime.now(); fechaHoy = date(hoy.year, hoy.month, hoy.day)
fechaHoySTR = f"{hoy.year}-{hoy.month}-{hoy.day}"

################################################################################################################################################################################

# Autentificar con twitter
if twitterIniciar:
    try:
        print("Conectando a Twitter")
        twitterAPI = twitter.Api(consumer_key=key, consumer_secret=secret_key, access_token_key=token, access_token_secret=secret_token)
        twitterAPI.VerifyCredentials()
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
    RPC = Presence(919501199428976641)
    RPC.connect()
    RPC.update(state="Cargando...", large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones)
    rcpConnect = True
    print('Discord Conectado con éxito.')
except Exception as Error:
    rcpConectionErrorMsg = Error
    rcpConnect = False
    jdbconsole.warning('No se pudo conectar a Discord.')

################################################################################################################################################################################

def merge(metodo="tienda"):
    try:
        jdbconsole.log('Juntando Imágenes, espere un momento...')
            
        separacionX = 6
        separacionY = 6

        if metodo == "tienda": ruta = "output/tiendaHoy"
        elif metodo == "og": ruta = "output/tiendaOg"
            
        imagenesItems = [file for file in listdir(ruta)] # Array con todos las imagenes de los items
        filasColumnas = round(math.sqrt(len(imagenesItems)+0.5)) # Definir la cantidad de items por filas y columnas sacando la raiz cuadrada de la cantidad de items
        shopPng = Image.new("RGBA", ((512 + separacionX)*filasColumnas, (512 + separacionY)*filasColumnas), color=(0, 0, 0, 0)) # Creando una imagen PNG para pegar los items

        # Inicia pegando desde las separaciones establecidas
        posX = separacionX 
        posY = separacionY 
        rowCounter = 0

        # Pegando las imagenes en la imagen PNG
        for img in imagenesItems:
            item = Image.open(f"{ruta}/{img}").convert("RGBA") # Abre imagen del item

            if rowCounter >= filasColumnas: # Si el contador es mayor a la cantidad de filas y columnas
                posY += 518 # Aumentar un bloque en Y // salto de linea
                posX = 6 # X queda en el inicio de nuevo 
                rowCounter = 0 # Se reinicia el contador de la fila 

            shopPng.paste(item, (posX, posY), item) # Pega el item en la posicion establecida
            posX += 518 # Aumentar un bloque en X
            rowCounter += 1 # Amenta el contador de los items en la fila
        jdbconsole.devTest("merge F1 completo")

        # Guardando imagen PNG con todos los items
        shopPng.save("./assets/cache/items.png")
        pngX, pngY = shopPng.size
        jdbconsole.devTest("saved PNG")

        # Creando una imagen para toda la tienda con las medidas
        if metodo == "tienda":
            shopFinal = Image.new("RGBA", (pngX, pngY+590), color="#"+fondoCustomItemShop)
        elif metodo == "og":
            shopFinal = Image.new("RGBA", (pngX, pngY+181), color="#"+fondoCustomItemShop)

        xFinal, yFinal = shopFinal.size
        jdbconsole.devTest("img jpg creada")

        # Pegando la imagen de fondo personalizada
        if bgCustomImage:
            customBgImg = Image.open('assets/imgs/fondo.png').convert('RGBA')
            customBgImg = customBgImg.resize((xFinal, yFinal))
            shopFinal.paste(customBgImg, (0,0), customBgImg)
            jdbconsole.devTest("fondo puesto")

        # Pegando la imagen PNG de todos los items, en la imagen de la tienda
        if metodo == "tienda":
            shopFinal.paste(shopPng, (0, 517), shopPng)
        elif metodo == "og":
            shopFinal.paste(shopPng, (0, 108), shopPng)
        jdbconsole.devTest("png pegado al main")

        # Escribiendo en la imagen titulo, fecha y CC de JuandaBot 
        draw=ImageDraw.Draw(shopFinal)
        if metodo == "tienda":
            draw.text((xFinal/2, 44),tituloCustomItemShop,font=ImageFont.truetype(fuente,240),fill='white', anchor="mt")
            jdbconsole.devTest("titulo dibujado")
            draw.text((xFinal/2, 339),fechaHoySTR,font=ImageFont.truetype(fuente,140),fill='white', anchor="mt")
            jdbconsole.devTest("fecha dibujado")
            draw.text((xFinal-7, 458),"Generado con JuandaBot",font=ImageFont.truetype(fuente,60),fill='white', anchor="rt")
            jdbconsole.devTest("CC dibujado")
        elif metodo == "og":
            draw.text((xFinal-7, 49),"Generado con JuandaBot",font=ImageFont.truetype(fuente,60),fill='white', anchor="rt")
            jdbconsole.devTest("CC dibujado")

        # Comprimiendo imagen y guardando
        shopFinal = shopFinal.convert("RGB")

        if metodo == "tienda":
            shopFinal.save("output/tienda.jpg", quality=30)
        elif metodo == "og":
            shopFinal.save("output/itemsOg.jpg", quality=30)

        jdbconsole.log('Imagen Generada en la carpeta output!')
        input()
        merge(metodo)

        return shopFinal
    except Exception as error:
        jdbconsole.error('Hubo un error al juntar los items y crear la imagen completa')
        jdbconsole.error(error)
        jdbconsole.errTip(linkDiscord)


# Funcion - Obtener la tienda actual
def tienda():
    print(Fore.YELLOW + f"Tienda Diaria.\nLOGGER\n\n")
    if rcpConnect: RPC.update(state='Tienda de objetos BR', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())

    # Limpiando Carpeta e inicializando variables
    start = time.time()
    x = 1
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
            itemType = i["mainType"]
            itemImgUrl = i["displayAssets"][0]["full_background"]
            itemId = i["mainId"]

            # Descargando imagen del item
            itemImg = requests.get(itemImgUrl, allow_redirects=True)
            open(f'./assets/cache/{itemId}.png', 'wb').write(itemImg.content)

            itemImg = Image.open(f'./assets/cache/{itemId}.png').resize((512,512))
            imgDraw = ImageDraw.Draw(itemImg)
    
            # Comprobar días sin salir
            itemUltimaSalida = i["previousReleaseDate"]
            if itemUltimaSalida:
                a = datetime.strptime(itemUltimaSalida, '%Y-%m-%d').date()
                b = fechaHoy - a
                if b.days >= 1:
                    itemDiasSinSalir = f'{b.days} días'
                else:
                    itemDiasSinSalir = 'Nuevo!'
            else:
                itemDiasSinSalir = 'Nuevo!'

            # Dibujar nombre, precio y días sin salir en la imagen
            imgDraw.text(
                (4,487), 
                itemDiasSinSalir, 
                font=ImageFont.truetype(fuente,24), 
                fill="white"
            )

            # Guardando imagen generada completa, en orden de tipo de item
            if itemType == 'bundle':
                itemImg.save(f'./output/tiendaHoy/a{itemId}.png')
            elif itemType == "outfit":
                itemImg.save(f'./output/tiendaHoy/b{itemId}.png')
            else:
                itemImg.save(f'./output/tiendaHoy/{itemId}.png')
                
            # Eliminando la imagen vacia del cache y calculando porcentaje
            os.remove(f'./assets/cache/{itemId}.png')
            porcentaje = int(round((x/y)*100, 0))

            jdbconsole.log(f'Imagen de {i["displayName"]} generada. ({x}/{y} - {porcentaje}%)')
            x+=1
        except Exception as error:
            jdbconsole.error(f'Error al generar la imagen de {i["displayName"]}, ignorando item. - {error}')

    # Merge de la tienda pe xd
    merge("tienda")

    # Subir a Twitter en caso que esté activado + su Exception en caso de error
    if twitterConnect:
        jdbconsole.log('Subiendo a Twitter.')
        try:
            twitterAPI.PostUpdate(twtBodyTienda, media='output/tienda.jpg')
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
                twitterAPI.PostUpdate(twtBodyOg, media='output/itemsOg.jpg')
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
            if seccionesImg:
                twitterAPI.PostUpdate(twtBodySecciones+secciones, media="assets/imgs/tiendasects.jpg")
            else:
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
            time.sleep(5)

# Función Automatica - Generacionde tienda actual
def autoTienda():
    if rcpConnect: RPC.update(state='Tienda diaria AUTO', large_image=rpcImage, large_text="By: @JuanDa553YT", buttons=rpcBotones, start=time.time())
    print(Fore.YELLOW + f'Tienda Diaria - MODO AUTOMATICO.\nLOGGER\n\n')

    # Literal el print de abajo dice lo que hace este bloque de código xd x6
    jdbconsole.log("Conectando con la API")
    try:
        data1 = requests.get('https://fortniteapi.io/v2/shop?lang=es', headers=headers).json()['lastUpdate']['uid']
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
            resp2 = requests.get('https://fortniteapi.io/v2/shop?lang=es', headers=headers)
            
            if resp2:
                data2 = resp2.json()
                jdbconsole.log(f"Detectando cambios en la tienda | Intento #{att}")
                att += 1

                # Detectar si data1 y data 2 no son iguales
                if data1 != data2['lastUpdate']['uid']:
                    # Generar las nuevas secciones llamando a la funcion de secciones
                    jdbconsole.tip("Cambio de secciones!")
                    tienda()
            
            else:
                jdbconsole.error("Actualmente, la API está caída. Espere mientras se intenta reconectar con la API...")
                att += 1
            time.sleep(5)


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

        print(Fore.RED + "• • • • • Funciones Automaticas (EXPERIMENTAL / BETA) • • • • •\n")

        print(Fore.BLUE + '(4) • Tienda Diaria AUTO')
        print(Fore.BLUE + '(5) • Secciones de Tienda AUTO\n')
    elif fnapikey == '' or checkFNapiIO(JuandaFortUser, fnapikey) == False:
        print(Fore.RED + '(1) • Tienda Diaria [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.RED + '(2) • Items OG de hoy [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.CYAN + '(3) • Secciones de Tienda\n')

        print(Fore.RED + "• • • • • Funciones Automaticas (EXPERIMENTAL / BETA) • • • • •\n")

        print(Fore.RED + '(4) • Tienda Diaria AUTO [NECESITAS LA KEY DE FORTNITEAPI.IO]')
        print(Fore.BLUE + '(5) • Secciones de Tienda AUTO\n')

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

    elif optionChoice == "4":
        system("cls")
        autoTienda()
    elif optionChoice == "5":
        system("cls")
        autoSecciones()



    elif optionChoice == "devMerge":
        temp = input()
        if temp == "tienda":
            merge("tienda")
        elif temp == "og":
            merge("og")
    else:
        system("cls")
        menu()

# Si el bot no está en la version actual, chao pescao
if botVersion == juandaBotAPI["public"]["version"]:
    menu()
else:
    system("cls")
    jdbconsole.error('Estas usando una version antigua de JuandaBot.')
    print(Fore.CYAN + f'\nEstas usando: v{botVersion}\nLa nueva version es: v{juandaBotAPI["public"]["version"]}\n')
    jdbconsole.exitMsg()

while True: time.sleep(1)
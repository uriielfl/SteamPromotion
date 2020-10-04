import requests
from bs4 import BeautifulSoup 
import sqlite3 
import re
import threading
from os import system
from time import sleep


##DB
con = sqlite3.connect("ourdata.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ourgames(gamename TEXT, gameurl TEXT, gameactualprice TEXT, gametrigger TEXT)")
con.commit()
##Menu/Requests/BS4



def AddIt():
    system('cls')
    url = str(input("URL do jogo:\n"))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    gamename = soup.find(class_="apphub_AppName")
    #formatação de texto chata
    #Boring text formatting
    gamename = str(gamename.get_text).replace('<bound method Tag.get_text of <div class="apphub_AppName">','').replace('</div>>','')
    confirmGamename = str(input("O nome do jogo é {}?\n s - Sim/Yes\n n - Não/No \n".format(gamename)))    
    if confirmGamename == "S" or confirmGamename == "s":
        gameactualprice = soup.find(class_='game_purchase_price')
        gameactualprice = re.sub('\D', '', str(gameactualprice))  
        halfStrprice = len(gameactualprice)/2
        gameactualprice = gameactualprice[:-int(halfStrprice)]
        gameactualpricev = gameactualprice[:int(halfStrprice)-2]+','+gameactualprice[int(halfStrprice)-2:]    
        gameactualpricep = gameactualprice[:int(halfStrprice)-2]+'.'+gameactualprice[int(halfStrprice)-2:]         
        gametrigger = float(input("Atualmente o jogo '"+str(gamename)+"' está custando R$"+str(gameactualpricev)+". Você quer que o valor esteja abaixo de quanto para ser avisado?\nExemplo de entrada: 9.00\nSe o jogo custar R$15,35, quando estiver abaixo de R$9,00, você será notificado.\n"))
        gameactualprice = gameactualprice[:int(halfStrprice)-2]+''+gameactualprice[int(halfStrprice)-2:]  

        #Here's our clean variables. / Aqui estão nossas variáveis limpas        
        #Adding this product to our db. Vamos adicionar o produto ao nosso banco de dados
        cur.execute("INSERT INTO ourgames VALUES('"+str(gamename)+"','"+str(url)+"','"+str(gameactualpricep)+"','"+str(gametrigger)+"')")
        con.commit()
        print("Jogo adicionado com sucesso!")
        sleep(2)
        system('cls')
        wantToExit = str(input("1 - Voltar ao Menu\n0 - Sair\n"))
        if wantToExit == "1":
            Menu()
        else:
            exit()
    else:
        exit()
   
def CheckIt():
    system('cls')
    print("Para voltar ao menu, pressione 'Ctrl+C'")
    try:
        while True:
            system('cls')
            cur.execute("SELECT * FROM ourgames") #Select our games in our db/ Selecione os nossos jogos em nosso banco de dados.
            con.commit()               
            for i in cur:             
                r = requests.get(str(i[1])) #Let's check how much for the game right now / Vamos ver o quanto está custando agora.
                soup = BeautifulSoup(r.text, "html.parser")
                gameactualprice = soup.find(class_='game_purchase_price')
                gameactualprice = re.sub('\D', '', str(gameactualprice))  #I really hate this formatting. / Eu realmente odeio essa formatação.
                halfStrprice = len(gameactualprice)/2
                gameactualprice = gameactualprice[:-int(halfStrprice)]
                gameactualpricep = gameactualprice[:int(halfStrprice)-2]+'.'+gameactualprice[int(halfStrprice)-2:]   
                if float(gameactualpricep) < float(i[3]): #If the price now is less than our trigger: / Se o precio agora for menor do que o nosso gatilho:
                    #Game in promotion!!!! / Jogo na promoção!!!
                    print("O jogo "+str(i[0])+" entrou na promoção! Quando você adicionou ele na sua lista, ele custava "+str(i[2])+" e o gatilho foi configurado para disparar quando ele chegasse em "+str(i[3])+". Atualmente ele está custando: "+str(gameactualpricep)+"")           
                else:
                    pass
    except KeyboardInterrupt: #Let's back to our menu!!! / Vamos voltar ao menu.
        Menu()

    t = threading.Thread(target=CheckIt).start() #Let's put it on a Thread, please! We want performance! / Vamos por isso em uma Thread, queremos performance!
    
def Menu():
    system('cls')
    menu = str(input("Menu:\n1 - Adicionar um jogo na lista\n2 - Checar promoções\n"))
    if menu == "1":
        AddIt()

    if menu == "2":
        CheckIt()

Menu()

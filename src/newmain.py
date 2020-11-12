import requests
from bs4 import BeautifulSoup 
import sqlite3 
import re
import threading
from os import system
from time import sleep
from PySide2.QtWidgets import (
    QMessageBox, QDialog, QMessageBox,
    QVBoxLayout, QLabel, QLineEdit
)
from PySide2 import QtGui


## DB
## SOCORRO!! lembra o tamnho dessas linhas?? kkk

con = sqlite3.connect("ourdata.db")
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS ourgames(
    gamename TEXT,
    gameurl TEXT,
    gameactualprice TEXT,
    gametrigger TEXT
    )
    """
)
con.commit()

## Menu/Requests/BS4

def AddIt(**kwargs):    
    def dialog():
        def retorno():
            global gametrigger
            gametrigger = gam.text()
            if gametrigger == '':
                gametrigger = '0'
            app.close()
        
        app = QDialog(kwargs['master'])
        lab = QLabel(
            f'''
            Atualmente o jogo <a href="{url}"><h3 style="color: green;
            background-color: rgba(0, 0, 0, 100);
            text-align: center; padding: 10px;">{gamename}</h3></a> está custando 
            <h3 style="color: red; background-color: rgba(0, 0, 0, 100); text-align: center;
            padding: 5px; border-radius: 10px;">R${gameactualpricev}.</h3>
            <p>Você quer que o valor esteja abaixo de quanto para ser avisado?<br> 
            Exemplo de entrada: 9.00 Se o jogo custar R$15,35 quando estiver<br>
            abaixo de R$9,00, você será notificado</p>
            '''
        )
        gam = QLineEdit(app)
        gam.setPlaceholderText('Pressione <Enter> para confirmar...')
        gam.returnPressed.connect(retorno)
        gra = QVBoxLayout(app)
        gra.addWidget(lab)
        gra.addWidget(gam)
        app.exec_()
    try:
        url = (kwargs['master'].pesquisa.text())
        if 'https://store.steampowered.com/app/' not in url:
            QMessageBox.warning(
            kwargs['master'], 'Erro',
            "A URL precisa ser de uma pagina de jogo Steam",
            QMessageBox.StandardButton.Ok
            )
            return
        kwargs['master'].pesquisa.clear()
        r = requests.get(url)
    except:
        QMessageBox.warning(
            kwargs['master'], 'ERRO', 'Insira uma URL Válida!',
            QMessageBox.StandardButton.Ok
        )
        return
    
    soup = BeautifulSoup(r.text, "html.parser")
    gamename = soup.find(class_="apphub_AppName")
    
    # formatação de texto chata
    # Boring text formatting
    
    gamename = str(gamename.get_text).replace(
        '<bound method Tag.get_text of <div class="apphub_AppName">'
        ,'').replace('</div>>',''
    )
    confirmGamename = QMessageBox.question(
        kwargs['master'], 'Confirmar',
        'O nome do jogo é {}?'.format(gamename),
        QMessageBox.StandardButton.Yes,
        QMessageBox.StandardButton.No
    )     
    if confirmGamename == 16384:
        gameactualprice = soup.find(class_='game_purchase_price')
        gameactualprice = re.sub('\D', '', str(gameactualprice))
        
        #  Não permitindo o cadastro de jogos gratis

        if gameactualprice == '':
            mesg = QMessageBox(kwargs['master'])
            pix = QtGui.QPixmap('img/header_image.png')
            mesg.setIconPixmap(pix)
            mesg.setMinimumSize(300, 200)
            mesg.setWindowTitle('O jogo esta gratis')
            mesg.setText('O jogo já está grátis corre e aproveita!!!')
            mesg.exec_()
            return
        
        halfStrprice = len(gameactualprice)/2
        gameactualprice = gameactualprice[:-int(halfStrprice)]
        gameactualpricev = gameactualprice[
            :int(halfStrprice)-2]+','+gameactualprice[int(halfStrprice)-2:]    
        gameactualpricep = gameactualprice[
            :int(halfStrprice)-2]+'.'+gameactualprice[int(halfStrprice)-2:]        
        gameactualprice = gameactualprice[
            :int(halfStrprice)-2]+''+gameactualprice[int(halfStrprice)-2:]
        
        # chama o dialogo para confirmar o nome do jogo
        dialog()   

        # Here's our clean variables. / Aqui estão nossas variáveis limpas        
        # Adding this product to our db. Vamos adicionar o produto ao nosso banco de dados
        # Sim pular linhas tambem é bom eheheheehhe 
        
        cur.execute(
            "INSERT INTO ourgames VALUES (?, ?, ?, ?)", [
                gamename,
                url,
                gameactualpricep,
                gametrigger
            ]
        )
        con.commit()
        QMessageBox.information(
            kwargs['master'], 'sucesso', "Jogo adicionado com sucesso!",
            QMessageBox.StandardButton.Ok
        )
        return
    else:
        QMessageBox.information(
            kwargs['master'], 'Desconhecido',
            "Desculpe, não sei o que houve",
            QMessageBox.StandardButton.Ok
        )
        return
   
def CheckIt(**kwargs):
    kwargs['master'].notification.clear()
    
    # Selecione os nossos jogos em nosso banco de dados.

    cur.execute("SELECT * FROM ourgames")
    con.commit()               
    for i in cur:
        print(i)   
        
        # Let's check how much for the game right now 
        # Vamos ver o quanto está custando agora.
        
        r = requests.get(str(i[1])) 
        soup = BeautifulSoup(r.text, "html.parser")
        gameactualprice = soup.find(class_='game_purchase_price')
        
        # I really hate this formatting.
        # Eu realmente odeio essa formatação.

        gameactualprice = re.sub('\D', '', str(gameactualprice)) 
        halfStrprice = len(gameactualprice)/2
        gameactualprice = gameactualprice[:-int(halfStrprice)]
        gameactualpricep = gameactualprice[
            :int(halfStrprice)-2]+'.'+gameactualprice[int(halfStrprice)-2:]   
        
        # If the price now is less than our trigger:
        # Se o precio agora for menor do que o nosso gatilho:
        
        if float(gameactualpricep) < float(i[3]): 
            
            # Game in promotion!!!!
            # Jogo na promoção!!!

            kwargs['master'].notification.addItem(
                f'''O jogo {i[0]} \nentrou na promoção! de {i[
                2]}\nestá por {gameactualpricep}. A sua meta era de {i[
                3]}\n{"+" * 40}\n''')
            kwargs['master'].remove.setVisible(True)
            return
        else:
            continue
    QMessageBox.information(
        kwargs['master'], 'Nada disponivel',
        "Não há nada com um preço aceitável no momento",
        QMessageBox.StandardButton.Ok
    )

# remove jogos cadastrados

def RemoveIt(**kwargs):
    listGames = cur.execute("SELECT * FROM ourgames")
    gameName = kwargs['master'].notification.currentItem().text()
    index = gameName.index('\n')
    gameNameFilter = gameName[7:index]
    cur.execute(
        'DELETE FROM ourgames WHERE gamename=(?)',
        [gameNameFilter.strip()]
    )
    con.commit()
    CheckIt(master=kwargs['master'])

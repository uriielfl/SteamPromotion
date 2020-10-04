# SteamPromotion
Create a list of games that you wish on Steam and be notified when the price get less than you want.
![List](https://i.imgur.com/ztjWMVh.png)

## Simple Menu:
![menu](https://i.imgur.com/WaFxO9g.png)
## Add URL:
![addurl](https://i.imgur.com/VHjRRjK.png)

## If you choose 2:

```python
        while True:            
            cur.execute("SELECT * FROM ourgames") #Select our games in our db/ Selecione os nossos jogos em nosso banco de dados.
            con.commit()               
            for i in cur:             
                r = requests.get(str(i[1])) #Let's check how much for the game right now / Vamos ver o quanto está custando agora.
                soup = BeautifulSoup(r.text, "html.parser")
                gamecurrentprice = soup.find(class_='game_purchase_price')
                gamecurrentprice = re.sub('\D', '', str(gamecurrentprice))  #I really hate this formatting. / Eu realmente odeio essa formatação.
                halfStrprice = len(gamecurrentprice)/2
                gamecurrentprice = gamecurrentprice[:-int(halfStrprice)]
                gamecurrentpricep = gamecurrentprice[:int(halfStrprice)-2]+'.'+gamecurrentprice[int(halfStrprice)-2:]   
                if float(gamecurrentpricep) < float(i[3]): #If the price now is less than our trigger: / Se o precio agora for menor do que o nosso gatilho:
                    #Game in promotion!!!! / Jogo na promoção!!!
                    system('cls')
                    print("O jogo "+str(i[0])+" entrou na promoção! Quando você adicionou ele na sua lista, ele custava "+str(i[2])+" e o gatilho foi configurado para disparar quando ele chegasse em "+str(i[3])+". Atualmente ele está custando: "+str(gamecurrentpricep)+"")           
                    sleep(2)  
                
```
![promotion](https://i.imgur.com/P31mwkr.png)

import random
import streamlit as st

st.title('Antes e depois do Jackpot')
form = st.form("my_form")
number = form.number_input('Quantidade de jogadores do torneio: ',step=1)
buyin = form.number_input('Qual o valor do Buy in: ',step=1)
games = form.number_input('Quantidade de jogos a simular: ',step=1)
fee = form.number_input('Qual o valor do fee para jackpot: ',step=1)
n_prob = form.number_input('Qual o numerador da probabilidade para o mega bounty: ',step=1)
d_prob = form.number_input('Qual o denominador da probabilidade para o mega bounty: ',step=1)
mega_bounty = form.number_input('Qual o valor do mega bounty: ',step=1)
but = form.form_submit_button("Simular")

if but:
    percent = games/100
    total_prizes = []
    total_wins = []
    total_new_prizes = []
    total_jackpots = []
    count = 0
    my_bar = st.progress(0)
    for j in range(1,games):
        jackpot = 0
        # create championship
        players = []
        bounty = []
        trues = []
        prize = []


        for i in range(number):
            players.append(i)
            bounty.append(buyin)
            trues.append(True)
            prize.append(0)

        bounties = dict(zip(players,bounty))
        lives = dict(zip(players,trues))
        prizes = dict(zip(players,prize))
        wins = dict(zip(players,prize))
        new_prizes = dict(zip(players,prize))
        jackpots = dict(zip(players,prize))

        sorteio = []
        for i in range(1,150):
            sorteio.append(0.006)
        for i in range(1,44):
            sorteio.append(0.0125)
        for i in range(1,5):
            sorteio.append(0.05)
        for i in range(0,1):
            sorteio.append(0.1)


        # select my player
        my_player = random.randint(0,number-1)

        # select K.O.
        while True:
            possible_players = dict(filter(lambda val: val[1] == True, lives.items()))
            if len(possible_players) > 1:
                p1 = random.randint(0,len(possible_players)-1)
                p2 = random.randint(0,len(possible_players)-1)
                p1 = list(possible_players.keys())[p1]
                p2 = list(possible_players.keys())[p2]
                sorted = random.randint(0,1)
                jack = random.randint(1,100)
                if sorted == 0:
                    lives[p2] = False
                    prizes[p1] = prizes[p1] + bounties[p2]/2
                    new_prizes[p1] = new_prizes[p1] + bounties[p2]/2 - fee
                    bounties[p1] = bounties[p1] + bounties[p2]/2
                    bounties[p2] = 0
                    wins[p1] =  wins[p1] + 1
                    jackpot = jackpot + fee
                    if jack == 1:
                        number1 = random.randint(0,len(sorteio)-1)
                        n=round(d_prob/n_prob)
                        rand_bool=random.randint(0,n*n-1)%n==0
                        if rand_bool == True:
                            new_prizes[p1] = new_prizes[p1] + mega_bounty
                            jackpots[p1] = jackpots[p1] + mega_bounty
                        else:
                            new_prizes[p1] = new_prizes[p1] + jackpot*sorteio[number1]
                            jackpot = jackpot - jackpot*sorteio[number1]
                            jackpots[p1] = jackpots[p1] + jackpot*sorteio[number1]
                        
                else:
                    lives[p1] = False
                    prizes[p2] = prizes[p2] + bounties[p1]/2
                    new_prizes[p2] = new_prizes[p2] + bounties[p1]/2 - fee
                    bounties[p2] = bounties[p2] + bounties[p1]/2
                    bounties[p1] = 0
                    wins[p2] =  wins[p2] + 1
                    jackpot = jackpot + fee
                    if jack == 1:
                        number1 = random.randint(0,len(sorteio)-1)
                        n=round(d_prob/n_prob)
                        rand_bool=random.randint(0,n*n-1)%n==0
                        if rand_bool == True:
                            new_prizes[p2] = new_prizes[p2] + mega_bounty
                            jackpots[p2] = jackpots[p2] + mega_bounty
                        else:
                            new_prizes[p2] = new_prizes[p2] + jackpot*sorteio[number1]
                            jackpot = jackpot - jackpot*sorteio[number1]
                            jackpots[p2] = jackpots[p2] + jackpot*sorteio[number1]
            else:
                break
            if lives[my_player] == False:
                break
        total_prizes.append(prizes[my_player])
        total_wins.append(wins[my_player])
        total_new_prizes.append(new_prizes[my_player])
        total_jackpots.append(jackpots[my_player])
        my_bar.progress(round(j/percent))

    st.subheader('Resultados')
    st.write('Total gasto com buyin R$ '+str(games*buyin))
    st.write('Total prizes R$ '+str(round(sum(total_prizes),2)))
    st.write('Total new prizes R$ '+str(round(sum(total_new_prizes),2)))
    st.write('Total em jackpots R$ '+str(round(sum(total_jackpots),2)))
    st.write('Diferança prizes R$ '+str(round(sum(total_new_prizes)-sum(total_prizes),2)))
    st.write('Média prizes R$ '+str(round(sum(total_prizes)/games,2))) 
    st.write('Média KOs por partida '+str(sum(total_wins)/games))

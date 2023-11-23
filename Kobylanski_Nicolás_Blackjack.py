#Importo las "libraries" correspondientes.
import random
import time

#Creo las variables globales de las cartas y la baraja.
spades = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
diamonds = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
hearts = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
clubs = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}

spades_original = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
diamonds_original = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
hearts_original = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
clubs_original = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}

full_deck = [spades, diamonds, hearts, clubs]
full_deck_original = [spades_original, diamonds_original, hearts_original, clubs_original]

def take_card():
    """
    Defino la variable de coger una carta de la baraja, además de comprobar
    si cualquiera de los diccionarios está vacio, para así volver a llenarlo.
    """
    if any(not j for j in full_deck):
        for i in range(len(full_deck)):
            full_deck[i] = full_deck_original[i]
        print("Shuffling the deck...\n")
        time.sleep(1)
    deck = random.choice(full_deck)
    card = random.choice(list(deck))
    random_value = deck.pop(card, None)
    return random_value

def play_again():
        """
        Defino la variable de rejugabilidad.
        """
        replay = input("Do you wish to play again? y for yes n for no: ")
        print(" ")
        while True:
            if replay == "y":
                game(is_replay=True)
                break
            elif replay == "n":
                print("Thanks for playing.")
                quit()
            else:
                replay = input("Please type a valid input. y/n: ")

def game(is_replay=False):
    """
    Defino la función principal que contiene todo el juego.
    """
    dealer_fcard = take_card()
    dealer_scard = take_card()
    user_fcard = take_card()
    user_scard = take_card()

    dealer_hand = [dealer_fcard, dealer_scard]
    user_hand = [user_fcard, user_scard]

    def split():
        """
        Defino una variable secundaria que se encarga de dividir las manos si las dos
        cartas de origen son iguales. Tiene la misma funcionalidad que en el blackjack real.
        """
        first_user_hand = [user_fcard]
        second_user_hand = [user_scard]

        #Aparece el equivalente a una "pantalla de carga" mientras decides que hacer con cada mano.
        print("\nSplitting your first hand...\n")
        new_fcard = take_card()
        first_user_hand.append(new_fcard)
        print(f"Your first hand is a {user_fcard} and a {new_fcard}. You have {sum(first_user_hand)}.")
        ask_card(first_user_hand, is_split=True)

        print("\nSplitting your second hand...\n")
        new_scard = take_card()
        second_user_hand.append(new_scard)
        print(f"Your first hand is a {user_scard} and a {new_scard}. You have {sum(second_user_hand)}.")
        ask_card(second_user_hand, is_split=True)

        add_card(is_split=True)

        #Condiciones de victoria una vez divididas las manos.
        if sum(first_user_hand) <= 21 and sum(second_user_hand) <= 21 and sum(first_user_hand) > sum(dealer_hand) and sum(second_user_hand) > sum(dealer_hand):
            print(f"\nYou won both hands with a {sum(first_user_hand)} and a {sum(second_user_hand)}. Dealer had a {sum(dealer_hand)}.")
            play_again()
        elif sum(first_user_hand) <= 21 and sum(first_user_hand) > sum(dealer_hand):
            print(f"\nYou won your first hand with a {sum(first_user_hand)} and busted the second one. Dealer had a {sum(dealer_hand)}.")
            play_again()
        elif sum(second_user_hand) <= 21 and sum(second_user_hand) > sum(dealer_hand):
            print(f"\nYou won your second hand with a {sum(second_user_hand)} and busted the first one. Dealer had a {sum(dealer_hand)}.")
            play_again()
        else:
            print("\nYou lost both hands.")
            play_again()
            
    def ask_card(hand, is_split=False):
        """
        Defino la función secundaria de pedir carta del usuario y dentro establezco 
        una serie de normas para que la carta del "As" valga 1 o 11, en su 
        correspondiente caso. 
        """
        ask = int(input("Do you want to ask or stay? 1 to ask 2 to stay: "))
        while True:
            if ask == 1:
                new_card = take_card()
                if new_card == 11:
                    if new_card + sum(hand) > 21:
                        new_card = 1
                    elif new_card + sum(hand) < 21:
                        new_card = 11
                hand.append(new_card)
                if sum(hand) > 21 and is_split == False:
                    print(f"You got a {new_card}. You busted.")
                    play_again()
                if sum(hand) > 21 and is_split == True:
                    print(f"You got a {new_card}. You busted your hand.\n")
                    break
                elif sum(hand) < 21:
                    ask = int(input(f"You got a {new_card}. You have a {sum(hand)}. Do you want to ask or stay? "))
                else:
                    print(f"You got {new_card}. You have 21, blackjack.")
                    break
            elif ask == 2:
                break
            else:
                break

    def add_card(is_split=False):
        """
        Defino la función secundaria de añadir una carta a la mano del croupier obedeciendo 
        las normas del blackjack; si la suma de sus cartas es menor a 17 debe pedir carta, 
        si es igual o mayor, se planta.
        """
        print(f"Dealer's second card is {dealer_scard}. He has {sum(dealer_hand)}.")
        while sum(dealer_hand) < 21:
            if sum(dealer_hand) < 17:
                new_card = take_card()
                if new_card == 11:
                    if new_card + sum(dealer_hand) > 21:
                        new_card = 1
                    elif new_card + sum(dealer_hand) < 21:
                        new_card = 11
                if is_split == False:
                    if new_card + sum(dealer_hand) == 21 and sum(user_hand) != 21:
                        print(f"Dealer took a {new_card} and has blackjack. You lose.")
                        play_again()
                    elif new_card + sum(dealer_hand) > 21:
                        print(f"Dealer took a {new_card}. He busted with {new_card + sum(dealer_hand)}, you win.")
                        play_again()
                elif is_split == True:
                    if new_card + sum(dealer_hand) == 21:
                        print(f"Dealer took a {new_card} and has blackjack.")
                        break
                    elif new_card + sum(dealer_hand) > 21:
                        print(f"Dealer took a {new_card}. He busted with {new_card + sum(dealer_hand)}, you win.")
                        play_again()
                print(f"Dealer took a {new_card}. He has {sum(dealer_hand) + new_card}.")
                time.sleep(1)
                dealer_hand.append(new_card)
            else:
                break
    
    #Se define el comienzo del juego teniendo en cuenta la variable de rejugabilidad.
    if is_replay == False:
        print(f"Welcome to the Blackjack table!\n \nDealer first card is {dealer_fcard}.")
    else:
        print(f"Dealer first card is {dealer_fcard}.")

    if sum(dealer_hand) == 21 and sum(user_hand) != 21:
        print(f"Your cards are {user_fcard} and {user_scard}. You have {user_fcard + user_scard}.")
        print(f"Dealer second card is {dealer_scard}. He has blackjack, you lose.")
        play_again()

    #Se definen aquí también la mayoría de condiciones de victoria del juego.
    print(f"Your cards are {user_fcard} and {user_scard}. You have {user_fcard + user_scard}.")
    if user_fcard == user_scard:
        split_choice = int(input("You have 2 equal cards. Do you wish to split? 1 to split, any other key to continue: "))
        if split_choice == 1:
            split()
        else:
            if sum(user_hand) == 21:
                add_card()
            else:
                ask_card(user_hand)
                add_card()
                if sum(dealer_hand) > sum(user_hand):
                    print(f"Dealer got {sum(dealer_hand)} and you got {(sum(user_hand))}. You lose.")
                elif sum(dealer_hand) < sum(user_hand):        
                    print(f"Dealer got {sum(dealer_hand)} and you got {(sum(user_hand))}. You win.")
                else:
                    print(f"You both got {sum(dealer_hand)}. It's a draw.")
                play_again()
    else:
        if sum(user_hand) == 21:
            add_card()
        else:
            ask_card(user_hand)
            add_card()
        if sum(dealer_hand) > sum(user_hand):
            print(f"Dealer got {sum(dealer_hand)} and you got {(sum(user_hand))}. You lose.")
        elif sum(dealer_hand) < sum(user_hand):        
            print(f"Dealer got {sum(dealer_hand)} and you got {(sum(user_hand))}. You win.")
        else:
            print(f"You both got {sum(dealer_hand)}. It's a draw.")
        play_again()
    
#Llamo la función.
if  __name__ == "__main__":
    game()

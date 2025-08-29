import os
import random
from collections import namedtuple
import copy
import time
import tkinter as tk

import keyboard
import show_game
import sidepots

Card = namedtuple('Card', ['num_value','face_value', 'suit'])


def shuffle(input_deck):
    output_deck = copy.copy(input_deck)
    num_cards = len(output_deck)
    for i in range(num_cards):
        random_index = random.randint(0, num_cards)
        tmp_card_holder = output_deck[i]
        output_deck[i] = output_deck[random_index]
        output_deck[random_index] = tmp_card_holder
    return output_deck

import random

def machine_shuffle(deck, passes=5, bins=5, seed=None):
    """
    Simulates an MD3-style batch shuffle.
    
    Args:
        deck (list): The input deck (e.g., list of cards or numbers).
        passes (int): Number of interleave passes to simulate.
        bins (int): Number of intermediate stacks to split into.
        seed (int or None): Optional seed for reproducibility.
        
    Returns:
        list: The shuffled deck.
    """
    if seed is not None:
        random.seed(seed)
    
    deck = deck[:]  # Copy to avoid modifying original
    
    for _ in range(passes):
        # Split deck into N bins randomly
        bin_decks = [[] for _ in range(bins)]
        for card in deck:
            chosen_bin = random.randint(0, bins - 1)
            bin_decks[chosen_bin].append(card)
        
        # Interleave the bins randomly
        merged_deck = []
        bin_indices = [0] * bins  # Pointers to current card in each bin
        
        while any(bin_indices[i] < len(bin_decks[i]) for i in range(bins)):
            # Choose a non-empty bin at random
            non_empty_bins = [i for i in range(bins) if bin_indices[i] < len(bin_decks[i])]
            chosen_bin = random.choice(non_empty_bins)
            # Pull next card from that bin
            merged_deck.append(bin_decks[chosen_bin][bin_indices[chosen_bin]])
            bin_indices[chosen_bin] += 1
        
        deck = merged_deck  # For next pass

    return deck


def make_deck(suits, face_values, num_values):
    output_deck = []
    for face_and_num_idx in range(len(face_values)):
        for suit in suits:
            output_deck.append(Card(num_values[face_and_num_idx], face_values[face_and_num_idx], suit))
    # for value_idx in face_chars:
    #     for suit in suits:
    #         output_deck.append(Card(value, suit))
    return output_deck

def insert_cut_card(deck):
    lower_bound = int(len(deck) * .65)
    upper_bound = int(len(deck) * .80)
    position = random.randint(lower_bound, upper_bound)
    deck.insert(position, Card('CUT', 'CUT', 'CUT'))


# def main_menu()
def deal_card(game_deck):
    delt_card = game_deck.pop()
    if delt_card.num_value == "CUT":
        return False
    return delt_card

def handle_key(event):
        if event.event_type != 'down':
            return
        return event.name

def nat_bj(hand):
    if (hand[0].num_value == '10' and hand[1].num_value == '11') and (hand[1].num_value == '10' and hand[0].num_value == '11'):
        return True
    return False

def contains_unmodified_ace(hand):
    print(hand)
    for index, card in enumerate(hand):
        if card.num_value == '11' and card.face_value == 'A':
            hand[index] = Card('1', card.face_value, card.suit)
            return True
    return False

def dealer_hit_huh(dealer_hand):
    dealer_sum = sum(map(lambda x: int(x.num_value), dealer_hand))
    if dealer_sum > 21:
        if contains_unmodified_ace(dealer_hand):
            return True
        else:
            return False
    dealer_face = map(lambda x: x.face_value, dealer_hand)
    if dealer_sum == 17 and 'A' in dealer_face:
        for card in dealer_hand:
            if card.num_value == '11':
                return True
        return False
    elif dealer_sum >= 17:
        return False
    return True        

def flush_input():
    import msvcrt
    while msvcrt.kbhit():
        msvcrt.getch()

def play_game(game_deck, buster_on, lucky_on):
    cut_card = False
    bal = 100
    while bal > 0 and not cut_card:
        print("bet ammount: ")
        bet = int(input())
        if lucky_on:
            print("lucky ammount: ")
            lucky = int(input())
        if buster_on:
            print("buster bet:")
            buster = int(input())
        show_game.clear_terminal()
        dealer_hand = []
        player_hand = [[]]

        # player 1
        draw_card = deal_card(game_deck)
        if draw_card == False:
            draw_card = deal_card(game_deck)
            cut_card = True
        player_hand[0].append(draw_card)
        show_game.show_table(player_hand, dealer_hand)

        # dealer 1 (dont show)
        draw_card = deal_card(game_deck)
        if draw_card == False:
            draw_card = deal_card(game_deck)
            cut_card = True
        dealer_hand.append(draw_card)
        show_game.show_table(player_hand, dealer_hand, hide_first_card=True)

        # player 2
        draw_card = deal_card(game_deck)
        if draw_card == False:
            draw_card = deal_card(game_deck)
            cut_card = True
        player_hand[0].append(draw_card)
        show_game.show_table(player_hand, dealer_hand, hide_first_card=True)


        # dealer 2
        draw_card = deal_card(game_deck)
        if draw_card == False:
            draw_card = deal_card(game_deck)
            cut_card = True
        dealer_hand.append(draw_card)
        show_game.show_table(player_hand, dealer_hand, hide_first_card=True)
        split = show_game.show_controls(player_hand[0])
        
        # check for natural blackjacks on either side
        if nat_bj(player_hand[0]) and not nat_bj(dealer_hand):
            print("The player wins!")
            time.sleep(0.5)
            continue
        if nat_bj(dealer_hand):
            print("Dealer Wins :<")
            time.sleep(0.5)
            continue 

        # main control loop
        player_sum = sum(map(lambda x: int(x.num_value), player_hand[0]))
        print("sum: ", player_sum)
        continue_huh = True
        is_first_move = True
        current_hand = 0
        while continue_huh:
            show_game.show_table(player_hand, dealer_hand, hide_first_card=True)
            show_game.show_controls(player_hand[current_hand], is_first_move)
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if key == 'f':
                    draw_card = deal_card(game_deck)
                    if draw_card == False:
                        draw_card = deal_card(game_deck)
                        cut_card = True
                    player_hand[current_hand].append(draw_card)
                    player_sum = sum(map(lambda x: int(x.num_value), player_hand[current_hand]))
                    if player_sum > 21:
                        if not contains_unmodified_ace(player_hand[current_hand]):
                            continue_huh = False
                        else:
                            player_sum -= 10
                    show_game.show_table(player_hand, dealer_hand, hide_first_card=True)
                    show_game.show_controls(player_hand[current_hand], is_first_move)    
                    print("sum: ", player_sum)
                    if player_sum > 21:
                        print("Player Bust!")
                        if len(player_hand) > current_hand + 1:
                            current_hand += 1
                            draw_card = deal_card(game_deck)
                            if draw_card == False:
                                draw_card = deal_card(game_deck)
                                cut_card = True
                            player_hand[current_hand].append(draw_card)
                            continue_huh = True
                            is_first_move = True
                elif key == 'j':
                    time.sleep(.5)
                    if len(player_hand) > current_hand + 1:
                        show_game.show_table(player_hand, dealer_hand, hide_first_card=True)
                        current_hand += 1
                        draw_card = deal_card(game_deck)
                        if draw_card == False:
                            draw_card = deal_card(game_deck)
                            cut_card = True
                        player_hand[current_hand].append(draw_card)
                        continue_huh = True
                        is_first_move = True
                    else:
                        show_game.show_table(player_hand, dealer_hand, hide_first_card=False)
                        if current_hand + 1 == len(player_hand) and dealer_hit_huh(dealer_hand):
                            dealer_hit = True
                            while dealer_hit:
                                draw_card = deal_card(game_deck)
                                if draw_card == False:
                                    draw_card = deal_card(game_deck)
                                    cut_card = True
                                dealer_hand.append(draw_card)
                                time.sleep(.5)
                                show_game.show_table(player_hand, dealer_hand, hide_first_card=False)
                                dealer_hit = dealer_hit_huh(dealer_hand)
                        dealer_sum = sum(map(lambda x: int(x.num_value), dealer_hand))
                        player_sum = sum(map(lambda x: int(x.num_value), player_hand[current_hand]))
                        print("dealer sum:", dealer_sum)
                        if dealer_sum > 21 or player_sum > dealer_sum:
                            print("player wins!")
                        elif dealer_sum > player_sum:
                            print("Dealer wins")
                        else:
                            print("Push!") 
                        continue_huh = False
                    # if len(player_hand) > current_hand + 1:
                            
                            
                elif is_first_move and key == 'd':
                    draw_card = deal_card(game_deck)
                    if draw_card == False:
                        draw_card = deal_card(game_deck)
                        cut_card = True
                    player_hand[current_hand].append(draw_card)
                    player_sum = sum(map(lambda x: int(x.num_value), player_hand[current_hand]))
                    if player_sum > 21:
                        if not contains_unmodified_ace(player_hand[current_hand]):
                            continue_huh = False
                            print("Player bust")
                            if len(player_hand) > current_hand + 1:
                                current_hand += 1
                                draw_card = deal_card(game_deck)
                                if draw_card == False:
                                    draw_card = deal_card(game_deck)
                                    cut_card = True
                                player_hand[current_hand].append(draw_card)
                                continue_huh = True
                                is_first_move = True
                            else:
                                continue
                        else:
                            player_sum -= 10
                    show_game.show_table(player_hand, dealer_hand, hide_first_card=False)
                    if continue_huh and dealer_hit_huh(dealer_hand):
                        dealer_hit = True
                        while dealer_hit:
                            draw_card = deal_card(game_deck)
                            if draw_card == False:
                                draw_card = deal_card(game_deck)
                                cut_card = True
                            dealer_hand.append(draw_card)
                            time.sleep(.5)
                            show_game.show_table(player_hand, dealer_hand, hide_first_card=False)
                            dealer_hit = dealer_hit_huh(dealer_hand)
                    dealer_sum = sum(map(lambda x: int(x.num_value), dealer_hand))
                    player_sum = sum(map(lambda x: int(x.num_value), player_hand[0]))
                    print("dealer sum:", dealer_sum)
                    if dealer_sum > 21 or player_sum > dealer_sum:
                        print("player wins!")
                    elif dealer_sum > player_sum:
                        print("Dealer wins")
                    else:
                        print("Push!") 
                    continue_huh = False
                    if len(player_hand) > current_hand + 1:
                            current_hand += 1
                            draw_card = deal_card(game_deck)
                            if draw_card == False:
                                draw_card = deal_card(game_deck)
                                cut_card = True
                            player_hand[current_hand].append(draw_card)
                            continue_huh = True
                            is_first_move = True 
                    
                elif split and key == 'k':

                    split_card = player_hand[current_hand].pop()
                    player_hand.append([split_card])
                    draw_card = deal_card(game_deck)
                    if draw_card == False:
                        draw_card = deal_card(game_deck)
                        cut_card = True
                    player_hand[current_hand].append(draw_card)
                    show_game.show_table(player_hand, dealer_hand, hide_first_card=True)
                    show_game.show_controls(player_hand[current_hand])
                    # show_game.print_hand(player_hand[1])
                    # player_decks[[]]
                elif key == 'esc':
                    print("escape key pressed, returning to menu")
            flush_input()
        if not continue_huh:
            continue            

    # player bet
        # if lucky -> lucky bet
        # if buster -> buster bet
    
    # begin setup
    # deal -> player, dealer face down (blank print) player, dealer
    # if lucky & if bet -> dealer top card + 2 player cards
    # check if dealer has blackjack
        # if yes push all 21s and make everyone else loos
    
    # if player blackjack, payout end game
    
    # begin game
    # player hit/stay
    # if hit
        # draw card, check for bust function == true
            # if bust, end game, +0
        # /\ hit/stay
    # if stay
        # dealer draw
        # if sum value >= 17 and not soft 17 (is_soft_17_huh)
            # stay
        # else
            # hit
                # if bust 
                    # payout player
                    # if buster & if bet -> dealer_numcards -> payout player
                # else
                    # compare dealer hand to player hand 
        

def main():
    face_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    num_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', '11']
    suits = ['♠', '♥', '♣', '♦']
    buster_on = False
    lucky_on = False

    deck = make_deck(suits, face_values, num_values)
    deck_6 = deck * 6
    insert_cut_card(deck_6)
    game_deck = machine_shuffle(deck_6)
    # print(game_deck)
    
    user = show_game.login()
    # show_game.main_menu(user)
    play_game(game_deck, buster_on, lucky_on)
main()




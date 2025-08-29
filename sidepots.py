def same_suits_huh(cards):
    the_suit = cards[0].suit
    for card in cards:
        if card.suit != the_suit:
            return False
    return True

def check_if_value(cards, value):
    for card in cards:
        if card.value == value:
            return True
    return False

def check_if_all_value(cards, value):
    for card in cards:
        if card.value != value:
            return False
    return True

def lucky_sidepot(cards, bet):
    card_sum = cards[0].value + cards[1].value + cards[2].value
    mult = 0
    if card_sum == 19:
        mult =  2
    if card_sum == 20:
        mult = 2
    
    same_suits = same_suits_huh(cards)
    
    if card_sum == 21 and not same_suits:
        mult =  3
    if card_sum == 21 and not same_suits:
        mult =  10
    
    value_6 = check_if_value(cards, '6')
    value_7 = check_if_value(cards, '7')
    value_8 = check_if_value(cards, '8')

    exists_678 = value_6 and value_7 and value_8

    if exists_678 and not same_suits:
        mult = 30
    
    if exists_678 and same_suits:
        mult =  100
    
    all_7s_huh = check_if_all_value(cards, '7')

    if all_7s_huh and not same_suits:
        mult =  50
    
    if all_7s_huh and same_suits:
        mult =  200
    if mult == 0: 
        return 0
    return mult * bet + bet
    
def buster_payout(num_cards, bet):
    buster = {3: 2, 4: 2, 5: 4, 6: 15, 7: 50}
    if num_cards in buster:
        mult = buster[num_cards]
    elif num_cards >= 8:
        mult = 250
    return mult * bet + bet
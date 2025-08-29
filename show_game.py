

from collections import namedtuple
import copy
import os
import time
import keyboard

Card = namedtuple('Card', ['num_value','face_value', 'suit'])

number_card_template = """
╭─────────╮
│v s s s  │
│    s    │
│  s s s  │
│    s    │
│  s s s v│
╰─────────╯"""

number_cards_suits = ["00000100000", "01000000010", "01000100010", 
                      "10100000101", "10100100101", "10101010101", 
                      "10111010101", "10111010111", "10111111101",
                      "11111011111", "00000000000"]

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_table(player_hand, dealer_hand, hide_first_card=False):
    clear_terminal()
    if not dealer_hand:
        # if is empty print nothing
        print('\n\n\n\n\n\n\n')
    else:
        print_hand(dealer_hand, hide_first_card)
    print('\n\n')
    if not player_hand: 
        print('\n\n\n\n\n\n\n')
    else:
        for i in range(len(player_hand)):
            print_hand(player_hand[i])
    time.sleep(.5)

def show_controls(player_hand, is_first_turn=True, current_hand=0):
    controls_line = ''
    controls_line += "hit(f) - stay(j)"
    if is_first_turn:
        controls_line += " - double(d)"
    split = False

    if player_hand[0].num_value == player_hand[1].num_value:
        split = True
        controls_line += " - split(k)"
    print(controls_line)
    return split

def print_hand(hand, hide_first_card = False):
    display_hand = []
    for cards in hand:
        if hide_first_card:
            display_hand.append(template_to_card(Card(" ", " ", " ")))
            hide_first_card = False
        else:
            display_hand.append(template_to_card(cards))
    print_cards_same_line(display_hand)

def template_to_card(card):
    value = card.face_value
    suit = card.suit
    if value == ' ':
        pattern = number_cards_suits[-1]
    elif value == 'A' or value == 'K' or value == 'Q' or value == 'J':
        pattern = number_cards_suits[1]
    else:
        pattern = number_cards_suits[int(value)-1]
    
    if value == '10':
        template_with_num = number_card_template.replace('v ', value).replace(' v', value)
    else:
        template_with_num = number_card_template.replace('v', value)
    list_card = list(template_with_num)
    #                              \/ so janky lmao
    # pattern = number_cards_suits[int(value[-1])-1]
    pattern_counter = 0
    for index in range(len(list_card)):
        if list_card[index] == 's':
            if pattern[pattern_counter] == '1':
                list_card[index] = suit
            else:
                list_card[index] = ' '
            pattern_counter += 1
    return ''.join(list_card)
 

def print_cards_same_line(cards):
    split_cards = []
    cards_output = ""
    for card in cards:
        split_cards.append(card.split('\n')[1:])
    for i in range(len(split_cards[0])):
        cur_line = ""
        for j in range(len(split_cards)):
            cur_line += split_cards[j][i] + "  "
        cards_output += cur_line + '\n'
    print(cards_output) 


# card1 = Card('10', 'K', '♠')
# card2 = Card('10', '10', '♥')
# card3 = Card('1', '1', '♥')

# print_cards_same_line([template_to_card(card1), template_to_card(card2), template_to_card(card3)])
# print(template_to_card('♠', 'K'))

def highlight(option):
            return f"{colors.UNDERLINE}{option}{colors.ENDC}"

def create_table_menu():
    print("Create table:")
    options = ["start", "min", "max", "luc", "bus", "con", "exit"]

    start = "0"
    min = "0"
    max = "0"
    lucky = False
    buster = False
    busterOnOff = "ON " + highlight("OFF")
    luckyOnOff = "ON " + highlight("OFF")
    print(f"""
        > starting ammount: ${start}
        > minimum bet: ${min}
        > maximum bet: ${max}
        > buster: {busterOnOff}
        > lucky: {luckyOnOff}
          """)
    

def login():
    print('--Welcome to Blackjack--')
    print('Please login: ', end='')
    user = input()
    clear_terminal()
    return user.lower()

def stats_menu():
    temp = 1

class MenuState:
    def __init__(self, user):
        self.options = ['play', 'stats', 'quit']
        self.selected = 0
        self.quit_menu = False
        self.user = user

    def handle_key(self, event):
        if event.event_type != 'down':
            return

        updated = False

        if event.name == 'up':
            self.selected = (self.selected - 1) % len(self.options)
            updated = True
        elif event.name == 'down':
            self.selected = (self.selected + 1) % len(self.options)
            updated = True
        elif event.name == 'enter':
            # print(f"Selected option: {self.options[self.selected].capitalize()}")
            self.quit_menu = True
        elif event.name == 'esc':
            self.quit_menu = True

        if updated:
            self.render_menu()
    
    def render_menu(self):
        print("\033[H\033[J", end="")  # ANSI clear

        def highlight(option):
            return f"{colors.UNDERLINE}{option.capitalize()}{colors.ENDC}"

        play = highlight("play") if self.selected == 0 else "Play"
        stats = highlight("stats") if self.selected == 1 else "Stats"
        quit = highlight("quit") if self.selected == 2 else "Quit"
            
        print(f"""
         _______   __                      __           _____                      __       
        /       \\ /  |                    /  |         /     |                    /  |      
        $$$$$$$  |$$ |  ______    _______ $$ |   __    $$$$$ |  ______    _______ $$ |   __ 
        $$ |__$$ |$$ | /      \\  /       |$$ |  /  |      $$ | /      \\  /       |$$ |  /  |
        $$    $$< $$ | $$$$$$  |/$$$$$$$/ $$ |_/$$/  __   $$ | $$$$$$  |/$$$$$$$/ $$ |_/$$/ 
        $$$$$$$  |$$ | /    $$ |$$ |      $$   $$<  /  |  $$ | /    $$ |$$ |      $$   $$<  
        $$ |__$$ |$$ |/$$$$$$$ |$$ \\_____ $$$$$$  \\ $$ \\__$$ |/$$$$$$$ |$$ \\_____ $$$$$$  \\ 
        $$    $$/ $$ |$$    $$ |$$       |$$ | $$  |$$    $$/ $$    $$ |$$       |$$ | $$  |
        $$$$$$$/  $$/  $$$$$$$/  $$$$$$$/ $$/   $$/  $$$$$$/   $$$$$$$/  $$$$$$$/ $$/   $$/
                                                                                                
        Welcome back, {self.user}!                                                                               
        > {play}
        > {stats}
        > {quit}""")

def main_menu(user):
    state = MenuState(user)
    state.render_menu()
    keyboard.hook(state.handle_key, suppress=True)
    while not state.quit_menu:
        time.sleep(0.05)
    selected_options = state.options[state.selected]
    if selected_options == 'play':
        create_table_menu()
    elif selected_options == 'stats':
        stats_menu()
    keyboard.unhook_all()
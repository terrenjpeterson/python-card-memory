# implementation of card game - Memory

import simplegui
import random

CARD_HEIGHT = 100
CARD_WIDTH = 50
NUMBER_CARDS = 16

# card list attributes
#
# attribute 1 - card sequence number
# attribute 2 - current card color
# attribute 3 - flipped state
# attribute 4 - card value number
# attribute 5 - value number color
#
card_list = []

last_number_flipped = 0
current_number_flipped = 0
first_card_flipped = 0
second_card_flipped = 0
moves = 0
need_to_reflip = False

# helper function to initialize game
def init():
    global last_number_flipped, current_number_flipped, need_to_reflip, first_card_flipped, second_card_flipped, moves
# these variables are used to track matching
    last_number_flipped = 0
    current_number_flipped = 0
    first_card_flipped = 0
    second_card_flipped = 0
    moves = 0
    need_to_reflip = False
#    
# build card numbers
    numbers = range(1, (NUMBER_CARDS / 2) + 1) + range(1, (NUMBER_CARDS / 2) + 1)
    random.shuffle(numbers)
# then create the cards through a list
    for card in range(1, NUMBER_CARDS + 1):
        card_list.append([card, "Green" , False, numbers[card -1], "Green"])
    pass  

def which_card_clicked(pos):
# determine which card of the range was selected
    card = int(pos[0] / CARD_WIDTH) + 1
    return card

def flip_this_card(flipped):
# actions to take when flipping a card
    global last_number_flipped, current_number_flipped
 
    for card in card_list:
        if card[0] == flipped and not card[2]:
            card[1] = "Black"
            card[2] = True
            current_number_flipped = card[3]
            card[4] = "White"

def reflip_this_card(reflip):
# will reflip a card based on the number passed in and reset attributes
    for card in card_list:
        if card[0] == reflip:
            card[1] = "Green"
            card[2] = False
            card[4] = "Green"            
            
# define event handlers
def mouseclick(pos):
    global last_number_flipped, current_number_flipped, need_to_reflip, first_card_flipped, second_card_flipped, moves
               
    if need_to_reflip:
        # this checks a flag previously set indicating that the last two need to be reflipped
        reflip_this_card(first_card_flipped)
        first_card_flipped = 0
        reflip_this_card(second_card_flipped)
        second_card_flipped = 0
        need_to_reflip = False
        
    flipped = which_card_clicked(pos)

    flip_this_card(flipped)

    if current_number_flipped == last_number_flipped:
        # this indicates a match
        need_to_reflip = False
        last_number_flipped = 0
        first_card_flipped = 0
        second_card_flipped = 0
    else:        
        # not a match situation
        if first_card_flipped > 0:
            # failed match situation
            need_to_reflip = True
            second_card_flipped = flipped
            last_number_flipped = 0
        else:
            # first flip situation
            moves += 1
            first_card_flipped = flipped
            second_card_flipped = 0
            need_to_reflip = False            
            last_number_flipped = current_number_flipped
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for card in card_list:
        canvas.draw_polygon([(card[0] * CARD_WIDTH - 1, 0), 
                             (card[0] * CARD_WIDTH - 1, CARD_HEIGHT), 
                              ((card[0] - 1) * CARD_WIDTH + 1, CARD_HEIGHT), 
                              ((card[0] - 1) * CARD_WIDTH + 1, 0)], 
                               1, "Green", card[1])
        canvas.draw_text(str(card[3]), (card[0] * CARD_WIDTH - 35, 60), 40, card[4])
    
    label.set_text("Moves = " + str(moves))
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
init()


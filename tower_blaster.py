"""
Name: Carol Wong
This is the program for Tower Blaster, a game that involves re-arranging a group of number bricks in order to
get an increasing sequence.
"""


def instructions():
    """
    This function prints the rules of the game.
    """
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("* * * * * * * * * * * * * * * * T O W E R   B L A S T E R * * * * * * * * * * * * * * * *")
    print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("")
    print("= = = = = = = = = = = = = = = = = = = = S T A R T = = = = = = = = = = = = = = = = = = = =")
    print("Instructions: This game starts with a pile of 60 bricks, numbered 1 ~ 60.")
    print("The number on the brick represents the width of the brick.")
    print("The first player to arrange a tower of 10 bricks from smallest to biggest wins.")
    print("(i.e. numbered least to greatest.)")
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print("")


def setup_bricks():
    """
    This function creates the main pile of 60 bricks, represented as a list containing the integers 1 ~ 60.
    This function also creates a discard pile of 0 bricks, represented as an empty list.
    This function returns both lists.
    """

    main_pile = list(range(1, 61))
    discard = []
    return main_pile, discard


def shuffle_bricks(bricks):
    """
    This function shuffles the given bricks, represented as a list. This is done to start the game.
    This function does not return anything.
    """

    import random
    random.shuffle(bricks)


def check_bricks(main_pile, discard):
    """
    This function checks if there are any cards left in the given main pile of bricks.
    If not, it shuffles the discard pile and moves those bricks to the main pile.
    Then it turns over the top card to be the start of the new discard pile.
    """

    if not main_pile:
        shuffle_bricks(discard)
        main_pile.extend(discard)  # adds all items in discard into main_pile
        discard.clear()  # removes all items from discard pile
        discard.append(main_pile[0])  # adds the first item in main mile into discard pile
        main_pile.pop(0)  # remove the first item in main pile


def check_tower_blaster(tower):
    """
    Given the computer's tower or the user's tower, this function checks if stability has been achieved,
    i.e whether the bricks are in ascending order. This function returns a boolean value.
    """

    tower_copy = tower.copy()  # make a copy of a tower
    tower_copy.sort()  # sort a tower in ascending order
    if tower_copy == tower:  # check if copy of tower is equaled to tower
        return True
    else:
        return False


def get_top_brick(brick_pile):
    """
    This function removes and returns the top brick from any given pile of bricks.
    This can be from the main pile, the discard pile, player's tower or computer's tower.
    """

    top_brick = brick_pile[0]
    brick_pile.pop(0)
    return top_brick


def deal_initial_bricks(main_pile):
    """
    This function starts the game by dealing two sets of 10 bricks each, from the given main_pile.
    It follows the normal conventions of dealing. The computer is always dealt first and always plays first.
    it returns a tuple containing two lists: the user's tower and the computer's tower.
    """

    computer_tower = []
    user_tower = []
    for i in range(0, 10):  # runs this for loop 10 times
        computer_tower.insert(0, get_top_brick(main_pile))  # takes top brick from main pile, insert in computer tower
        user_tower.insert(0, get_top_brick(main_pile))  # takes top brick from main pile, insert to user tower

    return computer_tower, user_tower


def add_brick_to_discard(brick, discard):
    """
    This function adds the given brick to the top of the given discard pile.
    This function does not return anything.
    """

    discard.insert(0, brick)  # insert brick into first index of discard pile


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard):
    """
    This function finds the given brick, represented by an integer,
    to be replaced in the given tower and replaces it with the given new brick.
    It checks if the given brick to be replaced is truly a brick in the given tower.
    Then, it moves the given brick to be replaced to the top of the given discard pile.
    It returns True if the given brick is replaced, otherwise it returns False.
    """

    if brick_to_be_replaced in tower:
        identified_index = tower.index(brick_to_be_replaced)  # locates the index number for the brick in tower
        tower[identified_index] = new_brick  # assign new brick to index space
        discard.insert(0, brick_to_be_replaced)  # brick to change is inserted into beginning of discard pile
        return True
    else:
        return False


def computer_play(tower, main_pile, discard):
    """
    This function is the computer's strategy of replacing bricks.
    Given the computer's tower and top discard brick, determine whether this brick is useful,
    then determine which brick to take, and which index position to place brick.
    """
    discard_top = discard[0]

    # The computer's strategy is to 'slice' the pile of 60 bricks into 10 groups (divide by 6),
    # and based on each block's value, distribute them across 10 slots in the computer's tower.
    #
    # The computer wants to intentionally fill the beginning and end of the tower first,
    # if the top brick on the discard pile is less than 19 or more than 42, take it.
    # Take that brick's number (minus 1, as indexes start at 0) and divide it by 6,
    # that will be the index position for the brick.
    #
    # In other words, if the top discard brick is:
    # 1 ~ 6, place in 1st block position (index 0)
    # 7 ~ 12, place in 2nd block position (index 1)
    # 13 ~ 18, place in 3rd block position (index 2)
    # 19 ~ 42, don't take it. Take brick from main pile. (See strategy below)
    # 43 ~ 48, place in 8th block position (index 7)
    # 49 ~ 54, place in 9th block position (index 8)
    # 55 ~ 60, place in 10th block position (index 9)

    if discard_top < 19 or discard_top > 42:
        computer_tower_index = (discard_top - 1) // 6
        brick_to_remove = tower[computer_tower_index]
        tower[computer_tower_index] = discard_top  # Place new brick and move unwanted brick into discard.
        discard[0] = brick_to_remove
        print("The computer picked [", tower[computer_tower_index], "] from the discard pile.", sep='')
        return tower

    # If the top brick on the discard pile is between 19 and 42, then take a brick from main pile.
    # This brick (minus 1, as indexes start at 0), divided by 6, will be the index position to place it.
    #
    # If the revealed brick from main brick is:
    # 1 ~ 6, place in 1st block position (index 0)
    # 7 ~ 12, place in 2nd block position (index 1)
    # 13 ~ 18, place in 3rd block position (index 2)
    # 19 ~ 24, place in 4th block position (index 3)
    # 25 ~ 30, place in 5th block position (index 4)
    # 31 ~ 36, place in 6th block position (index 5)
    # 37 ~ 42, place in 7th block position (index 6)
    # 43 ~ 48, place in 8th block position (index 7)
    # 49 ~ 54, place in 9th block position (index 8)
    # 55 ~ 60, place in 10th block position (index 9)
    # The computer's strategy does not discard a brick from main pile.

    if 18 < discard_top < 43:
        taken_from_main = get_top_brick(main_pile)
        computer_tower_index = (taken_from_main - 1) // 6
        brick_to_remove = tower[computer_tower_index]
        tower[computer_tower_index] = taken_from_main
        discard.insert(0, brick_to_remove)  # Place new brick and move unwanted brick into discard.
        print("The computer picked [", tower[computer_tower_index], "] from the main pile.", sep='')
        return tower


def main():
    """
    This function puts it all together.
    All user input takes place in this main function.
    """

    main_pile = setup_bricks()[0]  # takes main pile from setup_bricks
    shuffle_bricks(main_pile)  # shuffles main pile
    discard = setup_bricks()[1]  # takes discard pile from setup_bricks, which begins as empty
    add_brick_to_discard(get_top_brick(main_pile), discard)  # places top brick from main pile into discard pile

    first_deal = deal_initial_bricks(main_pile)  # makes a list called first deal using deal_initial_bricks function
    computer_tower = first_deal[0]  # computer tower is taken from this list's first index
    user_tower = first_deal[1]  # user tower is taken from this list's second index
    instructions()
    print("Computer Tower: ", computer_tower)
    print("Your Tower: ", user_tower)

    while check_tower_blaster(computer_tower) == False and check_tower_blaster(user_tower) == False:

        print("-----------------------------------------------------------------------------------------")
        print("COMPUTER'S TURN:")
        print("Computer's Tower: [?, ?, ?, ?, ?, ?, ?, ?, ?, ?]", )
        print("The brick in discard pile is [", discard[0], "]", sep='')
        computer_play(computer_tower, main_pile, discard)  # computer picks the brick (print is included),
        # and gets the new computer tower

        print("The computer has swapped a brick.")

        # Call the check_bricks function to check if the main pile is empty after each turn.
        check_bricks(main_pile, discard)

        if check_tower_blaster(computer_tower) == True or check_tower_blaster(user_tower) == True:
            print("= = = = = = = = = = = = = = = = = = G A M E  O V E R = = = = = = = = = = = = = = = = = =")
            if check_tower_blaster(computer_tower) == True:
                if check_tower_blaster(computer_tower):
                    print("You Lost! :(")
                    print("Computer Tower: ", computer_tower)
                    print("Your Tower: ", user_tower)
                    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
                if check_tower_blaster(user_tower) == True:
                    print("YOU WON! :)")
                    print("Your Tower: ", user_tower)
                    print("Computer Tower: ", computer_tower)
                    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            break

        print("-----------------------------------------------------------------------------------------")
        print("YOUR TURN!:")
        print("Your Tower:", user_tower)
        print("The brick in discard pile is [", discard[0], "]", sep='')
        while 0 == 0:  # takes selection of D or M from user (discard pile or main pile)
            selection = input(
                "Press 'D' to take the brick from the discard pile or 'M' to take a brick from the main pile. ")
            if selection[0] == 'D' or selection[0] == 'd':  # if selection is from discard pile
                print("You picked [", discard[0], "] from the discard pile.", sep='')

                while 0 == 0:
                    swapped_out_brick = int(input("Which brick do you want to swap out? (Input number on brick): "))

                    # if a brick is successfully replaced, display what has been swapped out, what has been added,
                    # remove the swapped out brick from index 1, and display the new tower
                    if find_and_replace(discard[0], swapped_out_brick, user_tower, discard):
                        find_and_replace(discard[0], swapped_out_brick, user_tower, discard)
                        print("You replaced [", swapped_out_brick, "] with [", discard[1], "]", sep='')
                        discard.pop(1)
                        print("Your Tower: ", user_tower)
                        break
                break

            if selection[0] == 'M' or selection[0] == 'm':  # if selection is from the main pile
                brick_from_main = get_top_brick(main_pile)
                print("The top brick of the main pile is [", brick_from_main, "]", sep='')

                while 0 == 0:
                    choice = input("Do you want to use this brick? Type 'Y' if yes, or 'N' to skip turn. ")
                    if choice[0] == 'Y' or choice[0] == 'y':
                        # if yes, takes input from user for which brick to swap out
                        while 0 == 0:
                            swapped_out_brick = int(input(
                                "Which brick do you want to swap out? (Input number on brick): "))

                            # check if user's said brick is actually in his pile, if so, replace, and display success
                            if find_and_replace(brick_from_main, swapped_out_brick, user_tower, discard):
                                find_and_replace(brick_from_main, swapped_out_brick, user_tower, discard)
                                print("You replaced [", swapped_out_brick, "] with [", brick_from_main, "]", sep='')

                                print("Your Tower: ", user_tower)
                                break
                        break

                    # if no, the brick that was drawn is moved to discard pile
                    if choice[0] == 'N' or choice[0] == 'n':
                        print("Your Tower: ", user_tower)
                        add_brick_to_discard(brick_from_main, discard)
                        break

                break

        # Call the check_bricks function to check if the main pile is empty after each turn.
        check_bricks(main_pile, discard)

        # If either the computer's tower or the human's tower is in ascending order, then the game is over
        if check_tower_blaster(computer_tower) == True or check_tower_blaster(user_tower) == True:
            print("")
            print("= = = = = = = = = = = = = = = = = = G A M E  O V E R = = = = = = = = = = = = = = = = = =")
            if check_tower_blaster(computer_tower):
                print("You Lost! :(")
                print("Computer Tower: ", computer_tower)
                print("Your Tower: ", user_tower)
                print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            if check_tower_blaster(user_tower):
                print("YOU WON! :)")
                print("Your Tower: ", user_tower)
                print("Computer Tower: ", computer_tower)
                print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            break


if __name__ == '__main__':
    main()

import random


### Die class that we previously wrote ###

class Die:
    '''Die class'''

    def __init__(self, sides=6):
        '''Die(sides)
        creates a new Die object
        int sides is the number of sides
        (default is 6)
        -or- sides is a list/tuple of sides'''
        # if an integer, create a die with sides
        #  from 1 to sides
        if isinstance(sides, int):
            self.numSides = sides
            self.sides = list(range(1, sides + 1))
        else:  # use the list/tuple provided
            self.numSides = len(sides)
            self.sides = list(sides)
        # roll the die to get a random side on top to start
        self.roll()

    def __str__(self):
        '''str(Die) -> str
        string representation of Die'''
        return 'A ' + str(self.numSides) + '-sided die with ' + \
               str(self.get_top()) + ' on top'

    def roll(self):
        '''Die.roll()
        rolls the die'''
        # pick a random side and put it on top
        self.top = self.sides[random.randrange(self.numSides)]

    def get_top(self):
        '''Die.get_top() -> object
        returns top of Die'''
        return self.top

    def set_top(self, value):
        '''Die.set_top(value)
        sets the top of the Die to value
        Does nothing if value is illegal'''
        if value in self.sides:
            self.top = value


### end Die class ###

class DinoDie(Die):
    '''implements one die for Dino Hunt'''

    def __init__(self, color):
        '''DinoDie(color)
        creates a new DinoDie object
        str color is the color of DinoDie'''
        self.color = color

        # create DinoDie based on the color of it
        if self.color == 'green':
            super().__init__(['dino', 'dino', 'dino', 'leaf', 'leaf', 'foot'])
        elif self.color == 'yellow':
            super().__init__(['dino', 'dino', 'leaf', 'leaf', 'foot', 'foot'])
        else:
            super().__init__(['dino', 'leaf', 'leaf', 'foot', 'foot', 'foot'])

    def __str__(self):
        '''str(DinoDie) -> str
        string representation of DinoDie'''
        return f'You rolled a {self.color} Dino die with {self.get_top()} on top.'

    def get_color(self):
        '''DinoDie.get_color() -> str
        returns the color of DinoDie'''
        return self.color


class DinoPlayer:
    '''implements a player of Dino Hunt'''

    def __init__(self, name):
        '''DinoPlayer(name)
        creates a new DinoPlayer object
        str name is the name of the player'''
        self.name = name
        self.points = 0

    def __str__(self):
        '''str(DinoPlayer) -> str
        string representation of DinoPlayer'''
        return f'{self.name} has {self.points} points'

    def get_name(self):
        '''DinoPlayer.get_name() -> str
        returns the name of DinoPlayer'''
        return self.name

    def get_points(self):
        '''DinoPlayer.get_points() -> int
        returns the points of DinoPlayer'''
        return self.points

    def increase_points(self, increment):
        '''DinoPlayer.increase_points(increment) -> None
        increases the points by increment'''
        self.points += increment


def play_dino_hunt(numPlayers, numRounds):
    '''play_dino_hunt(numPlayer,numRounds)
    plays a game of Dino Hunt
      numPlayers is the number of players
      numRounds is the number of turns per player'''
    # initialize the players
    player_list = []
    for i in range(numPlayers):
        name = ''
        while name.strip() == '':
            name = input(f'Player {i + 1}, please enter your name: ')
        print()
        player_list.append(DinoPlayer(name))

    # select a player to start
    current_player_num = random.randrange(numPlayers)

    # start the game
    for i in range(numRounds):
        print(f'ROUND {i + 1}\n')
        for j in range(numPlayers):
            # display the number of points each player has
            for p in player_list:
                print(f'{p.get_name()} has {p.get_points()} points.')
            print()

            # set the dice and the count for dinos rolled and feet rolled
            dice_list = [DinoDie('green') for i in range(6)]
            dice_list.extend([DinoDie('yellow') for i in range(4)])
            dice_list.extend([DinoDie('red') for i in range(3)])
            dino_count = 0
            foot_count = 0

            # start a turn
            print(f'{player_list[current_player_num].get_name()}, it is your turn!')
            earned_points = 0
            while True:
                rolled_dice = []
                # roll the dice
                input('Press enter to select dice and roll.')
                print()
                if len(dice_list) > 3:
                    for i in range(3):
                        die = dice_list[random.randrange(len(dice_list))]
                        dice_list.remove(die)
                        rolled_dice.append(die)
                        print(die)
                # less than three dice to roll
                else:
                    rolled_dice = dice_list
                    dice_list = []
                    for die in rolled_dice:
                        print(die)

                # determine which sides of the dice showed and their consequences
                for die in rolled_dice:
                    if die.get_top() == 'dino':
                        earned_points += 1
                        dino_count += 1
                    elif die.get_top() == 'leaf':
                        die.roll()
                        dice_list.append(die)
                    else:
                        foot_count += 1
                print()
                print(f'This turn so far: {dino_count} dinos and {foot_count} feet')
                # number of dice left
                print(f'You have {len(dice_list)} dice remaining:')
                # determine how many of each type of die are left
                green_dice_count = 0
                yellow_dice_count = 0
                red_dice_count = 0
                if len(dice_list) > 0:
                    for die in dice_list:
                        if die.get_color() == 'green':
                            green_dice_count += 1
                        elif die.get_color() == 'yellow':
                            yellow_dice_count += 1
                        elif die.get_color() == 'red':
                            red_dice_count += 1
                    # display which dice are left
                    print(f'{green_dice_count} green, {yellow_dice_count} yellow, {red_dice_count} red')

                # determine if a stomp happened
                if foot_count >= 3:
                    print('Too bad -- you have been stomped!\n')
                    earned_points = 0
                    break

                # ask the player whether he/she wants to roll again
                if len(dice_list) > 0:
                    keep_going = ''
                    while keep_going.lower() not in ['y', 'n']:
                        keep_going = input('Do you want to roll again? (y/n): ')
                        print()
                    if keep_going.lower() == 'n':
                        break
                # no more dice to roll
                else:
                    print('You have run out of dice to roll.\n')
                    break

            # add the earned points and continue to the next player
            player_list[current_player_num].increase_points(earned_points)
            current_player_num = (current_player_num + 1) % numPlayers

    # determine the winner(s)
    highest_score = 0
    for p in player_list:
        print(f'{p.get_name()} has {p.get_points()} points.')
        # determine the highest score
        if p.get_points() > highest_score:
            highest_score = p.get_points()
    is_tie = True
    for p in player_list:
        if p.get_points() != highest_score:
            is_tie = False
            break

    if not is_tie:
        # display the highest score
        print(f'The highest score is {highest_score}.')
        winners_list = [p for p in player_list if p.get_points() == highest_score]
        # one winner
        if len(winners_list) == 1:
            print(f'{winners_list[0].get_name()} is the winner!')
        # multiple winners
        else:
            for winner in winners_list:
                print(f'{winner.get_name()} is a winner!')
    # everyone has the same number of points
    else:
        print('No one won! Everyone has the same number of points.')

    # thank everyone for playing
    print('Thanks for playing!')


def game_rules():
    '''game_rules() -> None
    prints the rules for Dino Hunt'''
    print('Welcome to Dino Hunt!')
    print('This game simulates the hunting for dinosaurs using special dice.\n')
    print('Rules:')
    print('This game requires at least two players, and any number of rounds can be played.\n')
    print('There are three kinds of dice: green, yellow, and red.')
    print('Each die has three different sides: dino, leaf, foot.')
    print('Green Die: 3 dinos, 2 leaves, 1 foot')
    print('Yellow Die: 2 dinos, 2 leaves, 2 feet')
    print('Red Die: 1 dino, 2 leaves, 3 feet\n')
    print('On each turn, the player starts with 6 green dice, 4 yellow dice, and 3 red dice.')
    print('On each roll, the player selects 3 random dice and rolls them. ', end='')
    print('The dice are discarded if the top is a dino or a foot.')
    print('Dino: player earns 1 point')
    print('Leaf: die gets put back in the original pile to be rerolled')
    print('Foot: stomp\n')
    print('The player\'s turn ends when there are no more dice to roll, ', end='')
    print('he/she decides not to roll anymore, or three or more feet have been rolled.')
    print('If three or more feet have been rolled, the player is considered \'stomped\' and ', end='')
    print('loses all the points earned from the round.')
    print('A player cannot lose the points earned from previous rounds.')
    print('The player with the most points wins the game.\n')
    input('Are you ready to play? Press enter to start, and have fun!')
    print()


def get_num_players(minimum=2):
    '''get_num_players([minimum=2]) -> int
    gets the input of the number of players'''
    while True:
        num_players = input('Enter the number of players: ')

        # check if it is a valid input
        if num_players.strip() == '':
            print('Please enter the number of players.\n')
        elif not num_players.isdigit():
            print(f'{num_players} is not a nonnegative integer.\n')
        elif int(num_players) < minimum:
            print(f'You must have at least {minimum} players.\n')
        else:
            num_players = int(num_players)
            break
    print()
    return num_players


def get_num_rounds(minimum=1):
    '''get_num_rounds([minimum=1]) -> int
    gets the input of the number of rounds'''
    while True:
        num_rounds = input('Enter the number of rounds which will be played: ')

        # check if it is a valid input
        if num_rounds.strip() == '':
            print('Please enter the number of rounds that will be played.\n')
        elif not num_rounds.isdigit():
            print(f'{num_rounds} is not a nonnegative integer.\n')
        elif int(num_rounds) < minimum:
            print(f'A minimum of {minimum} round must be played.\n')
        else:
            num_rounds = int(num_rounds)
            break
    print()
    return num_rounds


# play the game
game_rules()
num_players = get_num_players()
num_rounds = get_num_rounds()
play_dino_hunt(num_players, num_rounds)
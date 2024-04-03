from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from ctypes import py_object

class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = None # change None value if necessary
        self.team_count = 0

    """
    Best case for choose_manually is is O(1), if the user is 'done' and stores no pokemon
    Worst case for choose_manually is O(n), where n the number of user inputs. As it iterates 
    over user pokemon choices, appending valid options to self.team until the team limit has 
    been reached the user is done
    """
    def choose_manually(self):
        self.team = ArrayR(1) # Initialise array size

        while len(self.team) < PokeTeam.TEAM_LIMIT: # While team Array is less TEAM_LIMIT (6)
            pokemon_choice = input("Enter a Pokemon's name or 'done': ") # Requests user pokemon choices
            if pokemon_choice.lower() == 'done': # If user requests done, break
                break
            if pokemon_choice in PokeTeam.POKE_LIST: # If user chose a pokemon in the pokemon list
                for i in range(len(self.team)): # Append pokemon to the array and increase team size by 1
                    self.team[i] = pokemon_choice
                    self.team += 1
            else:
                print("Inavlid Pokemon name, try again") # If user inputs invalid pokemon, try again until done or reached team limit


    def choose_randomly(self) -> None:
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1


    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        Best and Worse Case is O(n), where n is the length of team
        """
        # Heals all Pokémon to their original HP
        for pokemon in self.team:
            pokemon.health = Pokemon.health # This does not work

        # # Heals all Pokémon to their original HP
        # pokemon_health  = Pokemon.get_health
        # for pokemon in self.team:
        #     for health in pokemon:
        #         pokemon_health = base_health

    def assign_team(self, criterion: str = None) -> None:
        #Next Task
        raise NotImplementedError

    def assemble_team(self, battle_mode: BattleMode) -> None:
        #Next Task
        raise NotImplementedError

    def special(self, battle_mode: BattleMode) -> None:
        #Next Task
        raise NotImplementedError

    def __getitem__(self, index: int):
        """
        Best Case for __getitem__ is O(1), if the user gets a successful index the first time
        Worst Case for __getitem__ is O(n), where n is the number of attempts the user inputs,
        as it will repeat n amount of times until the user get a valid index
        """
        poke_team = self.team # Makes poke_team the array
        index = int(input("Enter an index to retrieve a Pokemon: ")) # Ask user input what index
        try:
            pokemon = poke_team[index] # Tries to see if user input index is within list
            print(f"The Pokemon at index {index} is: {pokemon}") #print
        except IndexError: # If not in list, raise error
            print("Invalid index. Please enter an index within the range of the team.")
        

    def __len__(self):
        """
        Best and Worse Case is O(1) as it only returns 
        """
        return len(self.team) #returns length of team

    def __str__(self):
        """
        Best Case for __str__ is O(1) if the list is empty
        Worst Case for __str__ is O(n), where n is the length of the team, as it 
        would have to loop through the team
        """
        team_str = "Pokemon Team:\n"
        # Displays all pokemon in the current team
        for pokemon in self.team:
            team_str += f"{pokemon.name}\n"
        return team_str
        


class Trainer:

    def __init__(self, name) -> None:
        self.name = name # Initialises Trainer Class
        self.poke_team = PokeTeam()
        self.pokedex = PokeTeam.POKE_LIST

    def pick_team(self, method: str) -> None:
        method = input('Enter r to choose team randomly or enter m to pick manually') # Asks user to choose method
        if method.lower() == 'r':
            PokeTeam.choose_randomly()
        elif method.lower() == 'm':
            PokeTeam.choose_manually()
        else:
            raise ValueError("Invalid input. Enter either 1 or 2.") # If input is invalid, raise error

    def get_team(self) -> PokeTeam:
        return self.poke_team # Gets current pokemon team
    
    def get_name(self) -> str:
        return self.name # Gets trainer name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        poke_type = pokemon.poketype # Get the PokeType of the pokemon
        self.pokedex.register_pokemon(poke_type) # Register the pokemon in the Pokedex

    def get_pokedex_completion(self) -> float:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())
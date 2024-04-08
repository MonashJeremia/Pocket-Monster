from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from math import *

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        """
        BIG O
        """
        winner_team = None # Initialises winner_team
        if self.battle_mode == BattleMode.SET: # Depending on which battle mode selected, it will procees with the following simulation
            winner_team = self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            winner_team = self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            winner_team = self.optimise_battle()
        else:
            raise ValueError("Please select valid BattleMode") # Raise if invalid input
        
        if winner_team == self.trainer_1.poke_team.team: # After the simulation, if it returns t1 poke team then
            return self.trainer_1 # t1 is winner
        elif winner_team == self.trainer_2.poke_team.team: # Vice versa
            return self.trainer_2
        return None # If no winner
        
    def _create_teams(self) -> None:
        """
        BIG O
        """

        self.trainer_1.poke_team.assemble_team(self.battle_mode) #assemble teams to t1 and t2
        self.trainer_2.poke_team.assemble_team(self.battle_mode)

    # def set_round_start(self):
    #     t1_pokemon = self.trainer_1.poke_team.team[-1] # Intialises last index in team to be current pokemon for t1
    #     t2_pokemon = self.trainer_2.poke_team.team[-1] # Intialises last index in team to be current pokemon for t2

    #     if t1_pokemon.speed > t2_pokemon.speed: # If t1 speed is faster than t2 speed
    #         self.battle_round(t1_pokemon, t2_pokemon) # t1 is attacker and t2 is defender
    #     elif t2_pokemon.speed > t1_pokemon.speed: # Vice versa
    #         self.battle_round(t2_pokemon, t1_pokemon)
    #     else:
    #         self.simultaneous_attack(t1_pokemon, t2_pokemon) # If both same speed, then call simultaneous_attack()

    #     self.set_round_end(t1_pokemon, t2_pokemon)

    # def set_round_end(self, t1_pokemon, t2_pokemon):
    #     if t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If both Pokemon alive, -1 hp from current hp
    #         t1_pokemon.get_health = t1_pokemon.get_health() - 1 # Gets current hp of pokemon and decrease by -1hp
    #         t2_pokemon.get_health = t2_pokemon.get_health() - 1

    #     if not t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If t2_pokemon is alive and other is not 
    #         t2_pokemon.level_up() # Level up t2_pokemon

    #     elif t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # If t1_pokemon is alive and other is not 
    #         t1_pokemon.level_up() # Level up t1_pokemon
    #     elif not t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # If both pokemon die
    #         pass # Nothing happens

    # def check_usable_team(self) -> bool:
    #     usable_team = any(pokemon.is_alive() for pokemon in self) # If atleast one pokemon is alive in the team 
    #     return usable_team # Return boolean
    
    def battle_round(self, attacker, defender) -> None: # Attacker intial turn
        """
        BIG O
        """
        attack_damage = ceil(attacker.attack(defender) * (self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion())) # Calculates new attack damage from the pokemon's attack multiplied by the ratio of the attackers and defenders pokedex completion
        defender.defend(attack_damage) # Decrease the defender (pokemon) hp by the newly calculated attack

        if defender.is_alive(): # Defender Turn if pokemon still alive
            counter_attack_damage = ceil(defender.attack(attacker) * (self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()))
            attacker.defend(counter_attack_damage)

    def simultaneous_attack(self, pokemon_1, pokemon_2) -> None: # Both pokemon attack each other
        """
        BIG O
        """
        attack_damage_1 = ceil(pokemon_1.battle_power(pokemon_2) * (self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion()))
        attack_damage_2 = ceil(pokemon_2.battle_power(pokemon_1) * (self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion()))

        pokemon_1.defence(attack_damage_2) # Decrease both hp
        pokemon_2.defence(attack_damage_1)

    # Note: These are here for your convenience
    # If you prefer you can ignore them
    def set_battle(self) -> PokeTeam | None:
        """
        BIG O
        """
        self._create_teams()
        while len(self.trainer_1.poke_team.team) > 0 and len(self.trainer_2.poke_team.team) > 0: # While length of both teams is >0
            t1_pokemon = self.trainer_1.poke_team.team[len(self.trainer_1.poke_team.team) - 1] # Intialises last index in team to be current pokemon for t1
            t2_pokemon = self.trainer_2.poke_team.team[len(self.trainer_2.poke_team.team) - 1] # Intialises last index in team to be current pokemon for t2

            # Calculates Speed
            if t1_pokemon.speed > t2_pokemon.speed: # If t1 speed is faster than t2 speed
                self.battle_round(t1_pokemon, t2_pokemon) # t1 is attacker and t2 is defender
            elif t2_pokemon.speed > t1_pokemon.speed: # Vice versa
                self.battle_round(t2_pokemon, t1_pokemon)
            else:
                self.simultaneous_attack(t1_pokemon, t2_pokemon) # If both same speed, then call simultaneous_attack()

            # Check pokemon vitality
            if t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If both Pokemon alive, -1 hp from current hp
                t1_pokemon.get_health = t1_pokemon.get_health() - 1 # Gets current hp of pokemon and decrease by -1hp
                t2_pokemon.get_health = t2_pokemon.get_health() - 1
            
            if not t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If t2_pokemon is alive and other is not
                t2_pokemon.level_up() # Level up t2_pokemon
                self.trainer_1.poke_team.team.pop() # Remove dead pokemon (current t1_pokemon) from team
            elif t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # Vice versa
                t1_pokemon.level_up() 
                self.trainer_1.poke_team.team.pop() 
            elif not t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # If both pokemon die
                pass # Nothing happens
        
        # Return the winning team
        if len(self.trainer_1.poke_team.team) > 0: # If t1 team length > 0 
            return self.trainer_1.poke_team.team #t1 wins
        elif len(self.trainer_2.poke_team.team) > 0: # Vice versa
            return self.trainer_2.poke_team.team

    def rotate_battle(self) -> PokeTeam | None:
        """
        BIG O
        """
        self._create_teams()
        while not self.trainer_1.poke_team.team.is_empty() and not self.trainer_2.poke_team.team.is_empty(): # While both team stacks are not empty
            
            t1_pokemon = self.trainer_1.poke_team.team.serve() # Assigns t1's first pokemon
            t2_pokemon = self.trainer_2.poke_team.team.serve() # Assigns t2's first pokemon

            # Calculate Speeds
            if t1_pokemon.speed > t2_pokemon.speed: # If t1 speed is faster than t2 speed
                self.battle_round(t1_pokemon, t2_pokemon) # t1 is attacker and t2 is defender
            elif t2_pokemon.speed > t1_pokemon.speed: # Vice versa
                self.battle_round(t2_pokemon, t1_pokemon)
            else:
                self.simultaneous_attack(t1_pokemon, t2_pokemon) # If both same speed, then call simultaneous_attack()

            # Checks if pokemons is alive
            if t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If both Pokemon alive, -1 hp from current hp
                t1_pokemon.get_health = t1_pokemon.get_health() - 1 # Gets current hp of pokemon and decrease by -1hp
                t2_pokemon.get_health = t2_pokemon.get_health() - 1
            
            if not t1_pokemon.is_alive() and t2_pokemon.is_alive(): # If t2_pokemon is alive and other is not
                t2_pokemon.level_up() # Level up t2_pokemon
                self.trainer_2.poke_team.team.append(t2_pokemon) # Appends t2_pokemon to the start of the array (which is the back)
            elif t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # If t1_pokemon is alive and other is not 
                t1_pokemon.level_up() # Level up t1_pokemon
                self.trainer_1.poke_team.team.append(t1_pokemon) # # Appends t1_pokemon to the start of the array (which is the back)
            elif not t1_pokemon.is_alive() and not t2_pokemon.is_alive(): # If both pokemon die
                pass # Nothing happens

        # Return the winning team
        if self.trainer_1.poke_team.team.is_empty(): # If t1 team length is empty
            return self.trainer_2.poke_team.team #t2 wins
        elif self.trainer_2.poke_team.team.is_empty(): # Vice versa
            return self.trainer_1.poke_team.team

    def optimise_battle(self) -> PokeTeam | None:
        """
        BIG O
        """
        # check if team alive
        #write stuff
        
        self.end_battle()
        raise NotImplementedError


if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")

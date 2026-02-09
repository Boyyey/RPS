from RPS_game import play, quincy, random_bot, reflective, cycle
from RPS import player

bots = [quincy, random_bot, reflective, cycle]

for bot in bots:
    print(f"--- Playing against {bot.__name__} ---")
    play(player, bot, 1000, verbose=True)

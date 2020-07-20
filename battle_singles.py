from showdown_webdriver import Driver

battle_format = "gen8vgc2020"

bot_driver = Driver("firefox", "SutadasutoIA", "Stardust_1")
bot_driver.load_team("sample_team", battle_format)
bot_driver.request_battle(battle_format)
while True:
    expected_action = bot_driver.get_expected_action()
    if expected_action == "start":
        bot_driver.choose_initial_pokemon(["Rotom", "Hydreigon", "Braviary", "Excadrill"])
        break

prev_turn = 0
while True:
    current_turn = bot_driver.get_current_turn()
    if current_turn > prev_turn:
        print("Turn %s" % current_turn)
        terrain, terrain_turns = bot_driver.get_terrain()
        rooms = bot_driver.get_rooms()
        prev_turn = current_turn
    if bot_driver.battle_has_finished():
        break
    expected_action = bot_driver.get_expected_action()
    if expected_action == "move":
        action = "move"
        target = ""
        if action == "move":
            bot_driver.click_on_move(target)
        else:
            bot_driver.switch_pokemon(target)
    elif expected_action == "switch":
        pokemon = ""
        bot_driver.switch_pokemon(pokemon)
a = 0
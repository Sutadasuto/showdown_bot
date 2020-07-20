import os

# Add drivers folder to path
os.environ["PATH"] += ":drivers"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Driver(object):
    def __init__(self, explorer, username, password=None):

        # Open the driver according to the desired browser
        if explorer == "firefox":
            self.webdriver = webdriver.Firefox()
        elif explorer == "chrome":
            self.webdriver = webdriver.Chrome()
        self.webdriver.get("https://play.pokemonshowdown.com/")

        # Let's log in
        self.signed_in = self.log_in(username, password)

    def go_home(self):
        self.webdriver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/ul[1]/li[1]/a").click()

    def load_team(self, team_file, format_name="gen8ou"):
        # format_name (at the moment of written this code) is genNformatname

        # Return to Home
        self.go_home()

        # Click on "Teambuilder"
        # Click on desired format
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@value='teambuilder']"))
            ).click()
        except:
            # Format name button not found. Check current gen
            self.webdriver.quit()

        # Click on "New Team"
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.NAME, "newTop"))
            ).click()
        except:
            # New Team button not found. Probably the page had problems loading
            self.webdriver.quit()

        # Select format
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/ol/li[2]/button[1]/em"))
            ).click()
        except:
            # Select a format button not found. Probably the page had problems loading
            self.webdriver.quit()

        # Click on desired format
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='selectFormat' and @value='%s']" % format_name))
            ).click()
        except:
            # Format name button not found. Check current gen
            self.webdriver.quit()

        # Click on Import from text or URL
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='import']"))
            ).click()
        except:
            # Import button not found
            self.webdriver.quit()

        # Write and save the team
        # Paste team on text box
        with open(team_file, "r") as team:
            try:
                WebDriverWait(self.webdriver, 60).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[@class='textbox']"))
                ).send_keys(team.read())
            except:
                # Text box not found
                self.webdriver.quit()

        # Click on Save
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='saveImport']"))
            ).click()
        except:
            # Save button not found
            self.webdriver.quit()

        # Validate team
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='validate']"))
            ).click()
        except:
            # Validate button not found or disabled
            self.webdriver.quit()
        # Look for validation result text
        try:
            validation_text = WebDriverWait(self.webdriver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/form/p[1]"))
            ).text
        except:
            # Label not found
            self.webdriver.quit()

        if validation_text.startswith("Your team is valid"):
            print("Team has been loaded and is valid for the selected format.")
            self.webdriver.find_element(By.XPATH, "//button[@name='close']").click()
            self.go_home()
            return True
        else:
            print("Team was either not loaded or invalid for the selected format.")
            self.webdriver.quit()
            return False

    def log_in(self, username, password=None):
        # Click on Choose name
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.NAME, "login"))
            ).click()
        except:
            # Choose name button not found. Probably the page had problems loading
            self.webdriver.quit()

        # Send username
        self.webdriver.find_element_by_name("username").send_keys(username)
        # Click on "Choose name" button after entering user name
        self.webdriver.find_element_by_xpath("/html/body/div[4]/div/form/p[2]/button[1]/strong").click()

        # If the username is known to have a password, send the password
        if password is not None:
            try:
                WebDriverWait(self.webdriver, 2).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                ).send_keys(password)
            except:
                # Password text box not found
                self.webdriver.quit()
                return False
            # Click on "Log in" button
            self.webdriver.find_element_by_xpath("/html/body/div[4]/div/form/p[5]/button[1]").click()
        # Otherwise, verify the site is not expecting a password
        else:
            try:
                password_tb = WebDriverWait(self.webdriver, 2).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                print("Password expected. Quitting driver")
                return False
            except:
                _ = 0

        try:
            page_username = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "username"))
            ).get_attribute("data-name")[1:]
        except:
            # User name element not found
            self.webdriver.quit()
            return False

        # Was log in successful?
        if page_username == username:
            print("User name is %s. Log in successful!" % username)
            return True
        else:
            print("User name is %s. Log in failed..." % page_username)
            return False

    def request_battle(self, format_name="gen8ou"):
        self.go_home()

        # Select format
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//button[@name='format']"))
            ).click()
        except:
            # Format selection button not found
            self.webdriver.quit()
            return False
            # Click on desired format
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='selectFormat' and @value='%s']" % format_name))
            ).click()
        except:
            # Format name button not found. Check current gen
            self.webdriver.quit()
            return False

        # Click on search button "Battle!"
        try:
            WebDriverWait(self.webdriver, 60).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@name='search']"))
            ).click()
        except:
            # Battle! button not found
            self.webdriver.quit()
            return False

        # Wait for an opponent
        try:
            opponent = WebDriverWait(self.webdriver, 120).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div/div[9]/div"))
            )
            print("Battle versus %s found!" % opponent.text)
            return True
        except:
            print("No battle found...")
            return False

    def get_terrain(self):
        'Returns: a tuple (name of current terrain -or "none" if not terrain is present-, minimum turns left)'

        terrain_names = ["psychic", "misty", "grassy", "electric"]
        battlefield_elements = self.find_battlefield_elements()
        for terrain_name in terrain_names:
            for element in battlefield_elements:
                if "%s terrain" % terrain_name in element:
                    # E.g. Psychic Terrain (3 or 6 turns)
                    min_turns = element.split(" (")[1].split(" or ")[0]
                    return (terrain_name, int(min_turns))
        return ("none", 0)

    def get_rooms(self):
        ':return a list of tuples (name of current room -or "none" if no room is present-, turns left)'

        room_names = ["trick", "magic"]
        found_rooms = []
        battlefield_elements = self.find_battlefield_elements()
        for room_name in room_names:
            for element in battlefield_elements:
                if "%s room" % room_name in element:
                    # E.g. Trick Room (2 turns)
                    min_turns = element.split(" (")[1].split(" turns")[0]
                    found_rooms.append((room_name, int(min_turns)))
        if len(found_rooms) == 0:
            return [("none", 0)]
        return found_rooms

    def get_current_turn(self):

        # Find the div in the battle screen that prints the current turn
        try:
            turn_text = WebDriverWait(self.webdriver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "turn"))
            ).text
            # Return the different text rows as a list
            return int(turn_text.split(" ")[-1])
        except:
            print("No battle screen found...")
            return None

    def get_current_pp(self):
        ':return a list of tuples (move name, current remaining pp)'

        moves = []
        # Find the buttons available to "Attack"
        try:
            buttons = WebDriverWait(self.webdriver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//button[@name='chooseMove']"))
            )
        except:
            print("No attack buttons found... Maybe they are hidden under 'Attack'?")
            return None

        for button in buttons:
            button_text = button.text.strip()
            # E.g. Stealth Rock\nRock\n32/32
            button_info = button_text.split("\n")
            name = button_info[0]
            pp = int(button_info[-1].split("/")[0])
            moves.append((name, pp))

        return moves

    def switch_pokemon(self, pokemon_name):
        ':argument Pokémon name as shown in Showdown e.g. Ferrothorn (notice the use capital letters)'

        # Find the buttons available to "Switch"
        try:
            buttons = WebDriverWait(self.webdriver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[@name='chooseSwitch']"))
            )
        except:
            print("No pokémon buttons found... Maybe they are hidden under 'Switch'?")
            return False

        for button in buttons:
            if button.text == pokemon_name:
                button.click()
                return True
        print("Impossible to switch to %s" % pokemon_name)
        return False

    def choose_initial_pokemon(self, pokemon_names):
        ':argument Either a string (name of initial pokémon) or a list of strings (names of pokémons to be choosen '\
        'in the order to te clicked). E.g. "Pikachu" or  ["Pikachu", "Eevee", "Charizard"]'

        if type(pokemon_names) is not list:
            pokemon_names = [pokemon_names]

        for pokemon_name in pokemon_names:
            pokemon_not_found = True
            # Find the buttons available to "start the battle"
            try:
                buttons = WebDriverWait(self.webdriver, 60).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//button[@name='chooseTeamPreview']"))
                )
            except:
                print("No pokémon buttons found")
                return False

            for button in buttons:
                if button.text == pokemon_name:
                    button.click()
                    pokemon_not_found = False
                    break
            if pokemon_not_found:
                print("%s button not found..." % pokemon_name)
                return False
        return True

    def click_on_move(self, move_name):
        ':argument Pokémon name as shown in Showdown e.g. Stealth Rock (notice the use of space and capital letters)'

        # Find and click the button corresponding to the move
        try:
            button = WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[@name='chooseMove' and @data-move='%s']" % move_name))
            )
            button_text = button.text.strip()
            # E.g. Stealth Rock\nRock\n32/32
            button_info = button_text.split("\n")
            pp = int(button_info[-1].split("/")[0])
            if pp > 0:
                button.click()
                return True
            else:
                print("Not enough pp for that move")
                return False
        except:
            print(
                "No %s button found... Does the pokémon know that move? Maybe it is hidden under 'Attack'?" % move_name)
            return False

    def get_expected_action(self):
        ':return A string, indicating if the bot is expected to "switch" into another pokémon, make a "move" with ' \
        'the current pokémon, or choose your initial pokémon to "start" the battle. If None is returned, no action ' \
        'from the bot is expected. If False is returned, an unexpected action is expected'

        try:
            what_to_do_label = self.webdriver.find_element(By.CLASS_NAME, "whatdo")
            # If there is an active pokémon, it is expect to attack or switch.
            # This can be know by the phrase "What will Pokémon do?"
            if what_to_do_label.text.startswith("What will "):
                return "move"
            elif what_to_do_label.text.startswith("Switch "):
                return "switch"
            elif what_to_do_label.text.startswith("How will you start "):
                return "start"
            else:
                print("Unknown action expected.")
                return False
        except:
            return None

    def find_battlefield_elements(self):
        # Find the div in the battle screen that prints the current terrain (among other battlefield conditions)
        try:
            battle_field_text = WebDriverWait(self.webdriver, 120).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div/div[3]"))
            ).text.lower()
            # Return the different text rows as a list
            return battle_field_text.split("\n")
        except:
            print("No battle screen found...")
            return None

    def in_battle_screen(self):
        try:
            self.webdriver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div/div[9]/div")
            return True
        except:
            return False

    def battle_has_finished(self):
        try:
            self.webdriver.find_element(By.XPATH, "//button[@name='closeAndRematch']")
            return True
        except:
            return False

    def close_page(self):
        self.webdriver.quit()

# md = Driver("firefox", "SutadasutoIA", "Stardust_1")
# md.load_team("ou", "gen8ou")
# md.request_battle("gen8ou")
# md.choose_initial_pokemon("Fierro")
a = 0

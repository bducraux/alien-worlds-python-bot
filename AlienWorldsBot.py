# Alien Worlds Bot class

import pyautogui as gui
from time import sleep
from os import system, name, path
from pyfiglet import Figlet


class AlienWorldsBot:
    def __init__(self):
        # Initialize bot
        self.mine_button_coordinates = {}
        self.claim_button_coordinates = {}
        self.approve_button_coordinates = {}
        self.refresh_button_coordinates = {}

        self.sleep_time_between_actions = 10
        self.sleep_time_between_mining_cycles = 0

        greetings()

        # get menu option
        self.get_user_menu_option()

    def get_user_menu_option(self, message=None):
        clear_console_screen()
        print_logo()
        if message is not None:
            print(message)
        # Get user input
        menu_options = "\n\n" \
                       "1. Start bot.\n" \
                       "2. Configurate click coordinates.\n" \
                       "3. Load last click coordinates.\n" \
                       "4. Set sleep time between actions.\n" \
                       "5. Set sleep time between mining\n" \
                       "6. Display configurations.\n" \
                       "7. Quit" \
                       "\n\n" \
                       "Choose an option: "

        user_input = input(menu_options)
        if user_input == "1":
            self.start_bot()
        elif user_input == "2":
            self.get_coordinates()
            self.save_coordinates_to_file()
            self.get_user_menu_option("Coordinates saved successfully. You can now start the bot.")
        elif user_input == "3":
            if self.load_coordinates_from_file():
                self.get_user_menu_option("Coordinates loaded from file. You can now start the bot.")
            else:
                self.get_user_menu_option("No coordinates found in file. "
                                          "Please choose option 2 to configure click coordinates.")
        elif user_input == "4":
            self.set_sleep_time_between_actions()
        elif user_input == "5":
            self.set_sleep_time_between_mining_cycles()
        elif user_input == "6":
            self.display_configurations()

        elif user_input == "7":
            raise SystemExit
        else:
            print("Invalid input. Try again.")

    def start_bot(self):
        try:
            if not all([self.mine_button_coordinates, self.claim_button_coordinates, self.approve_button_coordinates,
                        self.refresh_button_coordinates]):
                # ask user if he wants to load last coordinates
                user_input = input("\n\nYou have not configured click coordinates.\n"
                                   "Do you want to load last coordinates? (y/n): ")

                if user_input == "y":
                    if not self.load_coordinates_from_file():
                        self.get_user_menu_option("No saved coordinates found. "
                                                  "Please configure the click coordinates first.")

                    print_message("\n\nClick coordinates loaded from file.\n")
                    self.start_bot()

                print_message("Please configure click coordinates.")
                self.get_user_menu_option()

            print_message("Starting bot... \n If you want to stop the bot press Ctrl+C")
            # Start bot
            cycle = 1
            while True:
                waiting(f"Starting Cycle {cycle}", 3)

                # Mine
                clear_console_screen()
                print_message("Mining...")
                gui.moveTo(self.mine_button_coordinates['x'], self.mine_button_coordinates['y'])
                gui.click()
                waiting("Mining", self.sleep_time_between_actions)

                # Claim
                print_message("Claiming...")
                gui.moveTo(self.claim_button_coordinates['x'], self.claim_button_coordinates['y'])
                gui.click()
                waiting("Claiming", self.sleep_time_between_actions)

                # Approve
                print_message("Approving...")
                gui.moveTo(self.approve_button_coordinates['x'], self.approve_button_coordinates['y'])
                gui.click()
                waiting("Approving", self.sleep_time_between_actions)

                if cycle % 10 == 0:  # Refresh every 10 cycles
                    # Refresh page
                    print_message("Refreshing page")
                    gui.moveTo(self.refresh_button_coordinates['x'], self.refresh_button_coordinates['y'])
                    gui.click()
                    waiting("Refreshing page", 10)
                    cycle = 0

                if self.sleep_time_between_mining_cycles != 0:
                    waiting("Sleeping", self.sleep_time_between_mining_cycles)

                cycle += 1
        except KeyboardInterrupt:
            print_message("\n\nBot stopped.")
            self.get_user_menu_option()

    def set_sleep_time_between_actions(self):
        """
        Set sleep time between actions
        :return:
        """
        try:
            self.sleep_time_between_actions = int(input("Enter sleep time in seconds: "))
            self.get_user_menu_option()
        except ValueError:
            print("Invalid input. Try again.")
            self.set_sleep_time_between_actions()

    def set_sleep_time_between_mining_cycles(self):
        """
        Set sleep time between mining cycles
        :return:
        """
        try:
            self.sleep_time_between_mining_cycles = int(input("Enter sleep time in minutes: ")) * 60
            self.get_user_menu_option()
        except ValueError:
            print("Invalid input. Try again.")
            self.set_sleep_time_between_mining_cycles()

    # get mine button coordinates by using gui to get x,y coordinates click
    @staticmethod
    def get_button_coordinates(button_name):
        try:
            input(f"Position mouse on the {button_name} button and press enter: ")
            x, y = gui.position()

            return {'x': x, 'y': y}
        except KeyboardInterrupt:
            raise SystemExit

    def get_coordinates(self):
        try:
            # Get mine button coordinates
            self.mine_button_coordinates = self.get_button_coordinates("Mine")
            # Get claim button coordinates
            self.claim_button_coordinates = self.get_button_coordinates("Claim")
            # Get approve button coordinates
            self.approve_button_coordinates = self.get_button_coordinates("Approve")
            # Get refresh button coordinates
            self.refresh_button_coordinates = self.get_button_coordinates("Refresh page")
        except KeyboardInterrupt:
            raise SystemExit

    def save_coordinates_to_file(self):
        with open("coordinates.txt", "w") as file:
            file.write(f"{self.mine_button_coordinates['x']} {self.mine_button_coordinates['y']}\n")
            file.write(f"{self.claim_button_coordinates['x']} {self.claim_button_coordinates['y']}\n")
            file.write(f"{self.approve_button_coordinates['x']} {self.approve_button_coordinates['y']}\n")
            file.write(f"{self.refresh_button_coordinates['x']} {self.refresh_button_coordinates['y']}\n")

    def load_coordinates_from_file(self):
        # check if file exists
        if not path.isfile("coordinates.txt"):
            return False

        with open("coordinates.txt", "r") as file:
            lines = file.readlines()
            self.mine_button_coordinates = {'x': int(lines[0].split()[0]), 'y': int(lines[0].split()[1])}
            self.claim_button_coordinates = {'x': int(lines[1].split()[0]), 'y': int(lines[1].split()[1])}
            self.approve_button_coordinates = {'x': int(lines[2].split()[0]), 'y': int(lines[2].split()[1])}
            self.refresh_button_coordinates = {'x': int(lines[3].split()[0]), 'y': int(lines[3].split()[1])}

        return True

    def display_configurations(self):
        try:
            print_logo()
            print("Current configurations:")
            print(f"Sleep time between actions: {self.sleep_time_between_actions} seconds")
            print(f"Sleep time between mining cycles: {int(self.sleep_time_between_mining_cycles / 60)} minutes")
            print("Coordinates are set? " + ("Yes" if self.load_coordinates_from_file() else "No"))
            print("\n")
            input("Press enter to back to menu...")
            self.get_user_menu_option()
        except KeyboardInterrupt:
            raise SystemExit


def clear_console_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def waiting(message, sleep_time):
    for i in range(int(sleep_time)):
        # print text progress bar
        bar_length = 20
        filled_length = int(round(bar_length * i / sleep_time))
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        count_down = int(sleep_time) - i
        print_logo()
        print(f'\n\r{message}\n\nwaiting\n[{bar}] {count_down} seconds', end='')
        sleep(1)


def print_message(message):
    print_logo()
    print(f"\n{message}\n")


def print_logo():
    clear_console_screen()
    f = Figlet(font='doom')
    print(f.renderText('AlienWorldsBot'))


def greetings():
    # Greeting message
    print_logo()
    print("Hello, I'm the Alien Worlds Bot!")
    print("I will help you play Alien Worlds!\n")

    print("Instructions:")
    print("Open Alien Worlds website: play.alienworlds.io")
    print("login with your account")
    print("position the web browser window and the console window side by side\n")

    print("Follow the bot instructions to configure the click coordinates\n")

    print("Press Ctrl+C to stop the bot")

    print("Have fun!\n\n")

    input("Press Enter to continue...")

# Alien Worlds Bot class

import pyautogui as gui
from time import sleep
from os import system, name


def greetings():
    clear_console_screen()
    # Greeting message
    print("Hello, I'm the Alien Worlds Bot!")
    print("I will help you play Alien Worlds!\n")

    print("Instructions:")
    print("Open Alien Worlds website: play.alienworlds.io")
    print("login with your account")
    print("position the web browser window and the console window side by side\n")

    print("Follow the bot instructions to configure the click coordinates\n")

    print("Press Ctrl+C to stop the bot")

    print("Have fun!\n\n")


# get mine button coordinates by using gui to get x,y coordinates click
def get_button_coordinates(button_name):
    input(f"Position mouse on the {button_name} button and press enter: ")
    x, y = gui.position()

    return {'x': x, 'y': y}


class AlienWorldsBot:
    def __init__(self):
        # Initialize bot
        self.mine_button_coordinates = {}
        self.claim_button_coordinates = {}
        self.approve_button_coordinates = {}
        self.refresh_button_coordinates = {}

        self.sleep_time = 5

        greetings()

        # get menu option
        self.get_user_menu_option()

    def get_user_menu_option(self):
        # Get user input
        menu_options = "\n\n" \
                       "1. Start bot.\n" \
                       "2. Configurate click coordinates.\n" \
                       "3. Set sleep time between actions.\n" \
                       "4. Quit" \
                       "\n\n" \
                       "Choose an option: "

        user_input = input(menu_options)
        if user_input == "1":
            self.start_bot()
        elif user_input == "2":
            self.get_coordinates()
        elif user_input == "3":
            self.set_sleep_time()
        elif user_input == "4":
            raise KeyboardInterrupt
        else:
            print("Invalid input. Try again.")

    def get_coordinates(self):
        # Get mine button coordinates
        self.mine_button_coordinates = get_button_coordinates("Mine")
        # Get claim button coordinates
        self.claim_button_coordinates = get_button_coordinates("Claim")
        # Get approve button coordinates
        self.approve_button_coordinates = get_button_coordinates("Approve")
        # Get refresh button coordinates
        self.refresh_button_coordinates = get_button_coordinates("Refresh page")

        self.get_user_menu_option()

    def start_bot(self):
        try:
            if not all([self.mine_button_coordinates, self.claim_button_coordinates, self.approve_button_coordinates,
                        self.refresh_button_coordinates]):
                print_message("Please configure the click coordinates first.")
                self.get_coordinates()

            print_message("Starting bot... \n If you want to stop the bot press Ctrl+C")
            # Start bot
            cycles = 0
            while True:
                waiting(f"Starting Cycle {cycles}", 3)

                # Mine
                clear_console_screen()
                print_message("Mining...")
                gui.moveTo(self.mine_button_coordinates['x'], self.mine_button_coordinates['y'])
                gui.click()
                waiting("Mining", self.sleep_time)

                # Claim
                print_message("Claiming...")
                gui.moveTo(self.claim_button_coordinates['x'], self.claim_button_coordinates['y'])
                gui.click()
                waiting("Claiming", self.sleep_time)

                # Approve
                print_message("Approving...")
                gui.moveTo(self.approve_button_coordinates['x'], self.approve_button_coordinates['y'])
                gui.click()
                waiting("Approving", self.sleep_time)

                if cycles == 10:
                    # Refresh page
                    print_message("Refreshing page")
                    gui.moveTo(self.refresh_button_coordinates['x'], self.refresh_button_coordinates['y'])
                    gui.click()
                    waiting("Refreshing page", 5)
                    cycles = 0

                cycles += 1
        except KeyboardInterrupt:
            self.get_user_menu_option()

    def set_sleep_time(self):
        try:
            self.sleep_time = int(input("Enter sleep time in seconds: "))
            self.get_user_menu_option()
        except ValueError:
            print("Invalid input. Try again.")
            self.set_sleep_time()


def clear_console_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def waiting(message, sleep_time):
    for i in range(int(sleep_time / 0.5)):
        clear_console_screen()
        print(f"{message} {'.' * i}")
        sleep(0.5)


def print_message(message):
    clear_console_screen()
    print(message)

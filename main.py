from pynput.keyboard import Controller, Key
import pyautogui, time, os, csv, keyboard, pymem

IMAGE_ITIRATION = 0

class App:

    MAP_NAME = None
    MAP_IMAGE_ITTERATION = 0
    SKIP_INITIAL = False

    def __init__(self) -> None:
        self.keyboard = Controller()
        self.mouse = pyautogui
        self.console_commands_list = [
            # "sv_cheats 1;bot_kick;mp_limitteams 0;mp_autoteambalance 0;mp_roundtime 60;mp_roundtime_defuse 60;mp_freezetime 0;mp_warmup_end;ammo_grenade_limit_total 5;sv_infinite_ammo 1;mp_maxmoney 60000;mp_startmoney 60000;mp_buytime 9999;mp_buy_anywhere 1;mp_restartgame 1"
            "cl_showfps 0",
            "r_show_build_info false",
            "r_drawviewmodel false",
            "cl_drawhud 0",
        ]
        self.wait_time = 0.25 

    def run(self) -> None:
        self.ask_mapname()
        if self.SKIP_INITIAL == False:
            self.open_console()
            self.type_commands()
            self.close_console()
        self.rotate_camera()

    def ask_mapname(self) -> None:
        mapname = input("Mapname: ")
        if mapname != None or mapname != "":
            self.MAP_NAME = mapname
        else:
            raise Exception("Mapname is empty")

        skip_initial = input("Skip initial commands? (y/n): ")
        if skip_initial == "y":
            self.SKIP_INITIAL = True
        else:
            self.SKIP_INITIAL = False
        time.sleep(5)

    def open_console(self) -> None:
        self.keyboard.press('`')
        self.keyboard.release('`')
        time.sleep(0.25)

    def type_commands(self) -> None:
        for command in self.console_commands_list:
            self.keyboard.type(command)
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            time.sleep(1)

    def type_custom_command(self, command) -> None:
        self.keyboard.type(command)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        time.sleep(0.25)

    def close_console(self) -> None:
        self.keyboard.press('`')
        self.keyboard.release('`')
        time.sleep(0.25)

    def run_command(self, command):
        self.open_console()
        self.type_custom_command(command)
        self.close_console()

    def rotate_camera(self) -> None:
        degrees = 0
        for i in range(10):
            self.run_command(f"setang 0.0 {degrees} 0.0")
            self.make_screenshot()
            degrees += 36

    def make_screenshot(self):
        global IMAGE_ITIRATION
        if os.path.isdir(f"data/{self.MAP_NAME}") == False:
            os.mkdir(f"data/{self.MAP_NAME}")
        IMAGE_ITIRATION += 1 
        saveFileCWD = f"data/{self.MAP_NAME}/{IMAGE_ITIRATION}.png"
        pyautogui.screenshot(saveFileCWD)
        
        payload = {
            "file_name": saveFileCWD,
            "label": self.MAP_NAME,
        }
        
        self.append_csv(payload)
        time.sleep(0.5)

    def append_csv(self, payload):
        filename = "data/dataset.csv"
        writer = None
        
        # create data/dataset.csv if it doesn't exist, and append the given parameters to the dataframe
        if os.path.isfile("data/dataset.csv") == False:
            with open(filename, mode="w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "file_name",
                        "label"
                    ]
                )
        
        # append the given parameters to the csv file
        with open(filename, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    payload["file_name"],
                    payload["label"],
                ]
            )
        

if __name__ == "__main__":
    app = App()
    app.run()
    
    # wait for user to press enter key to run method again (for taking screenshots)
    while True:
        if keyboard.is_pressed("k"):
            app.rotate_camera()
            time.sleep(0.1)
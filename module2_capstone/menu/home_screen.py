from .screen import Screen
from .park_list import ParkListScreen


class HomeScreen(Screen):
    @property
    def user_input_prompt(self):
        return "Enter Any Value to Continue: "

    def display_main_screen(self):
        print(
            """
        
            ##    ##    ###    ######## ####  #######  ##    ##    ###    ##          ########     ###    ########  ##    ##  ######      ######     ###    ########   ######  ########  #######  ##    ## ######## 
            ###   ##   ## ##      ##     ##  ##     ## ###   ##   ## ##   ##          ##     ##   ## ##   ##     ## ##   ##  ##    ##    ##    ##   ## ##   ##     ## ##    ##    ##    ##     ## ###   ## ##       
            ####  ##  ##   ##     ##     ##  ##     ## ####  ##  ##   ##  ##          ##     ##  ##   ##  ##     ## ##  ##   ##          ##        ##   ##  ##     ## ##          ##    ##     ## ####  ## ##       
            ## ## ## ##     ##    ##     ##  ##     ## ## ## ## ##     ## ##          ########  ##     ## ########  #####     ######     ##       ##     ## ########   ######     ##    ##     ## ## ## ## ######   
            ##  #### #########    ##     ##  ##     ## ##  #### ######### ##          ##        ######### ##   ##   ##  ##         ##    ##       ######### ##              ##    ##    ##     ## ##  #### ##       
            ##   ### ##     ##    ##     ##  ##     ## ##   ### ##     ## ##          ##        ##     ## ##    ##  ##   ##  ##    ##    ##    ## ##     ## ##        ##    ##    ##    ##     ## ##   ### ##       
            ##    ## ##     ##    ##    ####  #######  ##    ## ##     ## ########    ##        ##     ## ##     ## ##    ##  ######      ######  ##     ## ##         ######     ##     #######  ##    ## ######## 

        """
        )

    @property
    def valid_user_input_strs(self) -> bool:
        return []

    @property
    def always_valid_user_str(self) -> bool:
        return True

    def do_action(self, user_input):
        # We don't do anything with the user input here.
        return ParkListScreen()

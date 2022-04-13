import os
import typing
from models import BaseModel
from datetime import datetime


# Our top level menu class that is inherited by all other menu classes
# This needs to have some sort of user input loop
# This needs to pass the user input to something that reads it.

# Our first screen is our list of Parks


class Screen:
    def clear_screen(self):
        command = "clear"
        if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
            command = "cls"
        os.system(command)

    @property
    def always_valid_user_str(self) -> bool:
        return False

    @property
    def valid_user_input_strs(self) -> typing.List[str]:
        raise NotImplementedError

    @property
    def user_input_prompt(self) -> str:
        raise NotImplementedError

    @property
    def model_object_list(self) -> typing.List[BaseModel]:
        raise NotImplementedError

    # Do the specified user action on whatever model
    # Then return the next screen the user should see.
    def do_action(self, user_input) -> object:
        raise NotImplementedError

    def display_main_screen(self):
        raise NotImplementedError

    def display_screen(self) -> None:
        self.clear_screen()
        self.display_main_screen()

    # Returns a bool depending on whether the input is valid. Define this on each screen class

    def validate_user_input(self, user_input, check_date=False) -> bool:
        # potential valid user inputs are, q, ints, names a whole bunch of things
        if check_date:
            try:
                datetime.strptime(user_input, "%Y-%m-%d").date()
            except ValueError:
                return False
            else:
                return True
        return (
            user_input in self.valid_user_input_strs
            or user_input == "q"
            or user_input == "quit"
            or self.always_valid_user_str
        )

    def handle_user_input(self) -> None:
        raise NotImplementedError

    def get_user_input(self, prompt=None, check_date=False, quit=True) -> str:
        if not prompt:
            prompt = self.user_input_prompt
        if quit:
            print("Type Q to quit:\n")
        valid_user_input = False
        clean_input = None
        while not valid_user_input:
            user_input = input(prompt)
            clean_input = user_input.strip().lower()
            valid_user_input = self.validate_user_input(clean_input, check_date)
            if not valid_user_input:
                print(f"\nSorry, but your input of {user_input} is not valid!")
        return clean_input

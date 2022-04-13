import enum
import typing
from .screen import Screen
from models import Park


class ParkListScreen(Screen):
    @property
    def user_input_prompt(self):
        return "Select a park from the list: "

    @property
    def model_object_list(self):
        parks = Park.query_all()
        return parks

    @property
    def valid_user_input_strs(self) -> typing.List[str]:
        valid_inputs = []
        for idx, park in enumerate(self.model_object_list):
            valid_inputs.append(park.park_name.lower())
            valid_inputs.append(str(idx + 1))
        return valid_inputs

    def do_action(self, user_input):
        from .park_detail import ParkDetailScreen

        # For this menu. Depending on the action string find the correct park.
        for idx, park in enumerate(self.model_object_list):
            if str(idx + 1) == user_input or park.park_name.lower() == user_input:
                return ParkDetailScreen(model=park)
        raise NotImplementedError("Somehow now a valid user input")

    def display_main_screen(self):
        print("---- National Parks ----")
        for idx, park in enumerate(self.model_object_list):
            print(f"\t{idx + 1}.) {park.park_name}")

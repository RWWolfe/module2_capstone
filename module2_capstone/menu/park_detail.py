from .screen_detail import ScreenDetail
from utilities import break_string_to_lines
import typing


class ParkDetailScreen(ScreenDetail):
    @property
    def user_input_prompt(self):
        return "Select a campground: "

    @property
    def model_object_list(self):
        return self.model.campgrounds

    @property
    def valid_user_input_strs(self) -> typing.List[str]:
        valid_inputs = []
        for idx, campground in enumerate(self.model_object_list):
            valid_inputs.append(campground.campground_name.lower())
            valid_inputs.append(str(idx + 1))

        valid_inputs.append("b")
        valid_inputs.append("back")
        valid_inputs.append("h")
        valid_inputs.append("home")
        return valid_inputs

    def do_action(self, user_input):
        from .park_list import ParkListScreen
        from .campground_detail import CampgroundDetailScreen

        # Now we have a list of action strings on valid_user_input_strs
        # For this menu. Depending on the action string find the correct park.
        new_screen = None
        for idx, campground in enumerate(self.model_object_list):
            if (
                str(idx + 1) == user_input
                or campground.campground_name.lower() == user_input
            ):
                return CampgroundDetailScreen(model=campground)
        new_screen = self.handle_back_and_home(
            user_input=user_input, BackScreenCls=ParkListScreen
        )
        if new_screen:
            return new_screen
        else:
            raise NotImplementedError("Somehow now a valid user input")

    def display_description_screen(self):
        print(f"---- {self.model.park_name} ----")
        print(
            f"""
            Location: {self.model.park_location}, 
            Established Date: {self.model.establish_date}, 
            Area: {self.model.area}sq. miles, 
            Average Visitors Per Year: {self.model.visitors}

            ---------------------------------------------------------------------------------
            {break_string_to_lines(self.model.description)}
            ---------------------------------------------------------------------------------

        """
        )

    def display_main_screen(self):
        print("\tSelect a Campground:")
        self.display_description_screen()
        for idx, campground in enumerate(self.model_object_list):
            print(f"\t\t{idx + 1}.) {campground.campground_name}")

        print("\t\tB.) Return to Parks List")
        print(f"\t\tH.) Return to Home Screen")

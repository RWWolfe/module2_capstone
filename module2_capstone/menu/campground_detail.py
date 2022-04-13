from .screen_detail import ScreenDetail
import typing


class CampgroundDetailScreen(ScreenDetail):
    @property
    def user_input_prompt(self):
        return "Select a Site to make a Reservation for: "

    @property
    def model_object_list(self):
        return self.model.campsites

    @property
    def valid_user_input_strs(self) -> typing.List[str]:
        valid_inputs = super().valid_user_input_strs
        for idx, site in enumerate(self.model_object_list):
            valid_inputs.append(f"site {str(site.site_number).lower()}")
            valid_inputs.append(str(idx + 1))
        return valid_inputs

    def do_action(self, user_input):
        from .park_detail import ParkDetailScreen
        from .create_reservation import CreateReservationScreen

        # Now we have a list of action strings on valid_user_input_strs
        # For this menu. Depending on the action string find the correct park.
        for idx, site in enumerate(self.model_object_list):
            if (
                str(idx + 1) == user_input
                or f"site {str(site.site_number).lower()}" == user_input
            ):
                return CreateReservationScreen(model=site)
        new_screen = self.handle_back_and_home(
            user_input=user_input,
            back_screen_model=self.model.park,
            BackScreenCls=ParkDetailScreen,
        )
        if new_screen:
            return new_screen
        else:
            raise NotImplementedError("Somehow now a valid user input")

    def display_description_screen(self):
        print(f"---- {self.model.campground_name} for {self.model.park.park_name} ----")
        print(
            f"""
            Open from: {self.model.open_from_mm.name}, 
            Open To: {self.model.open_to_mm.name}, 
            Daily Fee: ${self.model.daily_fee}
        """
        )

    def display_main_screen(self):
        self.display_description_screen()
        print(
            """
            -------------------------------------------------
            Select a Site: 
        """
        )
        for idx, site in enumerate(self.model_object_list):
            print(
                f"\t\t{idx + 1}.) Site {site.site_number} -- "
                + f"{'Wheel Chair Accessible -- ' if site.accessible else ''}"
                + f"{'Utilities available -- ' if site.utilities else ''}"
                + f"Max Occupancy: {site.max_occupancy} -- "
                + f"Max RV Length: {site.max_rv_length} Feet"
            )
        self.display_back_and_home()

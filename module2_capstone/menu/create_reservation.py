from .screen import Screen
from .screen_detail import ScreenDetail
from models.reservation import Reservation
from datetime import datetime


class CreateReservationScreen(ScreenDetail):
    def __init__(self, model):
        self.model = model

    @property
    def user_input_prompt(self):
        return "Name Your Reservation: "

    @property
    def model_object_list(self):
        return self.model.reservations

    @property
    def always_valid_user_str(self) -> bool:
        return True

    def do_action(self, user_input):
        from .campground_detail import CampgroundDetailScreen

        new_screen = self.handle_back_and_home(
            user_input=user_input,
            back_screen_model=self.model.campground,
            BackScreenCls=CampgroundDetailScreen,
        )
        if new_screen:
            return new_screen
        else:
            # We named the reservation. We need to set dates and confirm the dates are good
            return self.create_new_reservation(user_input)

    def create_new_reservation(self, name) -> Screen:
        from .park_list import ParkListScreen

        done_creating = False
        while not done_creating:
            starting_date = self.get_user_input(
                "Starting Date (YYYY-MM-DD):", True, False
            )
            ending_date = self.get_user_input("Ending Date (YYYY-MM-DD):", True, False)
            if (
                datetime.strptime(starting_date, "%Y-%m-%d").date()
                < datetime.strptime(ending_date, "%Y-%m-%d").date()
            ):
                if not (
                    self.model.campground.open_from_mm.value
                    <= datetime.strptime(starting_date, "%Y-%m-%d").date().month
                    and self.model.campground.open_to_mm.value
                    >= datetime.strptime(ending_date, "%Y-%m-%d").date().month
                ):
                    print(
                        f"Your reservation is not within the Campgrounds Accepted Time Period of {self.model.campground.open_from_mm.name} to {self.model.campground.open_to_mm.name}"
                    )
                elif (
                    datetime.strptime(starting_date, "%Y-%m-%d").date().year
                    != datetime.strptime(ending_date, "%Y-%m-%d").date().year
                ):
                    print(f"Your reservation must be contained within the same year.")
                elif (
                    datetime.now().date()
                    > datetime.strptime(starting_date, "%Y-%m-%d").date()
                ):
                    print(f"Your reservation must be in the future!.")
                else:
                    for resevation in self.model.reservations:
                        if (
                            datetime.strptime(starting_date, "%Y-%m-%d").date()
                            <= resevation.from_date
                            <= datetime.strptime(ending_date, "%Y-%m-%d").date()
                            or datetime.strptime(starting_date, "%Y-%m-%d").date()
                            <= resevation.to_date
                            <= datetime.strptime(ending_date, "%Y-%m-%d").date()
                        ):
                            print(
                                "Your reservation on this Site overlaps with someone else's! Please reschedule"
                            )
                            break

                    else:
                        new_reservation = Reservation.create_new_reservation_in_sql(
                            self.model.id, name, starting_date, ending_date
                        )
                        print(
                            f"Reservation Accepted and Saved! Confirmation Number: {new_reservation.id}"
                        )
                        input("Continue...?")
                        done_creating = True
            else:
                print("Start date cannot be after end date of reservation!")

        return ParkListScreen()

    def display_back_and_home(self):
        print(f"B.) Return to Previous Menu")
        print(f"H.) Return to Home Screen")

    def display_main_screen(self):
        from .park_detail import ParkDetailScreen
        from .campground_detail import CampgroundDetailScreen

        ParkDetailScreen(self.model.campground.park).display_description_screen()
        CampgroundDetailScreen(self.model.campground).display_description_screen()
        for idx, reservation in enumerate(self.model.reservations):
            print(
                f"\t{idx + 1}.) {reservation.reservation_name} -- {reservation.from_date}/{reservation.to_date}"
            )
        print(f"--- Create a new Reservation For Site {self.model.site_number}")
        self.display_back_and_home()

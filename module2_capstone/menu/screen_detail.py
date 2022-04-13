from .screen import Screen
import typing


class ScreenDetail(Screen):
    def __init__(self, model):
        self.model = model

    @property
    def user_input_prompt(self):
        raise NotImplementedError

    @property
    def model_object_list(self):
        raise NotImplementedError

    @property
    def valid_user_input_strs(self) -> typing.List[str]:
        valid_inputs = []
        valid_inputs.append("b")
        valid_inputs.append("back")
        valid_inputs.append("h")
        valid_inputs.append("home")
        return valid_inputs

    def handle_back_and_home(
        self, user_input, BackScreenCls, back_screen_model=None
    ) -> Screen:
        from .home_screen import HomeScreen

        if user_input == "b" or user_input == "back":
            if back_screen_model:
                return BackScreenCls(model=back_screen_model)
            else:
                return BackScreenCls()
        if user_input == "h" or user_input == "home":
            return HomeScreen()

    def display_description_screen(self):
        raise NotImplementedError

    def display_back_and_home(self):
        print(f"\t\tB.) Return to Previous Menu")
        print(f"\t\tH.) Return to Home Screen")

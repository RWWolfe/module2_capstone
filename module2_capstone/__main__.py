from menu import HomeScreen

# How is a __main__.py structured?
# define a main function which starts your application
# invoke your main funciton. That's it


def main():
    # Flow for application menuing ===> Display -> Prompt User Input -> Action -> New Display -> ...
    quit = False
    current_screen = HomeScreen()
    while not quit:
        # Step 1 -- Display Screen
        current_screen.display_screen()

        # Step 2 -- Prompt User Input -- This input will be all lowercase and cleaned and validated
        cleaned_and_validated_user_input = current_screen.get_user_input()

        # Step 3 -- Do an Action with the User Input

        if (
            cleaned_and_validated_user_input == "q"
            or cleaned_and_validated_user_input == "quit"
        ):
            quit = True
        else:
            current_screen = current_screen.do_action(cleaned_and_validated_user_input)

        # After we've done our action. We need to do the new display
        # Make sure a new screen is set
    else:
        print("Thanks for stopping by at our National Park Reservation App")


main()

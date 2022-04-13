import sqlalchemy as sa
from sqlalchemy.sql import text
import typing
from park import Park
from campground import Campground
from campsite import Site
from reservation import Reservation
from db.connect import db
from datetime import datetime


parks = Park.query_all()
campgrounds = Campground.query_all()
sites = Site.query_all()
reservations = Reservation.query_all()


user_input = None
done = None
while not done:
    print("Select a park: ")
    for idx, park in enumerate(parks):
        print(f"{idx + 1}.) {park.park_name}")

    user_input = input('Select park by number or enter D for more details, R to make a reservation, or Q to quit: ').strip().lower()

    if user_input and user_input[0] == 'd':
        for idx, park in enumerate(parks):
            print(f"\n{idx + 1}.) ID#{park.park_id}, {park.park_name}, {park.park_location}, {park.establish_date}, {park.area}sq. miles, {park.visitors} average visitors per year. {park.description}")

    if user_input and user_input[0] == 'q':
        break

    if user_input and user_input[0] == 'r':
        done = None
        while not done: 
            user_camp = input('Enter a campground: ').strip()

            for campground in campgrounds:
                if user_camp == campground.campground_name:
                    user_from = input('Enter a starting date yyyy-mm-dd: ').strip()
                    user_to = input('Enter an ending date yyyy-mm-dd: ').strip()

                    if campground.open_from_mm <= datetime.strptime(user_from, '%Y-%m-%d').date() and campground.open_to_mm >= datetime.strptime(user_to, '%Y-%m-%d').date():
                        for idx, site in enumerate(campground.campsites):
                            print(f'\n{idx + 1}.) Site:{site.site_id} Status:')

                        user_site_id = input('Choose a site: ')
                        for site in sites:
                            if site.site_id == int(user_site_id):
                                user_res_name = input('Enter the name for your reservation: ')
                                user_reservation = Reservation.create_new_reservation_in_sql(site.site_id, user_res_name, user_from, user_to)
                                print(f'Reservation made for {user_reservation.reservation_name} at {campground.campground_name}, Site: {site.site_number} on {user_reservation.from_date}, until {user_reservation.to_date}.\n Confirmation id:{user_reservation.reservation_id} ')

                    else:
                        user_input  = input('Invalid time. Would you like to enter an alternate date range? y/n: ').strip().lower()
                        if user_input and user_input[0] == 'n':
                            done = True
                        else:
                            pass
        
            else:
                user_input  = input('Invalid campground. Would you like to enter an alternate date range? y/n: ').strip().lower()
                if user_input and user_input[0] == 'n':
                    done = True
                else:
                    pass
    
    else:
        chosen_park = parks[int(user_input) - 1]

        print(f'You have chosen {chosen_park.park_name}.')

        for idx, campground in enumerate(chosen_park.campgrounds):
            print(f"{idx + 1}.) {campground.campground_name}")
        
        user_input = input('Select a campground by number or enter D for more details: ').strip().lower()
        
        if user_input and user_input[0] == 'd':
           for idx, campground in enumerate(chosen_park.campgrounds):
               print(f"\n{idx + 1}.) ID#{campground.campground_id}, {campground.campground_name}, Open from {campground.open_from_mm} until {campground.open_to_mm}, ${campground.daily_fee}")
        else:
            chosen_campground = chosen_park.campgrounds[int(user_input) - 1]

            print(f'You have chosen {chosen_campground.campground_name}.')

            for idx, campsite in enumerate(chosen_campground.campsites):
                print(f"\n{idx + 1}.) Site: {campsite.site_number}, Max Occupancy: {campsite.max_occupancy}, Maximum RV Length: {campsite.max_rv_length} feet.")
                if campsite.accessible:
                    print("Wheelchair accessible.")
                else:
                    print('Not wheelchair accessible.')
                if campsite.utilities:
                    print('Utilities available.')
                else:
                    print('No utilities available.')






                 #   user_input = input('Time slot is available! Would you like to make a reservation? y/n: ').strip().lower()
                 #       if user_input and user_input[0] == 'y':
                 #           user_reservation_name = input('Enter a name for your reservation: ')
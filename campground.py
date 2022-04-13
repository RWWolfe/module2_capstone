import sqlalchemy as sa
from sqlalchemy.sql import text
import typing
from db.connect import db


class Campground:
    def __init__ (self, campground_id, park_id, campground_name, open_from_mm, open_to_mm, daily_fee):
        self.campground_id = campground_id
        self.park_id = park_id
        self.campground_name = campground_name
        self.open_from_mm = open_from_mm
        self.open_to_mm = open_to_mm
        self.daily_fee = daily_fee

    @property
    def campsites(self) -> typing.List[object]:
        from campsite import Site
        campsites_results = db.execute(f"""
            SELECT site.site_id, site.campground_id, site_number, max_occupancy, accessible, max_rv_length, utilities
            FROM module2.site
            JOIN module2.campground ON module2.site.campground_id = module2.campground.campground_id
            WHERE {self.campground_id} = module2.campground.campground_id
        """)

        campsites = []
        for campsite in campsites_results.all():
            campsites.append(Site(campsite.site_id, campsite.campground_id, campsite.site_number, campsite.max_occupancy, campsite.accessible, campsite.max_rv_length, campsite.utilities))
        return campsites
   

    @classmethod
    def query_all(cls) -> typing.List[object]:

        campgrounds_all_result = db.execute("""
        SELECT campground.campground_id, campground.park_id, campground_name, open_from_mm, open_to_mm, daily_fee
        FROM module2.campground;
        """)

        campgrounds_all = []
        for campground in campgrounds_all_result.all():
            campgrounds_all.append(
                cls(
                    campground_id = campground.campground_id,
                    park_id = campground.park_id,
                    campground_name = campground.campground_name,
                    open_from_mm = campground.open_from_mm,
                    open_to_mm = campground.open_to_mm,
                    daily_fee = campground.daily_fee
                )
            )
        return campgrounds_all

    
  
  
  
  
  
  
    #def availability(self, user_from_date, user_to_date):
    #    open_from_int = None
    #    open_to_int = None
    #    
    #    for month in self.open_from_mm:
    #        if month == "JAN":
    #            open_from_int = 1
    #        if month == "FEB":
    #            open_from_int = 2
    #        if month == 'MAR':
    #            open_from_int = 3
    #        if month == 'APR':
    #            open_from_int = 4
    #        if month == 'MAY':
    #            open_from_int = 5
    #        if month == 'JUN':
    #            open_from_int = 6
    #        if month == 'JUL':
    #            open_from_int = 7
    #        if month == 'AUG':
    #            open_from_int = 8
    #        if month == 'SEP':
    #            open_from_int = 9
    #        if month == 'OCT':
    #            open_from_int = 10
    #        if month == 'NOV':
    #            open_from_int = 11
    #        if month == 'DEC':
    #            open_from_int = 12
#
    #    for month in self.open_to_mm:
    #        if month == "JAN":
    #            open_from_int = 1
    #        if month == "FEB":
    #            open_from_int = 2
    #        if month == 'MAR':
    #            open_from_int = 3
    #        if month == 'APR':
    #            open_from_int = 4
    #        if month == 'MAY':
    #            open_from_int = 5
    #        if month == 'JUN':
    #            open_from_int = 6
    #        if month == 'JUL':
    #            open_from_int = 7
    #        if month == 'AUG':
    #            open_from_int = 8
    #        if month == 'SEP':
    #            open_from_int = 9
    #        if month == 'OCT':
    #            open_from_int = 10
    #        if month == 'NOV':
    #            open_from_int = 11
    #        if month == 'DEC':
    #            open_from_int = 12
#
#
#
#
    #    if user_from_date.strip().lower() >= open_from_int and user_to_date.strip().lower() <= open_to_int:
    #        print('Available.')
    #    else:
    #        print('Unavailable.')
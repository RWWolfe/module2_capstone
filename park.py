import sqlalchemy as sa
from sqlalchemy.sql import text
import typing
from db.connect import db


class Park:
    def __init__ (self, park_id, park_name, park_location, establish_date, area, visitors, description):
        self.park_id = park_id
        self.park_name = park_name
        self.park_location = park_location
        self.establish_date = establish_date
        self.area = area
        self.visitors = visitors
        self.description = description


    @property
    def campgrounds(self) -> typing.List[object]:
        from campground import Campground
        campground_result = db.execute(f"""
        SELECT campground.campground_id, campground.park_id, campground_name, open_from_mm, open_to_mm, daily_fee
        FROM module2.campground
        JOIN module2.park ON module2.park.park_id = module2.campground.park_id
        WHERE {self.park_id} = module2.park.park_id
        ;
        """)
        campgrounds =[]
        for campground in campground_result.all():
            campgrounds.append(Campground(campground.campground_id, campground.park_id, campground.campground_name, campground.open_from_mm, campground.open_to_mm, campground.daily_fee))
        return campgrounds
    
    @classmethod
    def query_all(cls) -> typing.List[object]:

        parks_all_result = db.execute("""
        SELECT park.park_id, park_name, park_location, establish_date, area, visitors, description
        FROM module2.park
        ORDER BY park_name ASC;
        """)

        parks_all = []
        for park in parks_all_result.all():
            parks_all.append(
                cls(
                    park_id = park.park_id,
                    park_name = park.park_name,
                    park_location = park.park_location,
                    establish_date = park.establish_date,
                    area = park.area,
                    visitors = park.visitors,
                    description = park.description
                )
            )
        return parks_all
            
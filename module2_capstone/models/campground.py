from sqlalchemy.sql import text
import typing
from db.connect import db
from .base import BaseModel
from .enums import Month


class Campground(BaseModel):
    def __init__(
        self,
        campground_id,
        park_id,
        campground_name,
        open_from_mm,
        open_to_mm,
        daily_fee,
    ):
        self.campground_id = campground_id
        self.park_id = park_id
        self.campground_name = campground_name
        self._open_from_mm = open_from_mm
        self._open_to_mm = open_to_mm
        self.daily_fee = daily_fee

    @property
    def id(self):
        return self.campground_id

    @property
    def open_from_mm(self) -> Month:
        return Month[self._open_from_mm]

    @property
    def open_to_mm(self) -> Month:
        return Month[self._open_to_mm]

    @property
    def campsites(self) -> typing.List[object]:
        from models.campsite import Site

        campsites_results = db.execute(
            text(
                """
            SELECT site.site_id, site.campground_id, site_number, max_occupancy, accessible, max_rv_length, utilities
            FROM module2.site
            JOIN module2.campground ON module2.site.campground_id = module2.campground.campground_id
            WHERE :campground_id = module2.campground.campground_id
        """
            ),
            campground_id=self.campground_id,
        )

        campsites = []
        for campsite in campsites_results.all():
            campsites.append(
                Site(
                    campsite.site_id,
                    campsite.campground_id,
                    campsite.site_number,
                    campsite.max_occupancy,
                    campsite.accessible,
                    campsite.max_rv_length,
                    campsite.utilities,
                )
            )
        return campsites

    @property
    def park(self):
        from models.park import Park

        park_result = db.execute(
            text(
                """
            SELECT park.park_id, park_name, park_location, establish_date, area, visitors, description
            FROM module2.park
            WHERE :park_id = module2.park.park_id;
        """
            ),
            park_id=self.park_id,
        )
        park_row = park_result.one_or_none()
        if park_row:
            return Park(
                park_id=park_row.park_id,
                park_name=park_row.park_name,
                park_location=park_row.park_location,
                establish_date=park_row.establish_date,
                area=park_row.area,
                visitors=park_row.visitors,
                description=park_row.description,
            )
        else:
            return None

    @classmethod
    def query_all(cls) -> typing.List[object]:

        campgrounds_all_result = db.execute(
            """
            SELECT campground.campground_id, campground.park_id, campground_name, open_from_mm, open_to_mm, daily_fee
            FROM module2.campground;
        """
        )

        campgrounds_all = []
        for campground in campgrounds_all_result.all():
            campgrounds_all.append(
                cls(
                    campground_id=campground.campground_id,
                    park_id=campground.park_id,
                    campground_name=campground.campground_name,
                    open_from_mm=campground.open_from_mm,
                    open_to_mm=campground.open_to_mm,
                    daily_fee=campground.daily_fee,
                )
            )
        return campgrounds_all

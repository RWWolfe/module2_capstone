from sqlalchemy.sql import text
import typing
from db.connect import db
from .base import BaseModel


class Site(BaseModel):
    def __init__(
        self,
        site_id,
        campground_id,
        site_number,
        max_occupancy,
        accessible,
        max_rv_length,
        utilities,
    ):
        self.site_id = site_id
        self.campground_id = campground_id
        self.site_number = site_number
        self.max_occupancy = max_occupancy
        self.accessible = accessible
        self.max_rv_length = max_rv_length
        self.utilities = utilities

    @property
    def id(self):
        return self.site_id

    @property
    def campground(self):
        from models.campground import Campground

        campground_result = db.execute(
            text(
                """
            SELECT campground_id, park_id, campground_name, open_from_mm, open_to_mm, daily_fee
            FROM module2.campground
            WHERE :campground_id = module2.campground.campground_id;
        """
            ),
            campground_id=self.campground_id,
        )
        campground_row = campground_result.one_or_none()
        if campground_row:
            return Campground(
                campground_id=campground_row.campground_id,
                park_id=campground_row.park_id,
                campground_name=campground_row.campground_name,
                open_from_mm=campground_row.open_from_mm,
                open_to_mm=campground_row.open_to_mm,
                daily_fee=campground_row.daily_fee,
            )
        else:
            return None

    @property
    def reservations(self) -> typing.List[object]:
        from models.reservation import Reservation

        reservations_result = db.execute(
            text(
                """
            SELECT reservation.reservation_id, reservation.site_id, reservation_name, from_date, to_date, create_date
            FROM module2.reservation
            JOIN module2.site ON module2.site.site_id = module2.reservation.site_id
            WHERE :site_id = module2.reservation.site_id
        """
            ),
            site_id=self.site_id,
        )
        reservations = []
        for reservation in reservations_result.all():
            reservations.append(
                Reservation(
                    reservation.reservation_id,
                    reservation.site_id,
                    reservation.reservation_name,
                    reservation.from_date,
                    reservation.to_date,
                    reservation.create_date,
                )
            )
        return reservations

    @classmethod
    def query_all(cls) -> typing.List[object]:

        sites_all_result = db.execute(
            """
            SELECT site.site_id, site.campground_id, site_number, max_occupancy, accessible, max_rv_length, utilities
            FROM module2.site;
        """
        )

        sites_all = []
        for site in sites_all_result.all():
            sites_all.append(
                cls(
                    site_id=site.site_id,
                    campground_id=site.campground_id,
                    site_number=site.site_number,
                    max_occupancy=site.max_occupancy,
                    accessible=site.accessible,
                    max_rv_length=site.max_rv_length,
                    utilities=site.utilities,
                )
            )
        return sites_all

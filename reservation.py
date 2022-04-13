import sqlalchemy as sa
from sqlalchemy.sql import text
import typing
from db.connect import db

class Reservation:
    def __init__ (self, reservation_id, site_id, reservation_name, from_date, to_date, create_date):
        self.reservation_id = reservation_id
        self.site_id = site_id
        self.reservation_name = reservation_name
        self.from_date = from_date
        self.to_date = to_date
        self.create_date = create_date


    @property
    def campsite(self):
        from campsite import Site
        campsite_result = db.execute(f"""
        SELECT reservation.reservation_id, reservation.site_id, site.campground_id, site.site_number, site.max_occupancy, site.accessible, site.max_rv_length, site.utilities
        FROM module2.reservation
        JOIN module2.site ON module2.reservation.site_id = module2.site.site_id
        WHERE {self.site_id} = module2.reservation.site_id
        ;
        """)
        campsite_row = campsite_result.one_or_none()
        if campsite_row:
            return Site(site_id = campsite_row.site_id, campground_id = campsite_row.campground_id, site_number = campsite_row.site_number, max_occupancy = campsite_row.max_occupancy, accessible = campsite_row.accessible, max_rv_length = campsite_row.max_rv_length, utilities = campsite_row.utilities)
        else:
            return None
    
    
    @classmethod
    def query_all(cls) -> typing.List[object]:

        reservations_all_result = db.execute("""
        SELECT reservation_id, reservation.site_id, reservation_name, from_date, to_date, create_date
        FROM module2.reservation
        """)

        reservations_all = []
        for reservation in reservations_all_result.all():
            reservations_all.append(
                cls(
                    reservation_id = reservation.reservation_id,
                    site_id = reservation.site_id,
                    reservation_name = reservation.reservation_name,
                    from_date = reservation.from_date,
                    to_date = reservation.to_date,
                    create_date = reservation.create_date
                )
            )
        return reservations_all

    @classmethod
    def create_new_reservation_in_sql(cls, site_id, reservation_name, from_date, to_date):
        
        new_reservation = db.execute(text("""
        INSERT INTO module2.reservation (site_id, reservation_name, from_date, to_date)
        VALUES (:site_id, :reservation_name, :from_date, :to_date)
        RETURNING *;
        """), site_id = site_id, reservation_name = reservation_name, from_date = from_date, to_date = to_date)

        res = new_reservation.one()
        reservation = cls(res.reservation_id, res.site_id, res.reservation_name, res.from_date, res.to_date, res.create_date)
        return reservation
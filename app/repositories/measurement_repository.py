from sqlalchemy.orm import Session

from app.core.enums import Status
from app.models.measurement import Measurement
from app.models.measurement_item import MeasurementItem


class MeasurementRepository:

    # =====================================================
    # Measurement
    # =====================================================

    def create(
        self,
        db: Session,
        measurement: Measurement,
    ) -> Measurement:

        db.add(measurement)
        db.commit()
        db.refresh(measurement)

        return measurement

    def update(
        self,
        db: Session,
        measurement: Measurement,
    ) -> Measurement:

        db.commit()
        db.refresh(measurement)

        return measurement

    def get_by_id(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
        any_status: bool = False,
    ) -> Measurement | None:

        query = (
            db.query(Measurement)
            .filter(
                Measurement.company_id == company_id,
                Measurement.id == measurement_id,
            )
        )

        if not any_status:
            query = query.filter(
                Measurement.status == Status.ACTIVE,
            )

        return query.first()

    def get_by_project(
        self,
        db: Session,
        company_id: int,
        project_id: int,
        any_status: bool = False,
    ) -> list[Measurement]:

        query = (
            db.query(Measurement)
            .filter(
                Measurement.company_id == company_id,
                Measurement.project_id == project_id,
            )
        )

        if not any_status:
            query = query.filter(
                Measurement.status == Status.ACTIVE,
            )

        return (
            query
            .order_by(
                Measurement.id.asc(),
            )
            .all()
        )

    def get_last_measurement(
        self,
        db: Session,
    ) -> Measurement | None:

        return (
            db.query(Measurement)
            .order_by(
                Measurement.id.desc(),
            )
            .first()
        )

    def deactivate(
        self,
        db: Session,
        measurement: Measurement,
    ) -> Measurement:

        measurement.status = Status.INACTIVE

        db.commit()
        db.refresh(measurement)

        return measurement

    def restore(
        self,
        db: Session,
        measurement: Measurement,
    ) -> Measurement:

        measurement.status = Status.ACTIVE

        db.commit()
        db.refresh(measurement)

        return measurement

    # =====================================================
    # Measurement Items
    # =====================================================

    def create_item(
        self,
        db: Session,
        item: MeasurementItem,
    ) -> MeasurementItem:

        db.add(item)
        db.commit()
        db.refresh(item)

        return item

    def update_item(
        self,
        db: Session,
        item: MeasurementItem,
    ) -> MeasurementItem:

        db.commit()
        db.refresh(item)

        return item

    def get_item_by_id(
        self,
        db: Session,
        company_id: int,
        item_id: int,
        any_status: bool = False,
    ) -> MeasurementItem | None:

        query = (
            db.query(MeasurementItem)
            .join(Measurement)
            .filter(
                Measurement.company_id == company_id,
                MeasurementItem.id == item_id,
            )
        )

        if not any_status:
            query = query.filter(
                MeasurementItem.status == Status.ACTIVE,
            )

        return query.first()

    def get_items(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
        any_status: bool = False,
    ) -> list[MeasurementItem]:

        query = (
            db.query(MeasurementItem)
            .join(Measurement)
            .filter(
                Measurement.company_id == company_id,
                Measurement.id == measurement_id,
            )
        )

        if not any_status:
            query = query.filter(
                MeasurementItem.status == Status.ACTIVE,
            )

        return (
            query
            .order_by(
                MeasurementItem.id.asc(),
            )
            .all()
        )

    def deactivate_item(
        self,
        db: Session,
        item: MeasurementItem,
    ) -> MeasurementItem:

        item.status = Status.INACTIVE

        db.commit()
        db.refresh(item)

        return item

    def restore_item(
        self,
        db: Session,
        item: MeasurementItem,
    ) -> MeasurementItem:

        item.status = Status.ACTIVE

        db.commit()
        db.refresh(item)

        return item
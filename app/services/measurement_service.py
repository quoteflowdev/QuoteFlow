from app.core.calculations import CALCULATORS
from sqlalchemy.orm import Session

from app.models.measurement import Measurement
from app.models.measurement_item import MeasurementItem

from app.repositories.measurement_repository import MeasurementRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.project_repository import ProjectRepository

from app.schemas.measurement import (
    MeasurementCreate, MeasurementItemCreate, MeasurementItemUpdate, MeasurementUpdate,)


class MeasurementService:

    def __init__(self):

        self.measurement_repository = MeasurementRepository()
        self.project_repository = ProjectRepository()
        self.product_repository = ProductRepository()

    # =====================================================
    # Private
    # =====================================================

    def _generate_measurement_code(
        self,
        db: Session,
    ) -> str:

        last = self.measurement_repository.get_last_measurement(db)

        if last is None:
            return "MSR000001"

        number = int(
            last.measurement_code.replace(
                "MSR",
                "",
            )
        ) + 1

        return f"MSR{number:06d}"

    def _calculate_item(
        self,
        measurement: Measurement,
        item: MeasurementItem,
    ):

        calculator = CALCULATORS[
            measurement.product.calculation_type
        ]

        result = calculator.calculate(item)

        item.unit_value = result.unit_value
        item.calculated_value = result.total_value

    # =====================================================
    # Measurement
    # =====================================================

    def create_measurement(
        self,
        db: Session,
        company_id: int,
        request: MeasurementCreate,
    ):

        project = self.project_repository.get_project_by_id(
            db,
            company_id,
            request.project_id,
        )

        if project is None:
            raise ValueError("Project not found.")

        product = self.product_repository.get_product_by_id(
            db,
            company_id,
            request.product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        measurement = Measurement(

            company_id=company_id,

            project_id=request.project_id,

            product_id=request.product_id,

            measurement_code=self._generate_measurement_code(
                db
            ),

            measurement_name=request.measurement_name,

            created_by=None,
            updated_by=None,
            version=1,
        )

        return self.measurement_repository.create(
            db,
            measurement,
        )

    def get_measurements_by_project(
        self,
        db: Session,
        company_id: int,
        project_id: int,
    ):

        return self.measurement_repository.get_by_project(
            db,
            company_id,
            project_id,
        )

    def get_measurement_details(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
    ):

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            measurement_id,
        )

        if measurement is None:
            return None

        measurement.product = (
            self.product_repository.get_product_by_id(
                db,
                company_id,
                measurement.product_id,
            )
        )

        measurement.items = (
            self.measurement_repository.get_items(
                db,
                company_id,
                measurement.id,
            )
        )

        return measurement

    def update_measurement(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
        request: MeasurementUpdate,
    ):

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            measurement_id,
        )

        if measurement is None:
            return None

        data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in data.items():

            setattr(
                measurement,
                key,
                value,
            )

        measurement.version += 1

        return self.measurement_repository.update(
            db,
            measurement,
        )

    def change_measurement_status(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
        active: bool,
    ):

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            measurement_id,
            any_status=True,
        )

        if measurement is None:
            return None

        if active:

            return self.measurement_repository.restore(
                db,
                measurement,
            )

        return self.measurement_repository.deactivate(
            db,
            measurement,
        )

# =====================================================
    # Measurement Items
    # =====================================================

    def add_measurement_item(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
        request: MeasurementItemCreate,
    ):

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            measurement_id,
        )

        if measurement is None:
            raise ValueError("Measurement not found.")

        product = self.product_repository.get_product_by_id(
            db,
            company_id,
            measurement.product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        measurement.product = product

        item = MeasurementItem(

            measurement_id=measurement.id,

            location=request.location,

            height_feet=request.height_feet,
            height_inch=request.height_inch,

            width_feet=request.width_feet,
            width_inch=request.width_inch,

            length_feet=request.length_feet,
            length_inch=request.length_inch,

            quantity=request.quantity,

            remarks=request.remarks,

            created_by=None,
            updated_by=None,

            version=1,
        )

        self._calculate_item(
            measurement,
            item,
        )

        return self.measurement_repository.create_item(
            db,
            item,
        )

    def update_measurement_item(
        self,
        db: Session,
        company_id: int,
        item_id: int,
        request: MeasurementItemUpdate,
    ):

        item = self.measurement_repository.get_item_by_id(
            db,
            company_id,
            item_id,
        )

        if item is None:
            return None

        data = request.model_dump(
            exclude_unset=True,
        )

        for key, value in data.items():

            setattr(
                item,
                key,
                value,
            )

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            item.measurement_id,
        )

        if measurement is None:
            raise ValueError("Measurement not found.")

        product = self.product_repository.get_product_by_id(
            db,
            company_id,
            measurement.product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        measurement.product = product

        self._calculate_item(
            measurement,
            item,
        )

        item.version += 1

        return self.measurement_repository.update_item(
            db,
            item,
        )

    def change_measurement_item_status(
        self,
        db: Session,
        company_id: int,
        item_id: int,
        active: bool,
    ):

        item = self.measurement_repository.get_item_by_id(
            db,
            company_id,
            item_id,
            any_status=True,
        )

        if item is None:
            return None

        if active:

            return self.measurement_repository.restore_item(
                db,
                item,
            )

        return self.measurement_repository.deactivate_item(
            db,
            item,
        )

    def get_measurement_items(
        self,
        db: Session,
        company_id: int,
        measurement_id: int,
    ):

        measurement = self.measurement_repository.get_by_id(
            db,
            company_id,
            measurement_id,
        )

        if measurement is None:
            return None

        return self.measurement_repository.get_items(
            db,
            company_id,
            measurement_id,
        )
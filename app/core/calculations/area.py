from app.core.calculations.base import (
    BaseCalculation,
    CalculationResult,
)
from app.core.utils.measurement import MeasurementUtils
from app.models.measurement_item import MeasurementItem


class AreaCalculation(BaseCalculation):

    def calculate(
        self,
        item: MeasurementItem,
    ) -> CalculationResult:

        height = MeasurementUtils.feet_inch_to_feet(
            item.height_feet,
            item.height_inch,
        )

        width = MeasurementUtils.feet_inch_to_feet(
            item.width_feet,
            item.width_inch,
        )

        unit_value = round(
            height * width,
            2,
        )

        total_value = MeasurementUtils.multiply(
            unit_value,
            item.quantity,
        )

        return CalculationResult(
            unit_value=unit_value,
            total_value=total_value,
        )
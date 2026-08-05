from app.core.calculations.base import (
    BaseCalculation,
    CalculationResult,
)
from app.core.utils.measurement import MeasurementUtils
from app.models.measurement_item import MeasurementItem


class RunningCalculation(BaseCalculation):

    def calculate(
        self,
        item: MeasurementItem,
    ) -> CalculationResult:

        unit_value = MeasurementUtils.feet_inch_to_feet(
            item.length_feet,
            item.length_inch,
        )

        total_value = MeasurementUtils.multiply(
            unit_value,
            item.quantity,
        )

        return CalculationResult(
            unit_value=round(unit_value, 2),
            total_value=total_value,
        )
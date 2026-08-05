from app.core.calculations.base import (
    BaseCalculation,
    CalculationResult,
)
from app.models.measurement_item import MeasurementItem


class CountCalculation(BaseCalculation):

    def calculate(
        self,
        item: MeasurementItem,
    ) -> CalculationResult:

        unit_value = 1

        total_value = item.quantity

        return CalculationResult(
            unit_value=unit_value,
            total_value=float(total_value),
        )
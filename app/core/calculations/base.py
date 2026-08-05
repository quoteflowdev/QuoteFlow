from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.models.measurement_item import MeasurementItem


@dataclass
class CalculationResult:

    unit_value: float
    total_value: float


class BaseCalculation(ABC):

    @abstractmethod
    def calculate(
        self,
        item: MeasurementItem,
    ) -> CalculationResult:
        """
        Returns:

        unit_value  -> Single Piece Result

        total_value -> Final Result (Unit × Qty)
        """
        pass
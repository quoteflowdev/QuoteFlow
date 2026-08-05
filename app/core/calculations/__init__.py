from app.core.enums import CalculationType

from app.core.calculations.area import AreaCalculation
from app.core.calculations.running import RunningCalculation
from app.core.calculations.count import CountCalculation


CALCULATORS = {
    CalculationType.AREA: AreaCalculation(),
    CalculationType.RUNNING: RunningCalculation(),
    CalculationType.COUNT: CountCalculation(),
}
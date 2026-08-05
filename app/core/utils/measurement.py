from math import floor


class MeasurementUtils:

    @staticmethod
    def feet_inch_to_feet(
        feet: int | None,
        inch: float | None,
    ) -> float:

        feet = feet or 0
        inch = inch or 0

        return round(
            feet + (inch / 12),
            4,
        )

    @staticmethod
    def feet_to_feet_inch(
        value: float,
    ) -> tuple[int, float]:

        feet = floor(value)

        inch = round(
            (value - feet) * 12,
            2,
        )

        if inch == 12:

            feet += 1
            inch = 0

        return feet, inch

    @staticmethod
    def format_size(
        feet: int | None,
        inch: float | None,
    ) -> str:

        feet = feet or 0
        inch = inch or 0

        if inch == 0:
            return f"{feet}'"

        return f"{feet}' {inch}\""

    @staticmethod
    def multiply(
        value: float,
        quantity: int,
    ) -> float:

        return round(
            value * quantity,
            2,
        )
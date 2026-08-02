from enum import Enum


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CalculationType(str, Enum):
    AREA = "AREA"
    RUNNING = "RUNNING"
    COUNT = "COUNT"


class Unit(str, Enum):
    SQFT = "SQFT"
    SQM = "SQM"
    RFT = "RFT"
    METER = "METER"
    NOS = "NOS"


class ProjectStatus(str, Enum):
    NEW = "NEW"
    MEASUREMENT = "MEASUREMENT"
    QUOTATION = "QUOTATION"
    APPROVED = "APPROVED"
    WORK_STARTED = "WORK_STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PARTIAL = "PARTIAL"
    PAID = "PAID"
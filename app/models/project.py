from sqlalchemy import (Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String,)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import (ProjectStatus, Status,)
from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    project_code = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    project_name = Column(
        String(150),
        nullable=False,
    )

    site_address = Column(
        String(500),
        nullable=False,
    )

    site_contact_name = Column(
        String(100),
        nullable=True,
    )

    site_contact_number = Column(
        String(20),
        nullable=True,
    )

    remarks = Column(
        String(500),
        nullable=True,
    )

    project_status = Column(
        SqlEnum(ProjectStatus),
        nullable=False,
        default=ProjectStatus.NEW,
    )

    status = Column(
        SqlEnum(Status),
        nullable=False,
        default=Status.ACTIVE,
        index=True,
    )

    created_by = Column(
        Integer,
        nullable=True,
    )

    updated_by = Column(
        Integer,
        nullable=True,
    )

    version = Column(
        Integer,
        nullable=False,
        default=1,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    company = relationship(
        "Company",
        foreign_keys=[company_id],
        back_populates="projects",
    )

    customer = relationship(
        "Customer",
        foreign_keys=[customer_id],
        back_populates="projects",
    )

    measurements = relationship(
        "Measurement",
        back_populates="project",
        cascade="all, delete-orphan",
    )
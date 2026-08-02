from sqlalchemy.orm import Session

from app.core.enums import (
    CalculationType,
    Status,
    Unit,
)
from app.models.product import Product


DEFAULT_PRODUCTS = [
    {
        "name": "Window",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "window",
    },
    {
        "name": "Door",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "door",
    },
    {
        "name": "Glass",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "glass",
    },
    {
        "name": "Curtain",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "curtain",
    },
    {
        "name": "Railing",
        "type": CalculationType.RUNNING,
        "unit": Unit.RFT,
        "allow_decimal": True,
        "icon": "railing",
    },
    {
        "name": "Pipe",
        "type": CalculationType.RUNNING,
        "unit": Unit.RFT,
        "allow_decimal": True,
        "icon": "pipe",
    },
    {
        "name": "Wire",
        "type": CalculationType.RUNNING,
        "unit": Unit.RFT,
        "allow_decimal": True,
        "icon": "wire",
    },
    {
        "name": "Tiles",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "tiles",
    },
    {
        "name": "Granite",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "granite",
    },
    {
        "name": "Marble",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "marble",
    },
    {
        "name": "ACP",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "acp",
    },
    {
        "name": "Paint",
        "type": CalculationType.AREA,
        "unit": Unit.SQFT,
        "allow_decimal": True,
        "icon": "paint",
    },
    {
        "name": "Other",
        "type": CalculationType.COUNT,
        "unit": Unit.NOS,
        "allow_decimal": False,
        "icon": "other",
    },
]


def seed_products(db: Session):

    exists = db.query(Product).filter(
        Product.is_system.is_(True)
    ).first()

    if exists:
        return

    products = []

    for index, item in enumerate(DEFAULT_PRODUCTS, start=1):

        products.append(
            Product(
                company_id=None,
                product_code=f"SYS{index:06d}",
                product_name=item["name"],
                calculation_type=item["type"],
                default_unit=item["unit"],
                allow_decimal=item["allow_decimal"],
                display_order=index,
                icon=item["icon"],
                description=f"Default {item['name']} Product",
                is_system=True,
                status=Status.ACTIVE,
                version=1,
            )
        )

    db.add_all(products)
    db.commit()
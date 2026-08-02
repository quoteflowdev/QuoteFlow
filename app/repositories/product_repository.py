from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.enums import Status
from app.models.product import Product


class ProductRepository:

    def create_product(
        self,
        db: Session,
        product: Product
    ) -> Product:

        db.add(product)

        try:
            db.commit()
            db.refresh(product)
            return product

        except Exception:
            db.rollback()
            raise

    def get_products(
        self,
        db: Session,
        company_id: int
    ) -> list[Product]:

        return (
            db.query(Product)
            .filter(
                Product.status == Status.ACTIVE,
                or_(
                    Product.is_system.is_(True),
                    Product.company_id == company_id,
                ),
            )
            .order_by(
                Product.display_order.asc(),
                Product.product_name.asc(),
            )
            .all()
        )

    def search_products(
        self,
        db: Session,
        company_id: int,
        search: str,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Product]:

        return (
            db.query(Product)
            .filter(
                Product.status == Status.ACTIVE,
                or_(
                    Product.is_system.is_(True),
                    Product.company_id == company_id,
                ),
                Product.product_name.ilike(f"%{search}%"),
            )
            .order_by(
                Product.display_order.asc(),
                Product.product_name.asc(),
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_product_by_id(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(
                Product.id == product_id,
                Product.status == Status.ACTIVE,
                or_(
                    Product.is_system.is_(True),
                    Product.company_id == company_id,
                ),
            )
            .first()
        )

    def get_product_by_id_any_status(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(
                Product.id == product_id,
                or_(
                Product.is_system.is_(True),
                Product.company_id == company_id,
                ),
            )
            .first()
        )

    def get_product_by_name(
        self,
        db: Session,
        company_id: int,
        product_name: str,
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(
                Product.product_name == product_name,
                Product.status == Status.ACTIVE,
                Product.company_id == company_id,
            )
            .first()
        )

    def get_last_product(
        self,
        db: Session,
    ) -> Product | None:

        return (
            db.query(Product)
            .order_by(Product.id.desc())
            .first()
        )

    def update_product(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        try:
            db.commit()
            db.refresh(product)
            return product

        except Exception:
            db.rollback()
            raise

    def deactivate_product(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        product.status = Status.INACTIVE

        try:
            db.commit()
            db.refresh(product)
            return product

        except Exception:
            db.rollback()
            raise

    def restore_product(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        product.status = Status.ACTIVE

        try:
            db.commit()
            db.refresh(product)
            return product

        except Exception:
            db.rollback()
            raise


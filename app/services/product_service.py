from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (ProductCreate, ProductUpdate,)


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository()

    def _generate_product_code(
        self,
        db: Session,
        is_system: bool = False,
    ) -> str:

        last_product = self.product_repository.get_last_product(db)

        if last_product is None:
            number = 1
        else:
            number = last_product.id + 1

        prefix = "SYS" if is_system else "PRD"

        return f"{prefix}{number:06d}"

    def create_product(
        self,
        db: Session,
        company_id: int,
        product_data: ProductCreate,
    ) -> Product | None:

        existing_product = (
            self.product_repository.get_product_by_name(
                db,
                company_id,
                product_data.product_name,
            )
        )

        if existing_product is not None:
            return None

        product = Product(
            company_id=company_id,
            product_code=self._generate_product_code(db),
            product_name=product_data.product_name,
            calculation_type=product_data.calculation_type,
            default_unit=product_data.default_unit,
            allow_decimal=product_data.allow_decimal,
            description=product_data.description,
            is_system=False,
            created_by=company_id,
            updated_by=company_id,
        )

        return self.product_repository.create_product(
            db,
            product,
        )

    def get_all_products(
        self,
        db: Session,
        company_id: int,
    ) -> list[Product]:

        return self.product_repository.get_products(
            db,
            company_id,
        )

    def search_products(
        self,
        db: Session,
        company_id: int,
        search: str,
        page: int = 1,
        limit: int = 20,
    ) -> list[Product]:

        skip = (page - 1) * limit

        return self.product_repository.search_products(
            db=db,
            company_id=company_id,
            search=search,
            skip=skip,
            limit=limit,
        )

    def get_product_by_id(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ) -> Product | None:

        return self.product_repository.get_product_by_id(
            db,
            company_id,
            product_id,
        )

    def update_product(
        self,
        db: Session,
        company_id: int,
        product_id: int,
        product_update: ProductUpdate,
    ) -> Product | None:

        product = self.product_repository.get_product_by_id(
            db,
            company_id,
            product_id,
        )

        if product is None:
            return None

        if product.is_system:
            return None

        if (
            product_update.product_name is not None
            and product.product_name != product_update.product_name
        ):

            existing_product = (
                self.product_repository.get_product_by_name(
                    db,
                    company_id,
                    product_update.product_name,
                )
            )

            if existing_product is not None:
                return None

        update_data = product_update.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(product, field, value)

        product.updated_by = company_id
        product.version += 1

        return self.product_repository.update_product(
            db,
            product,
        )

    def deactivate_product(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ) -> Product | None:

        product = self.product_repository.get_product_by_id(
            db,
            company_id,
            product_id,
        )

        if product is None:
            return None

        if product.is_system:
            return None

        product.updated_by = company_id
        product.version += 1

        return self.product_repository.deactivate_product(
            db,
            product,
        )

    def restore_product(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ) -> Product | None:

        product = self.product_repository.get_product_by_id_any_status(
            db,
            company_id,
            product_id,
        )

        if product is None:
            return None

        if product.is_system:
            return None

        product.updated_by = company_id
        product.version += 1

        return self.product_repository.restore_product(
            db,
            product,
        )
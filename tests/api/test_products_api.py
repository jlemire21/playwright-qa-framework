import httpx
from pydantic import BaseModel, Field

API_BASE_URL = "https://dummyjson.com"


class ProductSchema(BaseModel):
    id: int
    title: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str


def test_get_single_product_matches_contract():
    response = httpx.get(f"{API_BASE_URL}/products/1", timeout=10.0)

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0  # Performance SLA check

    # Enforce strict JSON schema contract via Pydantic
    product = ProductSchema.model_validate(response.json())
    assert product.id == 1
    assert len(product.title) > 0


def test_get_products_list_pagination():
    response = httpx.get(f"{API_BASE_URL}/products", params={"limit": 5, "skip": 0}, timeout=10.0)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload["products"]) == 5
    for item in payload["products"]:
        ProductSchema.model_validate(item)


def test_nonexistent_product_returns_404():
    response = httpx.get(f"{API_BASE_URL}/products/999999", timeout=10.0)

    assert response.status_code == 404
    assert "not found" in response.json().get("message", "").lower()

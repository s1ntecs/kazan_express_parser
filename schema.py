from dataclasses import dataclass
from typing import Any, Dict, List, Union, Optional
from marshmallow import EXCLUDE


@dataclass
class Category:
    id: int
    title: str
    productAmount: Any = None
    parent: Any = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Review:
    reviewId: Optional[int] = None
    productId: Optional[int] = None
    date: Optional[int] = None
    edited: Optional[bool] = None
    customer: Optional[str] = None
    reply: Any = None
    rating: Optional[int] = None
    characteristics: Optional[List[Any]] = None
    pros: Any = None
    cons: Any = None
    content: Optional[str] = None
    photos: Optional[List[Any]] = None
    status: Optional[str] = None
    hasVerticalPhoto: Any = None
    like: Optional[bool] = None
    dislike: Optional[bool] = None
    amountLike: Optional[int] = None
    amountDislike: Optional[int] = None
    id: Optional[int] = None
    isAnonymous: Optional[bool] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Seller:
    id: Optional[int] = None
    title: Optional[str] = None
    link: Optional[str] = None
    description: Any = None
    hasCharityProducts: bool = False
    registrationDate: Optional[int] = None
    rating: float = None
    reviews: Optional[int] = None
    orders: Optional[int] = None
    official: bool = None
    contacts: Optional[List[Dict[str, Union[str, None]]]] = None
    categories: Optional[List[Dict[str, Union[int, str]]]] = None
    currentCategory: Any = None
    filters: List[Dict[str, Union[str, List[Union[int, float]]]]] = None
    appliedFilters: List[Dict[str, Union[str, Any]]] = None
    priceFilter: Any = None
    totalProducts: Optional[int] = None
    parents: List[Dict[str, Union[int, str]]] = None
    products: List[Any] = None
    sellerAccountId: Optional[int] = None
    info: Any = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class SkuList:
    id: int
    characteristics: Any = None
    availableAmount: Optional[int] = None
    fullPrice: Optional[float] = None
    purchasePrice: Optional[float] = None
    barcode: Optional[int] = None
    vat: Any = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Product:
    id: int
    title: Optional[str] = None
    category: Category = None
    rating: Any = None
    topFeedback: Review = None
    seller: Seller = None
    reviewsAmount: Any = None
    ordersAmount: Any = None
    rOrdersAmount: Any = None
    totalAvailableAmount: Any = None
    charityCommission: Any = None
    description: Optional[str] = None
    comments: Any = None
    attributes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    discountBadge: Any = None
    installment: Any = None
    skuList: List[SkuList] = None
    sellPrice: Optional[float] = None
    isEco: Optional[bool] = None
    isPerishable: Optional[bool] = None
    hasVerticalPhoto: Optional[bool] = None
    showKitty: Optional[bool] = None
    bonusProduct: Optional[bool] = None
    badges: List[Any] = None
    volumeDiscount: Any = None
    adultCategory: Optional[bool] = None
    colorPhotoPreview: Optional[bool] = None
    favourite: Optional[bool] = None
    product_url: str = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Payload:
    data: Product

    class Meta:
        unknown = EXCLUDE


@dataclass
class Data():
    payload: Payload

    def __str__(self) -> str:
        return f"product id = {self.payload.data.id}"

    class Meta:
        unknown = EXCLUDE

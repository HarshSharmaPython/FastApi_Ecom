from fastapi import FastAPI, Depends, Query, APIRouter
from typing import List, Optional
from beanie import PydanticObjectId
from bson import ObjectId
from ..models.product import SimpleProduct, VariantProduct

ShopRouter = APIRouter(tags=["Shop"])

async def filter_item(
    category: Optional[List[PydanticObjectId]] = Query(None),
    brand: Optional[str] = Query(None),
    tag: Optional[List[str]] = Query(None),
    age: Optional[List[str]] = Query(None),
    gender: Optional[List[str]] = Query(None),
    uses: Optional[List[str]] = Query(None),
    productform: Optional[List[str]] = Query(None),
    minprice: Optional[float] = Query(None),
    maxprice: Optional[float] = Query(None)
):
    return {
        "category": category,
        "brand": brand,
        "tag": tag,
        "age": age,
        "gender": gender,
        "uses": uses,
        "productform": productform,
        "minprice": minprice,
        "maxprice": maxprice
    }

@ShopRouter.get("/shop")
async def get_shop(filters: dict = Depends(filter_item)):
    query = {}

    # if filters["category"]:
    #     # query["category"] = filters["category"]
    #     # print(query['category'])
    #     query["category"] = {"$in": [ObjectId(cat) for cat in filters["category"]]}
    #     # print(query['category'])




    if filters["category"]:
 
            # category_ids = [ObjectId(cat) for cat in ]
        query["category.id"] = {"$in": filters["category"]}
        print(filters['category'])




    if filters["brand"]:
        query["brand"] = filters["brand"]

    if filters["tag"]:
        query["tag"] = {"$in": filters["tag"]}

    if filters["age"]:
        query["age"] = {"$in": filters["age"]}

    if filters["gender"]:
        query["gender"] = {"$in": filters["gender"]}

    if filters["uses"]:
        query["uses"] = {"$in": filters["uses"]}

    if filters["productform"]:
        query["productform"] = {"$in": filters["productform"]}

    if filters["minprice"] is not None or filters["maxprice"] is not None:
        query["regular_price"] = {}
        if filters["minprice"] is not None:
            query["regular_price"]["$gte"] = filters["minprice"]
        if filters["maxprice"] is not None:
            query["regular_price"]["$lte"] = filters["maxprice"]

    try:
        simple_items = await SimpleProduct.find(query).to_list(100)
        variant_items = await VariantProduct.find(query).to_list(100)
    except Exception as e:
        print(f"Error finding products: {e}")
        simple_items, variant_items = [], []

    return {"simple_items": simple_items, "variant_items": variant_items}

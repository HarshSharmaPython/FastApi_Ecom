from fastapi import APIRouter, status, HTTPException, Query
from ...models.product import *

ProductListingRouter = APIRouter(tags="Product Listing")

@ProductListingRouter.post('/', tags=["Product"])
async def CreateProduct(product: SimpleProductType):
    try:
        inserted_product = await SimpleProduct(**product.model_dump()).insert()
        return inserted_product
    except Exception as e:
        print("Error while inserting the product")
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the product. Please try again later.")
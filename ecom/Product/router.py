from typing import Set
from fastapi import APIRouter, HTTPException, status, Query
from ..models.product import *
from beanie import PydanticObjectId
from beanie.operators import In, Or
from .service import *
from datetime import datetime, timezone

ProductRouter = APIRouter()

@ProductRouter.get('/category', tags=["Category"])
async def GetCategories():
    try:
        categories = await Category.find_all().to_list()
        return categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to get the categories at the time. Please try again later.")
    
@ProductRouter.post('/category', tags=["Category"])
async def CreateCategory(category: CategoryType):
    if(category.name.strip()==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category name can't be empty.")
    is_category_exists = await check_if_category_exists(category.name)
    if(is_category_exists):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"A category with the name <{category.name}> already exists. Please select another name for the category.")
    try:
        inserted_category = await Category(**category.model_dump()).insert()
        return inserted_category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the category. Please try again later.")

@ProductRouter.delete('/category', tags=["Category"])
async def DeleteCategory(name: str):
    if(name.strip()==""):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category name can't be empty.")
    is_category_exists = await check_if_category_exists(name)
    if is_category_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with the name <{name}> does not exists.")
    try:
        await Category.find(Category.name==name).delete()
        return {"message": "Successfully deleted the category."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the category. Please try again later.")

@ProductRouter.patch('/category', tags=["Category"])
async def UpdateCategory(name: str, update_details: UpdateCategory):
    is_category_exists = await check_if_category_exists(name)
    if is_category_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category with the name <{name}> does not exists.")
    try:
        if update_details.name is not None:
            is_category_exists.name = update_details.name
        if update_details.image is not None:
            is_category_exists.image = update_details.image
        is_category_exists.updated_at = datetime.now(timezone.utc)
        await is_category_exists.save()
        return is_category_exists
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the category. Please try again later.")

@ProductRouter.get('/', tags=["Product", "Variant Product"])
async def GetProduct(product_id: PydanticObjectId, prod_type: str | None = None, fetch_links: bool = False):
    product = None
    if prod_type is None or prod_type == "simple":
        product = await SimpleProduct.get(product_id, fetch_links=fetch_links)
    elif prod_type == "variant":
        product = await VariantProduct.get(product_id, fetch_links=fetch_links)
    if product is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with the id: <{product_id}> does not exists.")
    return product

@ProductRouter.post('/', tags=["Product"])
async def CreateSimpleProduct(product: SimpleProductType):
    product_exists = await SimpleProduct.find_one(Or(SimpleProduct.slug==product.slug, SimpleProduct.sku_number==product.sku_number))
    if product_exists:
        if product_exists.slug == product.slug:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with slug: <{product.slug}> already exists.")
        if product_exists.sku_number == product.sku_number:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with sku number: <{product.sku_number}> already exists.")
    try:
        inserted_product = await SimpleProduct(**product.model_dump()).insert()
        return inserted_product
    except Exception as e:
        print("Error while inserting the product")
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the product. Please try again later.")

@ProductRouter.patch("/", tags=["Product"])
async def UpdateProduct(id: PydanticObjectId, update_details: UpdateProductType):
    product_exists = await check_if_product_exists(id)
    if product_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided product id does not exists. Please provide a valid id.")
    try:
        updated_category = update_details.category if update_details.category is not None else product_exists.category
        updated_group = update_details.grouped_with if update_details.grouped_with is not None else product_exists.grouped_with
        await product_exists.set({**update_details.model_dump(exclude_none=True, exclude=["category", "grouped_with"]), "category": updated_category, "grouped_with": updated_group, "updated_at": datetime.now(timezone.utc)})
        return product_exists
    except Exception as e:
        print("Error while updating the product")
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to update the product. Please try again later.")

@ProductRouter.delete("/", tags=["Product"])
async def DeleteProduct(id: PydanticObjectId):
    product_exists = await check_if_product_exists(id)
    if product_exists is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided product id does not exists. Please provide a valid id.")
    try:
        await product_exists.delete()
        return {"message": "Successfully deleted the product."}
    except Exception as e:
        print("Error while updating the product")
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to delete the product. Please try again later.")

async def GetMultipleVariantProducts(page_no: int, limit: int, skip: int, categories: list[PydanticObjectId] = Query(None)):
    if categories is None or len(categories) == 0:
        products = await VariantProduct.find(VariantProduct.type=="variant", limit=limit, skip=skip, fetch_links=True).to_list()
    else:
        products = await VariantProduct.find(VariantProduct.type=="variant", In(SimpleProduct.category._id, categories), limit=limit, skip=skip, fetch_links=True).to_list()
    return {"data": products, "total": len(products), "current_page": page_no}

async def GetMultipleSimpleProducts(page_no: int, limit: int, skip: int, categories: list[PydanticObjectId] = Query(None)):
    if categories is None or len(categories) == 0:
        products = await SimpleProduct.find(Or(SimpleProduct.type==None, SimpleProduct.type=="simple"), limit=limit, skip=skip, fetch_links=True).to_list()
    else: 
        products = await SimpleProduct.find(Or(SimpleProduct.type==None, SimpleProduct.type=="simple"), In(SimpleProduct.category._id, categories), limit=limit, skip=skip, fetch_links=True).to_list()
    return {"data": products, "total": len(products), "current_page": page_no}

@ProductRouter.get("/products", tags=["Product", "Variant Product"])
async def GetMultipleProducts(page_no: int = 1, prod_type: str | None = None, categories: list[PydanticObjectId] = Query(None)):
    if page_no<1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page no. must be greater than 0.")
    limit = 20
    skip = (page_no-1)*limit
    if prod_type == "simple" or prod_type is None:
        return await GetMultipleSimpleProducts(page_no, limit, skip, categories)
    elif prod_type == "variant":
        return await GetMultipleVariantProducts(page_no, limit, skip, categories)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid product type: <{prod_type}>")

@ProductRouter.post('/products', tags=["Product"])
async def CreateMultipleProducts(products: list[MassCreateSimpleProduct]):
    if len(products)==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No product provided.")
    try:
        await SimpleProduct.insert_many([SimpleProduct(**prod.model_dump()) for prod in products])
        return {"message": "Successfully inserted the products.", "total": len(products)}
    except Exception as e:
        print("Error while inserting multiple products")
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to insert multiple products at the time. Please try again later.")


@ProductRouter.post("/variant", tags=["Variant Product"])
async def CreateVariantProduct(product: VariantProductType):
    try:
        variants = create_new_variants(product.attributes)    
        inserted_product = await VariantProduct(variants=variants, **product.model_dump()).insert()
        return inserted_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to create the variant product. Please try again later.")

@ProductRouter.delete("/variant", tags=["Variant Product"])
async def DeleteVariantProduct(prod_id: PydanticObjectId):
    try:
        await VariantProduct.find_one(VariantProduct.id==prod_id, VariantProduct.type=="variant").delete()
        return {"message": "Successfully deleted the product."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to delete the variant product. Please try again later.")

@ProductRouter.patch('/variant', tags=["Variant Product"])
async def UpdateVariantProduct(prod_id: PydanticObjectId, update_details: UpdateVariantProductType):
    variant_prod = await VariantProduct.get(prod_id)
    if variant_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant product with id: <{prod_id}> could not be found.")
    if variant_prod.type != "variant":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The product with id: <{prod_id}> is not of type variant.")
    update_details.updated_at = datetime.now(timezone.utc)
    try:
        updated_category = update_details.category if update_details.category is not None else variant_prod.category
        await variant_prod.set({**update_details.model_dump(exclude_none=True, exclude=["category"]), "category": updated_category})
        return variant_prod
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to update the variant product. Please try again later.")

async def UpdateVariantProductAttributes(prod_id: PydanticObjectId, attributes: AttributeType):
    variant_prod = await VariantProduct.find(VariantProduct.id==prod_id, VariantProduct.type=="variant")
    if variant_prod is None:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail=f"Variant product with id: <{prod_id}> not found.")
        

@ProductRouter.patch("/variant/attr-props", tags=["Variant Product"])
async def UpdateVariantProdAttrProps(prod_id: PydanticObjectId, attr_name: str, new_props: list[str]):
    if len(new_props) == 0:
        return await DeleteVariantProdAttribute(prod_id=prod_id, attr_name=attr_name)
    variant_prod = await VariantProduct.get(prod_id)
    if variant_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant product with id: <{prod_id}> could not be found.")
    if variant_prod.type != "variant":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The product with id: <{prod_id}> is not of type variant.")
    if attr_name not in variant_prod.attributes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attribute with the name: <{attr_name}> could not be found.")
    update_object = get_updated_attribute_and_variants(product=variant_prod, attribute_name=attr_name, new_props=new_props)
    try:
        updated_prod = await variant_prod.update(
            {
                "$set": {"updated_at": datetime.now(timezone.utc), **update_object},
            }
        )
        return updated_prod
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to add attribute prop in variant product. Please try again later.")

@ProductRouter.post("/variant/attr", tags=["Variant Product"])
async def AddVariantProdAttribute(prod_id: PydanticObjectId, attr_name: str, props: Set[str]):
    variant_prod = await VariantProduct.get(prod_id)
    if variant_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant product with id: <{prod_id}> could not be found.")
    if variant_prod.type != "variant":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The product with id: <{prod_id}> is not of type variant.")
    if attr_name in variant_prod.attributes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attribute with the name: <{attr_name}> already exists.")
    variant_prod.attributes[attr_name] = props
    variant_prod.variants = create_new_variants(variant_prod.attributes)
    await variant_prod.save()
    return variant_prod

@ProductRouter.delete("/variant/attr", tags=["Variant Product"])
async def DeleteVariantProdAttribute(prod_id: PydanticObjectId, attr_name: str):
    variant_prod = await VariantProduct.get(prod_id)
    if variant_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant product with id: <{prod_id}> could not be found.")
    if variant_prod.type != "variant":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The product with id: <{prod_id}> is not of type variant.")
    if attr_name not in variant_prod.attributes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attribute with the name: <{attr_name}> could not be found.")
    del variant_prod.attributes[attr_name]
    variant_prod.variants = create_new_variants(variant_prod.attributes)
    await variant_prod.save()
    return variant_prod

@ProductRouter.patch('/variant/update', tags=["Variant Product"])
async def UpdateVariantProductVariant(prod_id: PydanticObjectId, variant_key: str, updated_variant: UpdateVariantType):
    variant_prod = await VariantProduct.get(prod_id)
    if variant_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant product with id: <{prod_id}> could not be found.")
    if variant_prod.type != "variant":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The product with id: <{prod_id}> is not of type variant.")
    if variant_key not in variant_prod.variants:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Variant with the key: <{variant_key}> could not be found.")
    try:
        variant_prod.variants[variant_key] = {**variant_prod.variants[variant_key].model_dump(), **updated_variant.model_dump(exclude_none=True)}
        await variant_prod.save()
        return variant_prod
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to add attribute prop in variant product. Please try again later.")


@ProductRouter.delete("/variants", tags=["Variant Product"])
async def DeleteMultipleVariantProducts(prod_ids: list[PydanticObjectId]):
    try:
        await VariantProduct.find(In(VariantProduct.id, prod_ids)).delete_many()
        return {"message": "Successfully deleted the product."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error. Unable to delete the variant product. Please try again later.")

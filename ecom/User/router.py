# all the routes are here   
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from ..config import Config,MailConfig
from beanie import PydanticObjectId
from ..models import User,UpdateUser,Purchase,PurchaseItem,SimpleProduct,VariantProduct,Invenrtory,CreateInventory
from ..Auth.mail.service import *
from ..Auth import decode_jwt_token
from datetime import datetime,timezone
from bson import ObjectId,DBRef
from beanie.odm.fields import Link

from ..utils import *
from ..utils.mail import *



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.OAuth_Token_URL)

def is_authenticated(token: str = Depends(oauth2_scheme)):
    user = decode_jwt_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User: User not found")     
    if user['role'] == "user":
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User: Not authorized")
    
    
UserRouter = APIRouter(dependencies=[Depends(is_authenticated)], tags=["User"])

@UserRouter.get('/')
async def UserIndex():
    return {'message':'this is message saying hello to the user'}

@UserRouter.get('/profile/')
async def profile(user: dict = Depends(is_authenticated)):
    user_id = user["id"]
    print(user_id)
    user_det = await User.get(PydanticObjectId(user_id))
    if user_det is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_det

@UserRouter.put("/")
async def update_profile( update: UpdateUser,user: dict = Depends(is_authenticated)):
    user_id = user["id"]
    user_det = await User.get(PydanticObjectId(user_id))
    if user_det is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await user_det.set({**user_det.model_dump(exclude_none = True),"updated_at":datetime.now(timezone.utc)})
    return user_det



@UserRouter.post("/purchase")
async def purchase(purchase: PurchaseItem, user: dict = Depends(is_authenticated)):
    user_id = user["id"]

    user_det = await User.get(PydanticObjectId(user_id))
    if user_det is None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    

    total_price = 0.0
    purchase_details = []

    for item in purchase.items:

        item_total_price = item.quantity * item.price
        total_price += item_total_price

        purchase_details.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
            "item_total": item_total_price
        })
        # product1= await item.product_id.fetch()
        # # print(product1)
        # # # product=  asd()
        # # product = await Invenrtory.find_one(Invenrtory.product_id==product1)
        # print(item.product_id)
        # # product = await Invenrtory.find_one({"product_id.$id": ObjectId(item.product_id)})
        # # product_id = item.product_id
        # product = await Invenrtory.find_one({"product_id.id": ObjectId(product1)})


        # try:
        #     product = await item.product_id.fetch()  # Fetch the actual product reference
        #     print(product)
        #     # product_id = product.id
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error fetching product ID: {str(e)}")

        # # Query the inventory using the fetched product ID
        # inventory_item = await Invenrtory.find_one({"product_id.$id": ObjectId(product)})



        product1= await item.product_id.fetch()
        # print(product1.id)
        print(product1)

        # Query the inventory using the product_id
        inventory_item = await Invenrtory.find_one({"product_id.$id": product1})
        
        if inventory_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {product1} not found")
        
        # Return the found product
        return inventory_item




        print(inventory_item)
        return inventory_item
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        else:
            if product.quantity<item.quantity:
                send_mail(
                    subject="Product out of stock",
                    body=f"Product {product.Batch_No} is out of stock.",
                    from_email="charvi@fglawkit.com",
                    to_email="harshsharma1172002@gmail.com",
                    password="casiosa78"
                    
                )
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not available")
            

        # return product

        if product:
            
            if isinstance(product,CreateInventory):
                product.quantity -= item.quantity
                # if product.quantity_details.quantity == 0:
                #     send_mail(
                #         subject="Product out of stock",
                #         body=f"Product {product.name} is out of stock.",
                #         from_email="charvi@fglawkit.com",
                #         to_email="harshsharma1172002@gmail.com",
                #         password="casiosa78"
                #     )
                await product.save()
            elif isinstance(product,VariantProduct):
                product.quantity -= item.quantity  
                await product.save()

        

    new_purchase = Purchase(
        user_id=user_det.id,
        items=purchase_details,
        total=total_price,
        purchase_date=datetime.now(timezone.utc)
    )
    await new_purchase.save()


#USER REFERRAL AND EARN POINTS
    if not user_det.has_purchased:
        if user_det.referral_by:
            referred_by = await User.find_one(User.referral_code == user_det.referral_by)
            if referred_by:
                referred_by.points += Config.user_points
                await referred_by.save()
        user_det.has_purchased = True  
        await user_det.save()

    user_det.Purchase.append(new_purchase)
    await user_det.save()

    return new_purchase



@UserRouter.get("/purchases/")
async def get_purchases(user: dict = Depends(is_authenticated)):
    user_oid = PydanticObjectId(user["id"])
    purchases = await Purchase.find(Purchase.user_id.id == user_oid).to_list()
    return purchases
    
        
{
  "user_id":"6697b08bdcdd5e67a95ad1c2",
  "items": [{"product_id":"6698f6323d7a85c6b348f07f","quantity":4,"price":100.50}],
  "total": 0,
  "purchase_date": "2024-07-17T10:45:57.145Z"
}




def asd():
    from pymongo import MongoClient
    from bson import ObjectId

    # Replace the URI with your MongoDB connection string
    client = MongoClient("mongodb+srv://dev:mWobL6mkRIxXROfZ@sampletest.1xbn54m.mongodb.net/?retryWrites=true&w=majority&appName=sampleTest")

    # Select the database and collection
    db = client['ecomm']
    inventory_collection = db['Invetory']

    # Define the query
    query = {
        "product_id": {
            "$ref": "product",
            "$id": ObjectId("669a45dbaa687d00429cb5d6")
        }
    }

    # Execute the query
    results = inventory_collection.find(query)

    # Print the results
    for result in results:
        print(result)

    print('done')
    return result
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env



def pay():
    merchant_id = "UATMERCHANT"  
    salt_key = "8289e078-be0b-484d-ae60-052f117f8deb"  
    salt_index = 1 
    env = Env.UAT # Change to Env.PROD when you go live
    phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
    
    
    
    unique_transcation_id = str(uuid.uuid4())[:-2]
    ui_redirect_url = "https://www.merchant.com/redirectPage"  
    s2s_callback_url = "localhost:8000/success" 

    amount = 10000  # 1 rupee, 100 paise  
    id_assigned_to_user_by_merchant = "YOUR_USER_ID"  
    pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transcation_id,  
                                                             amount=amount,  
                                                             merchant_user_id=id_assigned_to_user_by_merchant,  
                                                             callback_url=s2s_callback_url,  
                                                             redirect_url=ui_redirect_url)  
    pay_page_response = phonepe_client.pay(pay_page_request)  
    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
    print(pay_page_response)
    print(pay_page_url)
    return pay_page_response





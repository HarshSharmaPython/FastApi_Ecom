from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env

merchant_id = "YOUR_MERCHANT_ID"  
salt_key = "YOUR_SALT_KEY"  
salt_index = 1 
env = Env.UAT # Change to Env.PROD when you go live

phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)

import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest

unique_transaction_id = str(uuid.uuid4())[:-2]
ui_redirect_url = "https://www.merchant.com/redirectPage"  
s2s_callback_url = "https://www.merchant.com/callback"  
amount = 100  
id_assigned_to_user_by_merchant = 'YOUR_USER_ID'  
pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transaction_id,  
                                                             amount=amount,  
                                                             merchant_user_id=id_assigned_to_user_by_merchant,  
                                                             callback_url=s2s_callback_url,
redirect_url=ui_redirect_url)  
pay_page_response = phonepe_client.pay(pay_page_request)  
pay_page_url = pay_page_response.data.instrument_response.redirect_info.url


unique_transaction_id = "INSERT_YOUR_UNIQUE_TRANSACTION_ID"  
transaction_status_response = phonepe_client.check_status(merchant_transaction_id=unique_transaction_id)  
transaction_state = transaction_status_response.data.state


x_verify_header_data = "a005532637c6a6e4a4b08ebc6f1144384353305a9cd253d995067964427cd0bb###1"
phonepe_s2s_callback_response_body_string = '{"response": "eyJzdWNjZXNzIjpmYWxzZSwiY29kZSI6IlBBWU1FTlRfRVJST1IiLCJtZXNzYWdlIjoiUGF5bWVudCBGYWlsZWQiLCJkYXRhIjp7Im1lcmNoYW50SWQiOiJtZXJjaGFudElkIiwibWVyY2hhbnRUcmFuc2FjdGlvbklkIjoibWVyY2hhbnRUcmFuc2FjdGlvbklkIiwidHJhbnNhY3Rpb25JZCI6IkZUWDIzMDYwMTE1NDMxOTU3MTYzMjM5IiwiYW1vdW50IjoxMDAsInN0YXRlIjoiRkFJTEVEIiwicmVzcG9uc2VDb2RlIjoiUkVRVUVTVF9ERUNMSU5FX0JZX1JFUVVFU1RFRSIsInBheW1lbnRJbnN0cnVtZW50IjpudWxsfX0="}'
is_valid = phonepe_client.verify_response(x_verify=x_verify_header_data,  
                                          response=phonepe_s2s_callback_response_body_string)


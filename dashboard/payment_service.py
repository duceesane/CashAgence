import hashlib
import requests
from django.conf import settings

def generate_confirm(user_id):
    """
    Kani waa shaqo dhalisa koodhka 'confirm'.
    PDF-ku wuxuu leeyahay: Xisaabi MD5 adoo isku xiraya (userId:hash)[cite: 31, 32].
    """
    # Isku dar userId, dhibicda (:), iyo hash_key-ga [cite: 32, 33]
    confirm_str = f"{user_id}:{settings.API_HASH}"
    # U beddel mashiinka MD5 hash oo u dhiib natiijada [cite: 32, 33]
    return hashlib.md5(confirm_str.encode('utf-8')).hexdigest()


def generate_user_search_signature(user_id):
    """
    Kani wuxuu dhaliyaa saxiixa 'sign' ee loogu talagalay raadinta qofka (Player Search)[cite: 73, 76].
    """
    # 1. Tallaabada koowaad ee PDF-ka: SHA256 ee (hash={0}&userid={1}&cashdeskid={2}) [cite: 74]
    str1 = f"hash={settings.API_HASH}&userid={user_id}&cashdeskid={settings.API_CASHDESK_ID}"
    sha256_1 = hashlib.sha256(str1.encode('utf-8')).hexdigest()

    # 2. Tallaabada labaad ee PDF-ka: MD5 ee (userid={0}&cashierpass={1}&hash={2}) [cite: 75]
    str2 = f"userid={user_id}&cashierpass={settings.API_CASHIER_PASS}&hash={settings.API_HASH}"
    md5_2 = hashlib.md5(str2.encode('utf-8')).hexdigest()

    # 3. Tallaabada saddexaad: Isku dar Result1 + Result2, ka dibna ka dhig SHA256 [cite: 76]
    combined_str = sha256_1 + md5_2
    final_signature = hashlib.sha256(combined_str.encode('utf-8')).hexdigest()
    
    return final_signature


def get_user_profile(user_id):
    """
    Shaqadan waxay u dirtaa codsiga (GET Request) nidaamka weyn si loo soo raadiyo Player-ka[cite: 69, 70].
    """
    # 1. Soo xisaabi koodka confirm-ka adoo wacaya shaqadii kor ku tiilay [cite: 72]
    confirm_code = generate_confirm(user_id)
    
    # 2. Diyaari URL-ka rasmiga ah ee PDF-ka ku qoran[cite: 70]:
    # Horgalka + /Users/{userId}?confirm={code}&cashdeskid={id}
    base_url = settings.API_BASE_URL.rstrip('/')
    url = f"{base_url}/Users/{user_id}?confirm={confirm_code}&cashdeskid={settings.API_CASHDESK_ID}"
    
    # 3. Diyaari saxiixa ammaanka ee madaxa (Header-ka) la saarayo [cite: 9, 76]
    signature = generate_user_search_signature(user_id)
    headers = {
        "sign": signature,  # Shirkaddu haddii ay weydo saxiixan waxay soo celineysaa error 401 [cite: 9, 10]
        "Content-Type": "application/json"
    }

    try:
        # 4. U dir codsiga shirkadda weyn adoo isticmaalaya requests.get [cite: 70]
        response = requests.get(url, headers=headers)
        
        # 5. Haddii uu si guul leh u soo jawaabo (Status 200) [cite: 77]
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json() # Xogta qofka: currencyId, userId, name [cite: 78, 79, 80]
            }
        else:
            return {
                "success": False, 
                "error_code": response.status_code, 
                "message": "API-gu wuxuu soo celiyay qalad ama qofka lama tapo."
            }
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": str(e)}
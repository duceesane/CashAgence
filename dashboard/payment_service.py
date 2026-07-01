import hashlib
import requests
from django.conf import settings
from datetime import datetime, timezone

def generate_confirm(user_id):
    """
    MD5(userId:hash)
    """
    confirm_str = f"{user_id}:{settings.API_HASH}"
    return hashlib.md5(confirm_str.encode("utf-8")).hexdigest()


def generate_user_search_signature(user_id):
    """
    Player Search Signature
    """

    # Step 1
    str1 = (
        f"hash={settings.API_HASH}"
        f"&userid={user_id}"
        f"&cashdeskid={settings.API_CASHDESK_ID}"
    )

    sha256_1 = hashlib.sha256(
        str1.encode("utf-8")
    ).hexdigest()

    # Step 2
    str2 = (
        f"userid={user_id}"
        f"&cashierpass={settings.API_CASHIER_PASS}"
        f"&hash={settings.API_HASH}"
    )

    md5_2 = hashlib.md5(
        str2.encode("utf-8")
    ).hexdigest()

    # Step 3
    final_signature = hashlib.sha256(
        f"{sha256_1}{md5_2}".encode("utf-8")
    ).hexdigest()

    return final_signature


def get_user_profile(user_id):

    confirm_code = generate_confirm(user_id)

    url = (
        f"{settings.API_BASE_URL}"
        f"/Users/{user_id}"
        f"?confirm={confirm_code}"
        f"&cashdeskid={settings.API_CASHDESK_ID}"
    )

    signature = generate_user_search_signature(user_id)

    headers = {
        "sign": signature,
        "Accept": "application/json",
    }

    try:

        print("URL:", url)
        print("SIGN:", signature)
        print("CONFIRM:", confirm_code)

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }

        return {
            "success": False,
            "error_code": response.status_code,
            "api_response": response.text
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": str(e)
        }
def generate_balance_confirm():
    confirm = f"{settings.API_CASHDESK_ID}:{settings.API_HASH}"
    return hashlib.md5(confirm.encode()).hexdigest()


def generate_balance_signature(dt):
    # Step 1
    str1 = (
        f"hash={settings.API_HASH}"
        f"&cashdeskid={settings.API_CASHDESK_ID}"
        f"&dt={dt}"
    )

    sha1 = hashlib.sha256(str1.encode()).hexdigest()

    # Step 2
    str2 = (
        f"dt={dt}"
        f"&cashierpass={settings.API_CASHIER_PASS}"
        f"&cashdeskid={settings.API_CASHDESK_ID}"
    )

    md5 = hashlib.md5(str2.encode()).hexdigest()

    # Step 3
    return hashlib.sha256(f"{sha1}{md5}".encode()).hexdigest()


def check_balance():

    dt = datetime.now(timezone.utc).strftime("%Y.%m.%d %H:%M:%S")

    url = (
        f"{settings.API_BASE_URL}"
        f"/Cashdesk/{settings.API_CASHDESK_ID}/Balance"
        f"?confirm={generate_balance_confirm()}"
        f"&dt={dt}"
    )

    headers = {
        "sign": generate_balance_signature(dt),
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response.json()
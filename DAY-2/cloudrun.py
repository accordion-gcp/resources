
#entrypoint - convert_to_inr

import functions_framework
import requests

CURRENCY_MAP = {
    "India": "INR", "USA": "USD", "UK": "GBP", "Germany": "EUR",
    "UAE": "AED", "Singapore": "SGD", "Australia": "AUD", "Canada": "CAD"
}

@functions_framework.http
def convert_to_inr(request):
    calls = request.get_json()["calls"]
    replies = []
    for amount, country in calls:
        currency = CURRENCY_MAP.get(country)
        if currency in (None, "INR"):
            replies.append(amount)
            continue
        try:
            resp = requests.get(
                f"https://api.frankfurter.dev/v1/latest?amount={amount}&from={currency}&to=INR",
                timeout=5
            )
            replies.append(resp.json()["rates"]["INR"])
        except Exception:
            replies.append(None)
    return {"replies": replies}
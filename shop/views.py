from django.views.generic import View
from django.http import JsonResponse
from shop.services import get_daily_report


class ReportView(View):
    """ Endpoint to return a report of orders for a given date, specified as 'YYYY-MM-DD'.

    Sample response:

    {
        "customers": 9,
        "total_discount_amount": 15152814.736907512,
        "items": 2895,
        "order_total_avg": 15895179.735734595
        "discount_rate_avg": 0.13145131216518066,
        "commissions": {
            "promotions": {
                "5": 1153804.8,
                "2": 188049.402
            },
            "total": 20833236.93,
            "order_average": 2314804.1042
        }
    }

    """
    def get(self, request, *args, **kwargs):
        return JsonResponse(get_daily_report(kwargs['date']))

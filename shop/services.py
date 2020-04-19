from datetime import datetime

from shop.models import *


def get_daily_report(date_string: str):
    """ Returns a report of daily order metrics based on a string specifying date in the format 'YYYY-MM-DD'."""
    order_queryset, vendor_queryset, promotion_queryset = get_daily_querysets(date_string)
    customer_ids = [order.customer_id for order in order_queryset]
    unique_customers = len(set(customer_ids))
    report = {"customers": unique_customers}
    order_data = get_order_data(order_queryset, vendor_queryset, promotion_queryset)
    report.update(order_data)
    return report


def get_daily_querysets(date_string: str):
    """ Filters orders, vendor commissions and promotions by date """
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    order_queryset = Order.objects.filter(created_at__date=date)
    vendor_queryset = VendorCommission.objects.filter(date=date)
    promotion_queryset = ProductPromotion.objects.filter(date=date)
    return order_queryset, vendor_queryset, promotion_queryset


def get_order_data(order_queryset: models.QuerySet, vendor_queryset: models.QuerySet, promotion_queryset) -> dict:
    """ Calculates metrics for the report by iterating through each order line for a single day """
    order_line_queryset = OrderLine.objects.filter(order_id__in=order_queryset)
    total_discount_amount, items, order_total_sum, discount_rate_sum, commission_sum = 0, 0, 0, 0, 0
    number_of_orders = order_queryset.count()
    promotions_totals = {}

    for order_line in order_line_queryset:
        items += order_line.quantity
        discount = order_line.full_price_amount - order_line.discounted_amount
        total_discount_amount += discount
        discount_rate_sum += order_line.quantity * order_line.discount_rate
        order_total_sum += order_line.total_amount

        vendor_id = order_queryset.filter(id=order_line.order_id).get().vendor_id
        commission_rate = vendor_queryset.filter(vendor_id=vendor_id).get().rate
        commission_earned = commission_rate * order_line.total_amount
        commission_sum += commission_earned
        
        active_promotion = promotion_queryset.filter(product_id=order_line.product_id)
        if active_promotion:
            promotion = active_promotion.get().promotion_id
            promotions_totals[promotion] = promotions_totals.get(promotion, 0) + commission_earned

    order_total_avg = order_total_sum / number_of_orders if number_of_orders else 0
    discount_rate_avg = discount_rate_sum / items if items else 0
    commission_avg = commission_sum / number_of_orders if number_of_orders else 0
    order_data = {
        "total_discount_amount": total_discount_amount,
        "items": items,
        "order_total_avg": order_total_avg,
        "discount_rate_avg": discount_rate_avg,
        "commissions": {
            "promotions": promotions_totals,
            "total": commission_sum,
            "order_average": commission_avg
        }
    }
    return order_data

from datetime import datetime

from shop.models import *


def get_daily_report(date_string: str) -> dict:
    """ Returns a report of daily order metrics based on a string specifying date in the format 'YYYY-MM-DD'."""
    date = datetime.strptime(date_string, '%Y-%m-%d').date()
    order_queryset = Order.objects.filter(created_at__date=date)
    customer_ids = [order.customer_id for order in order_queryset]
    unique_customers = len(set(customer_ids))
    report = {"customers": unique_customers}
    order_data = get_order_data(date, order_queryset)
    report.update(order_data)
    return report


def safe_divide(numerator: float, denominator: int) -> float:
    """ Divides without raising an exception for days where there have been no orders """
    if denominator:
        return numerator / denominator
    return 0


def get_order_data(date: datetime.date, order_queryset: models.QuerySet) -> dict:
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
        commission_earned = get_commission_earned(date, order_queryset, order_line)
        commission_sum += commission_earned
        calculate_commission_per_promotion(date, order_line.product_id, promotions_totals, commission_earned)

    order_total_avg = safe_divide(order_total_sum, number_of_orders)
    discount_rate_avg = safe_divide(discount_rate_sum, items)
    commission_avg = safe_divide(commission_sum, number_of_orders)
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


def get_commission_earned(date: datetime.date, order_queryset: models.QuerySet, order_line: OrderLine) -> float:
    """ Calculates commission earned on a single order line """
    vendor_queryset = VendorCommission.objects.filter(date=date)
    vendor_id = order_queryset.filter(id=order_line.order_id).get().vendor_id
    commission_rate = vendor_queryset.filter(vendor_id=vendor_id).get().rate
    return commission_rate * order_line.total_amount


def calculate_commission_per_promotion(date: datetime.date, product_id: int, promotions_totals: dict,
                                       commission_earned: float):
    """ Checks if there is a promotion on a product and if so adds the commission on the sale to the total commission
    for that promotion """
    promotion_queryset = ProductPromotion.objects.filter(date=date)
    active_promotion = promotion_queryset.filter(product_id=product_id)
    if active_promotion:
        promotion = active_promotion.get().promotion_id
        promotions_totals[promotion] = promotions_totals.get(promotion, 0) + commission_earned

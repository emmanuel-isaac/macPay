from django import template
import datetime

register = template.Library()

from services.core_functions import diff_month, add_months


@register.filter(name='get_current_payment_plan')
def get_current_payment_plan(fellow):
    last_payment_history = fellow.paymenthistory_set.last()
    if last_payment_history:
        try:
            current_payment_plan = last_payment_history.current_payment_plan
            return current_payment_plan
        except ValueError as e:
            print e
    return None


@register.filter(name='get_amount_paid')
def get_amount_paid(fellow):
    payment_history = fellow.paymenthistory_set.all()
    num_payments = len(payment_history)
    if payment_history and payment_history[num_payments - 1].sum_paid:
        amounts_paid = map(lambda x: x.sum_paid, payment_history)
        total_sum_paid = reduce(lambda x, y: x + y, amounts_paid)
        return total_sum_paid
    else:
        return None


@register.filter(name='get_months_left_on_plan')
def get_months_left_on_plan(fellow):
    payment_started = fellow.payment_start_date
    last_payment = fellow.paymenthistory_set.last()
    current_payment_plan = get_current_payment_plan(fellow)
    if current_payment_plan and last_payment:
        if last_payment.sum_paid:
            number_payment_months = diff_month(last_payment.date, payment_started)
            months_left = int(current_payment_plan.plan_duration) - int(number_payment_months) - 1
            return months_left
        else:
            return current_payment_plan.plan_duration
    return None


@register.filter(name='get_tentative_payment_end_date')
def get_tentative_payment_end_date(fellow):
    try:
        months_left = get_months_left_on_plan(fellow)

        if months_left:
            return add_months(datetime.date.today(), months_left)
    except Exception, e:
        pass
    return None


@register.filter(name='get_balance')
def get_balance(fellow):
    if fellow.paymenthistory_set.all():
        amount_paid = get_amount_paid(fellow)
        if amount_paid:
            return fellow.computer.cost - get_amount_paid(fellow)
    return None


@register.filter(name='check_none')
def check_none(value):
    if value:
        return value
    return '--'

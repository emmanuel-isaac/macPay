from apps.payment.models import PaymentHistory, PaymentPlan
import calendar
import datetime


def create_payment_history(months, fellow):
    payment_plan = fellow.recent_payment_plan
    computer_cost = fellow.computer.cost
    sum_paid = float(computer_cost) / float(payment_plan.plan_duration)
    for i in xrange(0, months):
        payment = PaymentHistory(fellow=fellow, sum_paid=sum_paid, payment_plan=payment_plan)
        payment.save()
        continue
    return 'Created'


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def add_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month / 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day, [31,
                       29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)

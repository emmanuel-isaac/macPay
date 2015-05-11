from apps.payment.models import PaymentHistory



def create_payment_history(months, fellow):
    payment_plan = fellow.recent_payment_plan
    computer_cost = fellow.computer.cost
    sum_paid = float(computer_cost) / payment_plan.plan_duration
    for i in xrange(0, months):
        payment = PaymentHistory(fellow=fellow, sum_paid=sum_paid, payment_plan=payment_plan)
        payment.save()
        continue
    return 'Created'
AUTO_REFUND_LIMIT = 100.0

def can_auto_refund(amount):
    return 0 < amount <= AUTO_REFUND_LIMIT

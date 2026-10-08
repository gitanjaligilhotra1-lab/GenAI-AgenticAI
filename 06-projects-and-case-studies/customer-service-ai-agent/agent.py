import re
from guardrails import can_auto_refund
from rag import search_policy
from tools import create_refund, create_replacement, get_order

class CustomerSupportAgent:
    def __init__(self):
        self.last_order_id = None
        self.pending_action = None

    def chat(self, message):
        text = message.lower().strip()
        order_id = self._order_id(message) or self.last_order_id
        if order_id:
            self.last_order_id = order_id

        confirmations = {"yes", "yes please", "confirm", "please do"}
        cancellations = {"no", "cancel", "no thanks"}
        if self.pending_action and text not in confirmations | cancellations:
            self.pending_action = None

        if self.pending_action and text in confirmations:
            action = self.pending_action
            self.pending_action = None
            if action["type"] == "refund":
                order = get_order(action["order_id"])
                amount = action["amount"]
                if not order or amount <= 0 or amount > order["price"] or not can_auto_refund(amount):
                    return "Refund no longer eligible. No refund was executed."
                refund_id = create_refund(action["order_id"], amount)
                return ("Refund created successfully. Refund ID: " + refund_id) if refund_id else "Refund failed. No refund was executed."
            if action["type"] == "replacement":
                replacement_id = create_replacement(action["order_id"])
                return "Replacement created successfully.\nReplacement ID: %s\nPolicy: %s" % (replacement_id, action["policy"])

        if self.pending_action and text in cancellations:
            self.pending_action = None
            return "Okay. I did not create the pending action."

        if "policy" in text or ("return" in text and "refund" not in text):
            hit = search_policy(message)
            return (hit["text"] + "\nSource: " + hit["source"]) if hit else "I could not find an approved policy."

        if "damaged" in text or "replace" in text:
            if not order_id:
                return "Please provide an order ID, for example ORD-1001."
            order = get_order(order_id)
            if not order:
                return "I could not find that order."
            if not order["delivered"]:
                return "This order has not been delivered yet, so damaged-item replacement is not available. Shipping support should investigate delivery status."
            policy = search_policy("damaged replacement")
            self.pending_action = {"type": "replacement", "order_id": order_id, "policy": policy["source"]}
            return "%s is eligible for damaged-item replacement under %s. Would you like me to create the replacement?" % (order["item"], policy["source"])

        if "refund" in text:
            if not order_id:
                return "Please provide the order ID you want refunded."
            order = get_order(order_id)
            if not order:
                return "I could not find that order."
            if re.search(r"\$\s*[-+]", message):
                return "Please provide a valid positive refund amount."
            amount = self._amount(message)
            if "$" in message and amount is None:
                return "Please provide a valid refund amount with at most two decimal places."
            if amount is None:
                amount = order["price"]
            if amount <= 0:
                return "Refund amount must be greater than zero. No refund was executed."
            if amount > order["price"]:
                return "I cannot refund more than the item price ($%.2f)." % order["price"]
            if not can_auto_refund(amount):
                return "A $%.2f refund requires human approval. No refund was executed." % amount
            self.pending_action = {"type": "refund", "order_id": order_id, "amount": amount}
            return "Please confirm a $%.2f refund for %s. Would you like me to create the refund?" % (amount, order_id)

        return "I can help with return policy, damaged-item replacements, and refunds. Try order ORD-1001."

    @staticmethod
    def _order_id(message):
        match = re.search(r"ORD-\d+", message.upper())
        return match.group(0) if match else None

    @staticmethod
    def _amount(message):
        match = re.search(r"\$\s*(\d+(?:\.\d{1,2})?)", message)
        return float(match.group(1)) if match else None

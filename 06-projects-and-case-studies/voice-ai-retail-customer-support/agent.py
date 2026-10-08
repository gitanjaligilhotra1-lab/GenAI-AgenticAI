import re
from tools import create_replacement, get_order
from rag import search_policy

class VoiceRetailAgent:
    def __init__(self):
        self.order_id=None
        self.pending=None

    def handle_turn(self,message):
        text=message.lower().strip()
        match=re.search(r"ORD-\d+",message.upper())
        if match:
            new_order_id = match.group(0)
            if new_order_id != self.order_id:
                self.pending = None
            self.order_id = new_order_id
        confirmations = {"yes", "yes please", "confirm", "please do"}
        cancellations = {"no", "cancel", "no thanks"}
        if self.pending and text not in confirmations | cancellations:
            self.pending = None

        if self.pending and text in confirmations:
            pending=self.pending; self.pending=None
            replacement=create_replacement(pending["order_id"])
            return "Confirmed. Replacement created for %s. Reference %s."%(pending["order_id"],replacement)
        if self.pending and text in cancellations:
            self.pending=None; return "Okay. I will not create the replacement."

        if "where" in text or "status" in text:
            order=get_order(self.order_id) if self.order_id else None
            return ("Your "+order["item"]+" is "+order["status"]+".") if order else "Please tell me your order ID."

        if "damaged" in text or "replace" in text:
            if not self.order_id: return "I can help. What is the order ID?"
            order=get_order(self.order_id)
            if not order: return "I could not find that order. Please repeat the order ID."
            if not order["delivered"]: return "That order has not been delivered yet, so I cannot create a damaged-item replacement."
            policy=search_policy("damaged delivered replacement confirmation")
            self.pending={"type":"replacement","order_id":self.order_id,"policy":policy["source"]}
            return "%s is eligible for replacement under %s. Would you like me to create it?"%(order["item"],policy["source"])

        if "return" in text or "policy" in text:
            hit=search_policy(message); return hit["text"]+"\nSource: "+hit["source"] if hit else "I could not find an approved policy."
        return "I can help with order status, returns, or a damaged item."

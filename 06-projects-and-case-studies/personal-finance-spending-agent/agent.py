import re
from decimal import Decimal, InvalidOperation
from tools import transactions, monthly_income

D = lambda value: Decimal(str(value))

def money(value):
    return "$" + format(value.quantize(Decimal("0.01")), ",.2f")

class FinanceAgent:
    def chat(self, question):
        tx = transactions()
        text = question.lower().strip()
        income = D(monthly_income())
        spending = sum((-D(x["amount"]) for x in tx if D(x["amount"]) < 0), Decimal("0"))
        surplus = income - spending
        if "subscription" in text or "recurring" in text:
            rows = [x for x in tx if x.get("recurring") and D(x["amount"]) < 0]
            if not rows:
                return "No recurring expenses are marked in the sample data."
            total = sum((-D(x["amount"]) for x in rows), Decimal("0"))
            return "\n".join(f'{x["merchant"]}: {money(-D(x["amount"]))}/month (sample assumption)' for x in rows) + "\nTotal marked recurring: " + money(total) + "/month."
        if "unusual" in text or "large purchase" in text:
            rows = [x for x in tx if x.get("category") == "shopping" and -D(x["amount"]) > D("300")]
            if not rows:
                return "No shopping purchases above the illustrative $300 threshold."
            return "Flagged by simple threshold (not statistical anomaly detection): " + ", ".join(f'{x["merchant"]} {money(-D(x["amount"]))}' for x in rows)
        if "afford" in text or "purchase" in text:
            match = re.search(r"(?<![\w.])\$?([0-9]+(?:\.[0-9]{1,2})?)(?![\w.])", text)
            if not match:
                return "Please provide a purchase amount, for example: can I afford 1500?"
            try:
                price = D(match.group(1))
            except InvalidOperation:
                return "Please provide a valid purchase amount."
            if price <= 0:
                return "Please provide a positive purchase amount."
            return (f"Illustrative sample-month surplus: {money(surplus)}. "
                    f"After a {money(price)} purchase: {money(surplus - price)}. "
                    "This does not account for savings, debt, future bills, or timing and is not a reliable affordability determination or financial advice.")
        if "summary" in text or "spend" in text or not text:
            return f"Sample monthly income: {money(income)}\nRecorded spending: {money(spending)}\nIllustrative remainder: {money(surplus)}"
        return "Try: summary, subscriptions, unusual, or can I afford 1500."

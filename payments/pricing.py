from decimal import Decimal
from .models import PricingRule

def calculate_adjusted_charge(total_amount: Decimal, fee_count: int, base_charge: Decimal) -> Decimal:
    """
    Calculate the adjusted service charge based on pricing rules.
    
    Args:
        total_amount (Decimal): The total amount of fees selected (sum of fee totals).
        fee_count (int): Number of fees selected.
        base_charge (Decimal): The base admin/service charge before adjustments.
    
    Returns:
        Decimal: The adjusted charge after applying pricing rules.
    """

    # Fetch all active pricing rules ordered by min_total_amount then min_fee_count
    pricing_rules = PricingRule.objects.filter(is_active=True).order_by('min_total_amount', 'min_fee_count')

    for rule in pricing_rules:
        if rule.applies_to(total_amount, fee_count):
            if rule.rule_type == PricingRule.RULE_TYPE_FLAT:
                # If flat fee, override the charge with rule value
                return rule.value
            elif rule.rule_type == PricingRule.RULE_TYPE_PERCENT:
                # If percent, calculate discount on base charge
                discount = (rule.value / Decimal('100')) * base_charge
                adjusted = base_charge - discount
                return max(adjusted, Decimal('0'))  # Ensure non-negative
    # No rule matched, return base charge
    return base_charge

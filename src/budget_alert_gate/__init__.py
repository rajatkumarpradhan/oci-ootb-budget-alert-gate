"""Offline preview of OCI Budget alert thresholds, not OCI's forecast engine."""
from decimal import Decimal, InvalidOperation

def number(value):
    try:
        n=Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('invalid amount') from exc
    if not n.is_finite() or n < 0: raise ValueError('amount must be finite and non-negative')
    return n

def evaluate(budget, actual, forecast, rules):
    budget=number(budget)
    if budget == 0: raise ValueError('budget must be positive')
    values={'ACTUAL':number(actual),'FORECAST':number(forecast)}
    results=[]
    for rule in rules:
        kind=rule['type']; mode=rule['threshold_type']
        if kind not in values or mode not in ('PERCENTAGE','ABSOLUTE'):
            raise ValueError('unsupported alert rule')
        threshold=number(rule['threshold'])
        boundary=budget * threshold / 100 if mode=='PERCENTAGE' else threshold
        # Local preview convention includes equality. Not a delivery guarantee.
        results.append({'name':rule['name'],'type':kind,'boundary':str(boundary),
                        'observed':str(values[kind]),'triggered':values[kind]>=boundary})
    return results

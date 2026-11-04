from budget_alert_gate import evaluate
rules=[{'name':'actual-80','type':'ACTUAL','threshold_type':'PERCENTAGE','threshold':80},
       {'name':'forecast-100','type':'FORECAST','threshold_type':'PERCENTAGE','threshold':100}]
for label,actual,forecast,expected in [('healthy',20,60,0),('forecast warning',60,120,1),('both warning',90,130,2)]:
    result=evaluate(100,actual,forecast,rules)
    fired=[r['name'] for r in result if r['triggered']]
    assert len(fired)==expected
    print(f'{label}: actual={actual}, forecast={forecast}, fired={fired}')
print('DEMO OK: 3 snapshots, healthy -> forecast warning -> actual and forecast warnings')

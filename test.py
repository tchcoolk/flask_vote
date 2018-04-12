v = dict.fromkeys(['k1', 'k2'], [])
v['k1'].append(666)
print(v)
v['k1'] = 777
print(v)

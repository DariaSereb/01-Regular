import sys
import numpy
import scipy
import json
import pandas
from scipy import stats, cumsum
from datetime import datetime
from scipy.optimize import optimize

data = pandas.read_csv(sys.argv[1])
out = {}

if sys.argv[2] == 'average':
    data.loc['mean'] = data.mean()
    data = data.tail(1)
else:
    id = int(sys.argv[2])
    data = data.loc[data['student'] == id]



data = data.drop('student', axis='columns')
exercise = data.rename(lambda x: x.split('/')[1].strip(), axis='columns')
exercise = exercise.groupby(by=exercise.columns, axis=1).sum()
out['mean'] = exercise.mean(axis=1).iloc[0]
out['median'] = exercise.median(axis=1).iloc[0]
out['passed'] = int(exercise.iloc[0].astype(bool).sum())
out['total'] = exercise.sum(axis=1).iloc[0]

pul_rok = datetime.strptime('2018-09-17', '%Y-%m-%d').toordinal()
data = data.rename(lambda x: x.split('/')[0].strip(), axis='columns')
data = data.rename(lambda x: datetime.strptime(x, '%Y-%m-%d').toordinal() - pul_rok, axis='columns')
data = data.groupby(by=data.columns, axis=1).sum()
data = data.reindex(sorted(data.columns), axis=1)
points = cumsum(data, axis=1)
slp = scipy.optimize.curve_fit(lambda x, m: m*x, list(data.columns.values), points.iloc[0])[0][0]

if slp != 0:
    out['regression slope'] = slp
    out['date 16'] = str(datetime.fromordinal(pul_rok + int(round(16 / slp))).date())
    out['date 20'] = str(datetime.fromordinal(pul_rok + int(round(20 / slp))).date())
else:
    out['regression slope'] = 0

print(json.dumps(out, ensure_ascii=False, indent=2))

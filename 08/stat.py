import sys
import pandas
import json

data = pandas.read_csv(sys.argv[1])
data = data.drop("student", axis='columns')

if sys.argv[2] == 'dates':
    data = data.rename(lambda x: x.split('/')[0].strip(), axis='columns')
elif sys.argv[2] == 'exercises':
    data = data.rename(lambda x: x.split('/')[1].strip(), axis='columns')
elif sys.argv[2] == 'deadlines':
    data = data.rename(lambda x: x.strip(), axis='columns')
else:
    print("Invalid option", file=sys.stderr)

data = data.groupby(by=data.columns, axis=1).sum()
out = {}

for column in data:

    out[column] = {
        "mean": data[column].mean(),
        "median": data[column].median(),
        "first": data[column].quantile(0.25),
        "last": data[column].quantile(0.75),
        "passed": int(data[column].astype(bool).sum()),
    }

print(json.dumps(out, ensure_ascii=False, indent=2))

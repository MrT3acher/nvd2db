# nvd2db
Convert NVD JSON Feed to database (sqlite supported at this time)

## How to Use?

to initialize the database:

```
python -m nvd2db init
```

to convert JSON Feeds of 2021 and 2022 you can run command below: (you can also add other years as argument)

```
python -m nvd2db convert nvdcve-1.1-2022.json nvdcve-1.1-2021.json
```


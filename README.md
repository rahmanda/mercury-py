# Mercury-py

Mercury-py is complementary script for Kibana to help you data cleaning against json formatted log. It reads exported csv from [ElasticSearch CSV Exporter](https://chrome.google.com/webstore/detail/elasticsearch-csv-exporte/kjkjddcjojneaeeppobfolgojhohbpjn?hl=en) chrome extension, then produce clean csv file out of json formatted field.

## How to use
1. Install mercury-py first via `pip install git+https://github.com/rahmanda/mercury-py.git`.
2. Run this command `mercury` on your console.
3. Enter csv file and json rule file in your directory.
4. Your exported csv file will be created on your current directory under name 'exported_csv.csv'.

## Json rule
Below is valid example of json rule. You can also find it under `src/mercury_py/example_rule.json` directory on this repository.
```json
{
  "column_names": ["booking message", "timestamp", "first name", "title", "pax type", "last name", "birth date"],
  "rules": {
    "0": {
      "filter": [
        ["Status", "Message"]
      ]
    },
    "1": {
      "no_json": true
    },
    "2": {
      "entry_point": ["Passengers", {"name": "0", "hash_type": "int"}],
      "filter": [
        "FirstName",
        "Title",
        "PaxType",
        "LastName",
        "BirthDate"
      ]
    }
  }
}
```
Key `rules` contains rule of every column you want to extract. For json formatted column, we should provide `entry_point` and `filter` list. Both of lists can contain plain string, dictionary, or list value.

If we provide list, the program will trace all keys until the last key to get the value we want. Let say one of your field looks like this.
```
"{""Status"":{""Message"":""Booking failed.""}}"
```
According to this filter `["Status", "Message"]`, it will produce value `Booking failed.`

If we provide dictionary, it will reformat the key or the value before adding to final result. Let say one of your field looks like this.
```
"{""Passengers"": [{""FirstName"": ""Rahmanda"", ""Title"": ""MR"", ""PaxType"": ""ADT"", ""LastName"": ""Wibowo"", ""BirtDate"": ""2012-01-01""}]}"
```
According to this entry point rule `["Passengers", {"name": "0", "hash_type": "int"}]`, we start fetching data from `['Passengers'][0]` key, then get the data based on filter rule.

If we don't want the program to parse certain field into json, we have to provide `"no_json": true`.

## Options
`--csv`: Directory path of consummable csv (required).
`--rule`: Directory path of json rule (required).
`--csv-delimiter` : Specify csv delimiter. Default value ',' (optional).
`--export` : Directory path of exported csv. Default value 'exported_csv.csv' (optional).

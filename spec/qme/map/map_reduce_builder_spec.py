import json
import time

COMPLEX_MEASURE_JSON = """
{
  "id": "0043",
  "name": "Pneumonia Vaccination Status for Older Adults",
  "steward": "NCQA",
  "population": {
    "and": [
      {
        "category": "Patient Characteristic",
        "title": "Age > 17 before measure period",
        "query": {"age": {"_gt": 17}}
      },
      {
        "category": "Patient Characteristic",
        "title": "Age < 75 before measure period",
        "query": {"age": {"_lt": 75}}
      },
      {
        "or": [
          {
            "category": "Patient Characteristic",
            "title": "Male",
            "query": {"sex": "male"}
          },
          {
            "category": "Patient Characteristic",
            "title": "Female",
            "query": {"sex": "female"}
          }
        ]
      }
    ]
  },
  "denominator": {},
  "numerator": {},
  "exception": {}
}
"""

MAP_FUNCTION = """
function () {
  var value = {i: 0, d: 0, n: 0, e: 0};
  if (this.birthdate<=-764985600) {
    value.i++;
    if (this.measures["0043"].encounter>=1253318400) {
      value.d++;
      if (this.measures["0043"].vaccination==true) {
        value.n++;
      } else if (false) {
        value.e++;
        value.d--;
      }
    }
  }
  emit(null, value);
};
"""

# Assuming you have a Python version of the `Builder` class from the previous conversation
# measure_json = ...
# hash = json.loads(measure_json)
date = time.mktime(time.strptime("2010-09-19", "%Y-%m-%d"))
measure = Measure(hash, {"effective_date": date})
builder = Builder(hash, {"effective_date": date})
assert builder.numerator == '(this.measures["0043"].vaccination==true)'
assert builder.denominator == f'(this.measures["0043"].encounter>={measure.parameters["earliest_encounter"]})'
assert builder.population == f'(this.birthdate<={measure.parameters["earliest_birthdate"]})'
assert builder.exception == '(false)'
assert builder.map_function == MAP_FUNCTION
assert builder.reduce_function == Builder.REDUCE_FUNCTION

# ...
hash = json.loads(COMPLEX_MEASURE_JSON)
measure = Measure(hash, {})
builder = Builder(hash, {})
assert builder.population == '((this.measures["0043"].age>17)&&(this.measures["0043"].age<75)&&((this.measures["0043"].sex=="male")||(this.measures["0043"].sex=="female")))'

import base64
import re


def decode_and_transform(values, dynamic_value):
    result = ""
    for value in values:
        decoded_value = base64.b64decode(value).decode("utf-8")
        numeric_value = int("".join(filter(str.isdigit, decoded_value))) - dynamic_value
        char_value = chr(numeric_value)
        result += char_value
    return result


def extract_values_from_javascript(js_code):
    # Extract dynamic variable names and their values using regular expressions
    pattern = r"var (\w+) = (\[[^\]]+\]);"
    matches = re.findall(pattern, js_code)
    return eval(matches[0][1])


def extract_dynamic_value(js_code):
    # Extract dynamic value from the JavaScript code
    # )) - 12345678)
    pattern = r"\)\s*-\s*(\d+)"
    match = re.search(pattern, js_code)

    if match:
        return int(match.group(1))
    else:
        return 0  # Default value if dynamic value is not found


def execute_javascript_code(js_code):
    # Extract variable values from the JavaScript code
    variable_values = extract_values_from_javascript(js_code)
    dynamic_value = extract_dynamic_value(js_code)
    data = decode_and_transform(variable_values, dynamic_value)
    return data


# Example usage
js_code = """
var HyV = ""; var ZmK = ["dGZ4Nzc4MjQ4NTdyVG8=","T0JLNzc4MjQ4NjJDQnM=","VXNLNzc4MjQ4NzVFcUc=","ZnNUNzc4MjQ4MTlNbmw=", "cm9nNzc4MjQ3NjdBZVY="];
ZmK.forEach(function WdX(value) { HyV += String.fromCharCode(parseInt(atob(value).replace(/\D/g,'')) - 77824757); } );
document.write(decodeURIComponent(escape(HyV)));
"""

results = execute_javascript_code(js_code)
print(results)

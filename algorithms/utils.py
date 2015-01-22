from math import log
from collections import Counter
import sys

class InvalidDataError(Exception):
    pass

def gain(data, target_attribute, target_attrib_entropy, attribute):
    attrib_gain = target_attrib_entropy
    attribute_values = [record[attribute] for record in data]
    total = len(attribute_values)
    count = Counter(attribute_values)
    for key in count:
        p = count[key]/float(total)
        attrib_values = [record[target_attribute] for record in data if record[attribute] == key]
        attrib_gain -= p * entropy(Counter(attrib_values),len(attrib_values))

    return attrib_gain

def continuous_gain(data, target_attribute, target_attrib_entropy, attribute):
    try:
        local_data = [(float(record[attribute]), record[target_attribute]) for record in data]
    except ValueError:
        raise InvalidDataError("Unable to convert continuous data to float values.")
    local_data.sort(key=lambda x: x[0])
    smaller_values = Counter()
    bigger_values = Counter(record[1] for record in local_data)

    min_entropy = 1.0
    threshold = None
    count = 0
    total = len(local_data)

    for n in range(0, total - 1):
        count += 1
        smaller_values[local_data[n][1]] += 1
        bigger_values[local_data[n][1]] -= 1

        if local_data[n][0] != local_data[n+1][0]:
            p = count/total
            new_entropy = p * entropy(smaller_values, count)
            new_entropy += (1-p) * entropy(bigger_values, total-count)
            if new_entropy < min_entropy:
                min_entropy = new_entropy
                threshold = local_data[n][0]

    return (target_attrib_entropy - min_entropy, threshold)

def entropy(count, total):
    entropy = 0
    for key in count:
        if count[key] != 0:
            p = count[key]/float(total)
            entropy -= p * log(p, 2)

    return entropy

def is_continuous_attribute(attribute):
    return attribute[0] == '*'

def read_option(text = None, fail_text = None, conversion = None, condition = None):
    while True:
        if text:
            sys.stdout.write(text)
        option = sys.stdin.readline()
        if conversion:
            try:
                option = conversion(option)
            except:
                if fail_text:
                    sys.stdout.write(fail_text)
            else:
                if condition:
                    if condition(option):
                        break
                    else:
                        if fail_text:
                            sys.stdout.write(fail_text)
                else:
                    break

    return option

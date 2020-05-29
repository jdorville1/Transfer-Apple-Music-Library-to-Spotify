import math
import re
from collections import Counter


word = re.compile(r"[\w&-]+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    print(intersection)
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    print(numerator)

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return numerator / denominator


def text_to_vector(text):
    words = word.findall(text.lower())
    return Counter(words)


text1 = "197250 hello"
text2 = "197251 hello"

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)

cosine = get_cosine(vector1, vector2)

print("Cosine:", cosine)



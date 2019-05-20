#!/usr/local/bin/python3
#https://docs.python.org/2/library/collections.html
#https://docs.python.org/3/library/urllib.request.html
#https://docs.python.org/3/howto/regex.html

from collections import defaultdict
from collections import Counter
import urllib.request
import re

def nGrams(content, n):
    content = '~' + content + '~'
    dd = defaultdict(Counter)
    for i in range(len(content)-n):
        prefix = content[i:i+n]
        dd[prefix][content[i+n]] += 1
    result = defaultdict(dict)
    for pre, chars in dd.items():
        totalCount = sum(chars.values())
        for key, value in chars.items():
            result[pre][key] = value/totalCount
    return result

def spellCorrecly(word, n, forward, backward):
    def prop(s, nGrams):
        result = 1.0
        found = False
        for i in range(len(s)-n):
            d = nGrams[s[i:i+n]]
            if s[i+n] in d:
                found = True
                result = result * d[s[i+n]]
        if not found:
            return 0.0
        maxValue = 0.0
        for key, val in nGrams[s[len(s)-n:]].items():
            if key != '~':
                maxValue = max(maxValue, val)
        if maxValue > 0.5:
            return 0.0
        return result
    if len(word) < n:
        return False
    score = prop(word, forward) * prop(word[::-1], backward)
    return score > 0.1

if __name__ == "__main__":
    request = urllib.request.Request(url='https://www.blognone.com/node/109862', method='GET')
    response = urllib.request.urlopen(request).read()
    content = response.decode('utf8')
    thaiContent = re.sub('[^ก-๙]', '', content)
    forward = nGrams(thaiContent, 4)
    backward = nGrams(thaiContent[::-1], 4)
    print(spellCorrecly('คอมพิวเตอร์', 4, forward, backward))
    print(spellCorrecly('ดอมพิวเตอร์', 4, forward, backward))
    print(spellCorrecly('ระคับประคอง', 4, forward, backward))
    print(spellCorrecly('ประคับประคอง', 4, forward, backward))
    print(spellCorrecly('ประคับประคอ', 4, forward, backward))
    print(spellCorrecly('หัวเว้ย', 4, forward, backward))
    print(spellCorrecly('หัวเว่ย', 4, forward, backward))
    print(spellCorrecly('หัวเหว่ย', 4, forward, backward))

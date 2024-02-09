probabilities = {'4.html': 0.25, '3.html': 0.25, '2.html': 0.25, '1.html': 0.25}
page_i = {'4.html': 1, '3.html': 2, '1.html': 1}

# Divide values in probabilities by values in page_i with the same key
result = {key: probabilities[key] / page_i[key] for key in set(probabilities) & set(page_i)}

print(result)

def find_median(data) -> int:
    if isinstance(data, dict):
        sorted_values = sorted(data.values())
    elif isinstance(data, list):
        sorted_values = sorted(data)
    
    length = len(sorted_values)
    middle = length // 2
    
    if length % 2 != 0:
        return sorted_values[middle]
    else:
        return (sorted_values[middle - 1] + sorted_values[middle]) / 2

def filter_upper_half(data: dict):
    upper_half = dict()
    for id, kw_quantity in data.items():
        if kw_quantity >= find_median(data):
            upper_half[id] = kw_quantity
    return upper_half 

def filter_on_top(data: dict, depth):
    print(len(data))
    result = filter_upper_half(data)
    for _ in range(depth):
        result = filter_upper_half(result)
    
    print(len(result))
    return result

def find_matches(text, phrase):
    text_list = text.lower().split()
    query_words = phrase.lower().split()

    phrase_matches = 0

    # Проходимся по тексту, чтобы найти вхождения фразы
    for i in range(len(text_list)):
        if query_words[0] in text_list[i]:
            # Если первое слово фразы найдено, проверяем, следует ли за ним остальные слова фразы
            try:
                if all(query_words[j] in text_list[i + j] for j in range(len(query_words))):
                    phrase_matches += 1
            except Exception:
                pass
    return phrase_matches
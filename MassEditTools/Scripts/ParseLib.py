def smart_count(string, character, end = None):
    """
    Counts how many characters are in a string, up to a certain index, while ignoring those characters which are inside a string
    """
    if end is not None:
        string = string[:end]
    while '"' in string: #Remove all FT strings from the given string
        start = string.find('"')
        end = string.find('"', start+1)
        string = string[:start] + (string[end+1:] if end >= 0 else "")
    if isinstance(character, str):
        return string.count(character)
    elif isinstance(character, (list, tuple)): #If a list of characters is passed in, count for all of them. This can help improve performance by skipping the "" removal when multiple things need to be counted.
        return [string.count(char) for char in character]


def smart_split(string, operators, search_dir = 0, strip_spaces = True):
    """
    Finds the first instance of an operator in a string that is not inside brackets (it can itself still be brackets though), nor inside a conditional block, and returns:
    (left, operator, right)

    search_dir:
    0 - Left to right
    1 - Right to left
    
    If no valid operator is found, will return:
    (string, None, None)
    Note:
    Only splits one time.
    """
    if isinstance(operators, str):
        operators = [operators]
    index = len(string) if search_dir else -1
    while True:
        if search_dir:
            #Find the operator in the string that ends at the latest possible
            # point. If multiple operators end at the same point (e.g. lerp and
            # inverselerp in "inverselerp(1, 2)", pick the longest one, as that
            # means the other operator is simply a substring of the other
            # operator, which should thus get priority
            index = max([(string.rfind(operator, 0, index), len(operator)) for operator in operators if string.rfind(operator, 0, index) >= 0], default = (-1, 0), key = lambda x: (sum(x), x[1]))[0]
        else:
            index = min([(string.find(operator, index + 1), -len(operator)) for operator in operators if string.find(operator, index + 1) >= 0], default = (-1, 0))[0]
        #If the operator doesn't exist (outside of brackets), return 3 * (None,)
        if index == -1:
            return (string, None, None)
        
        #If the index is inside brackets:
        if smart_count(string, "(", index) != smart_count(string, ")", index):
            continue #Move on to the next round

        #If the index is inside a string:
        if string.count('"', 0, index) % 2:
            continue

        
        
        #Find which operator was actually indexed
        #This can NOT be done in the min(___) line, as some operators are a
        # substring of another operator, which could otherwise incorrectly make
        # the wrong operator be assumed.
        #To find the correct operator, look for the longest operator which'
        # string fits at the index

        #Iterate over all operators, sorted by length descending
        for operator in sorted(operators, key = len, reverse = True):
            #If the operator matches what is in the string, and the operator is
            # indeed an operator, and not part of a variable name:
            if operator == string[index:index + len(operator)] and not (operator[-1].isalpha() and string[index + len(operator) : index + len(operator) + 1].isalpha()):
                break
        else: #If no break
            #If no operator matched, and this was thus a false positive due to
            # variable naming
            continue

        if string[index+1:index+2] == "=" and operator != "==": #Do not parse e.g. += as "+", or |= as "="
            continue

        #returns (left, operator, right)
        if strip_spaces:
            return (string[:index].strip(" "), operator, string[index + len(operator):].strip(" "))
        else:
            return (string[:index], operator, string[index + len(operator):])

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

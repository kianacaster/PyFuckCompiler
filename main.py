import sys

TOKENS = {
    "+":"ADD",
    "-":"SUB",
    "<":"MVL",
    ">":"MVR",
    ".":"OUT",
    "[":"LST",
    "]":"LFN",
    ",":"INP"
}

def run_length_encoding(string):
    if len(string) < 1:
        return 0

    count = 1
    rle_string = []
    for i in range(len(string) - 1):
        if string[i] == string[i + 1] and count < 9:
            count = count + 1
        else:
            rle_string.append(str(count) + string[i])
            count = 1
    rle_string.append(str(count) + string[-1])
    return ''.join(rle_string)


def tokenise(rle_encoded_string):
    count = 0
    token_str = []
    for c in rle_encoded_string:
        if c in '0123456789':
            token_str.append(" " + c)
        else:
            if c in TOKENS:
                token_str.append(TOKENS[c])
    token_str.append(' ')
    return ''.join(token_str)[1::]

def sanitise(code):
    cleaned_code = ""
    for char in code:
        if char in TOKENS:
            cleaned_code += char
    return cleaned_code

def compile_to_encoded_tokens(source_code):
    return tokenise(run_length_encoding(sanitise(source_code)))

def get_token():
    return {
        "Value": "",
        "Count": 0,
        "Children": [],
        "Parent": None
    }

def generate_tree(token_string):
    token_list = []
    tmp_token = get_token()
    for c in token_string:
        if c in '0123456789':
            tmp_token["Count"] = int(c)
        elif c in "ADSUFBMVLROTNIP":
                tmp_token["Value"] += c
        elif c == ' ':
            token_list.append(tmp_token)
            tmp_token = get_token()
    head_node = get_token()
    parent = head_node
    for tk in token_list:
        tk["Parent"] = parent
        if tk['Value'] == 'LST':
            tk["Parent"] = parent
            parent["Children"].append(tk)
            parent = tk
        elif tk['Value'] == 'LFN':
            parent["Children"].append(tk)
            parent = parent["Parent"]
        else:
            parent["Children"].append(tk)
    return head_node

def print_tree(head):
    if head["Value"] != " " and head["Count"] != 0:
        print(str(head["Count"]) + head["Value"])
    if len(head["Children"]) > 0:
        for token in head["Children"]:
            print_tree(token)

def main(src):
    tokens = compile_to_encoded_tokens(src)
    tree = generate_tree(tokens)
    python_code = compile_to_python(tree)
    with open("output.py", "w", encoding="utf-8") as f:
        f.write(python_code)
if __name__ == "__main__":
    args = sys.argv
    global source
    source = ""
    if len(args) < 2:
        print("Requires arguments. Use -h or --help")
    elif args[1] == "--file" or args[1] == "-f":
        file_src = args[2]
        with open(file_src, 'r') as file:
            source = ''.join(file.readlines())
    elif args[1] == "--string" or args[1] == '-s':
        source = args[2]
    elif args[1] == "--help" or args[1] == '-h':
        print("Help!")
    elif args[1] is not None: 
        print("Invalid option")
    if source:
        main(source)
    else:
        print("No sourcecode provided")
    
        
        

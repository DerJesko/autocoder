import sys
import os
import chardet
import string

output_directory = sys.argv[2]

def split_letters(s):
    result = []
    for letter in s:
        if letter == " ":
            result.append("sc")
        elif letter == "\t":
            result.append("tb")
        elif letter == "\r":
            pass
        elif letter == "\n":
            result.append("lb")
        elif letter in string.whitespace:
            result.append("ws")
        else:
            result.append(letter)
    return result


for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith(".c"):
            try:
                with open(root + "/" + file, "rb") as f:
                    enc = chardet.detect(f.read())["encoding"]
                with open(root + "/" + file, encoding=enc) as f:
                    s = f.read()
                letters = ' '.join(split_letters(s))
                hash_ = abs(hash(letters))
                project = (root.split("/"))[3]
                with open(output_directory + project + "." + str(hash_) + ".txt", "w") as f:
                    f.write(letters)
            except (UnicodeDecodeError):
                print("UnicodeDecodeError: " + root + "/" + file)
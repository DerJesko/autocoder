import sys
import os
from hashlib import sha256
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

lexer = get_lexer_by_name("c")

def simplify(s):
    tokens = lexer.get_tokens(s)
    stripped = []
    preprocfiles = dict()
    var_names = dict()
    var_tokens = {Token.Name, Token.Name.Attribute, Token.Name.Class, Token.Name.Constant, Token.Name.Decorator, Token.Name.Entity, Token.Name.Exception, Token.Name.Function, Token.Name.Function.Magic, Token.Name.Label, Token.Name.Namespace, Token.Name.Other. Token.Name.Tag, Token.Name.Variable, Token.Name.Variable.Class, Token.Name.Variable.Global, Token.Name.Variable.Instance, Token.Name.Variable.Magic}
    builtin_tokens = {Token.Keyword, Token.Keyword.Constant, Token.Keyword.Declaration, Token.Keyword.Namespace, Token.Keyword.Pseudo, Token.Keyword.Reserved, Token.Keyword.Type,
        Token.Name.Builtin, Token.Name.Builtin.Pseudo, Token.Punctuation, Token.Operator, Token.Operator.Word}
    string_tokens = {Token.Literal.String, Token.Literal.String.Escape, Token.Literal.String.Affix, Token.Literal.String.Backtick, Token.Literal.String.Delimiter, Token.Literal.String.Doc, Token.Literal.String.Double, Token.Literal.String.Escape, Token.Literal.String.Heredoc, Token.Literal.String.Interpol, Token.Literal.String.Affix, Token.Literal.String.Other, Token.Literal.String.Regex, Token.Literal.String.Single, Token.Literal.String.Symbol}
    comment_tokens = {Token.Comment, Token.Comment.Hashbang, Token.Comment.Multiline, Token.Comment.Single, Token.Comment.Special}
    int_tokens = {Token.Literal.Number, Token.Literal.Number.Bin, Token.Literal.Number.Hex, Token.Literal.Number.Integer, Token.Literal.Number.Integer.Long, Token.Literal.Number.Oct}
    for (tokentype, string) in tokens:
        if tokentype in builtin_tokens:
            stripped.append(string)
        elif tokentype == Token.Comment.Preproc or tokentype == Token.Comment.PreprocFile:
            stripped.append("preproc")
        elif tokentype in comment_tokens:
            stripped.append("comment")
        elif tokentype == Token.Literal.String.Char:
            stripped.append("char")
        elif tokentype in string_tokens:
            stripped.append("string")
        elif tokentype == Token.Literal.Number.Float:
            stripped.append("float")
        elif tokentype in int_tokens:
            try:
                if int(string) <= 20:
                    stripped.append("integer" + str(int(string)))
                else:
                    stripped.append("integer")
            except:
                stripped.append("integer")
        elif tokentype in var_tokens:
            if not (string in var_names):
                var_names[string] = len(var_names)
            stripped.append("var" + str(var_names[string]))
        elif tokentype == Token.Literal.Number.Oct:
            stripped.append("octal")
        elif tokentype == Token.Error:
            stripped.append("error")
        elif tokentype == Token.Text:
            pass
        else:
            print(str((tokentype, string)))
    return stripped

output_directory = sys.argv[2]

for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith(".c"):
            try:
                with open(root + "/" + file) as f:
                    s = f.read()
                simp = ' '.join(simplify(s))
                hash_ = abs(hash(simp))
                project = (root.split("/"))[3]
                #print(project)
                with open(output_directory + project + "." + str(hash_) + ".txt", "w") as f:
                    f.write(simp)
            except (UnicodeDecodeError):
                print("UnicodeDecodeError:" + root + "/" + file)

#print(' '.join(simp))
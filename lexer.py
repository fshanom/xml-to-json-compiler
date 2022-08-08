from sly import Lexer

class XmlToJsonLexer(Lexer):
    # Nomes dos tokens
    tokens = { TEXTO, ABRE_TAG, FECHA_TAG, BARRA }

    # Caracteres que devem ser ignorados
    ignore = '\n\t '

    # Expressões regulares para os tokens
    TEXTO = r'[a-zA-Z0-9_]+' #porque não pode usar a string vazia?
    ABRE_TAG = r'<'
    FECHA_TAG = r'>'
    BARRA = r'/'

if __name__ == '__main__':
    #Carrega arquivo como string para análise léxica
    data = open("/home/fxavier/cefet-rj/comp-2022.1/xml-to-json-compiler/entrada.xml", "r")
    data = data.read()
    lexer = XmlToJsonLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
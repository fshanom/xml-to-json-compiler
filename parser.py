from sly import Parser
from lexer import XmlToJsonLexer

class XmlToJsonParser(Parser):
    # Get the token list from the lexer (required)
    tokens = XmlToJsonLexer.tokens
    debugfile = 'parser.out'

    # Produções semânticas

    # E -> <F>G</F>
    # E -> epsilon
    # F -> tag
    # G -> ZEZ
    # G -> epsilon
    # Z -> G
    # Z -> texto
    # Z -> epsilon

    ''' 
    
    BNF Grammar

    e        : <F> conteudo </F>
             |
    F        : TEXTO
    conteudo : z1 e z2
             | z1
             | z2
             |
    z1       : conteudo
             | TEXTO
             |
    z2       : conteudo
             | TEXTO
             |

    
            Grammar                             Action
    -----------------------------       ---------------------------------
    e        : <F> conteudo </F>        e.val = {F.val : {conteudo.val}}
             |                          e.val = 

    F        : TEXTO                    F.val = "str(TEXTO.val)"

    conteudo : z1 e z2                  conteudo.val = z1.val e.val z2.val
             |                          conteudo.val = 

    z1       : conteudo                 z1.val = conteudo.val
             | TEXTO                    z1.val = "@":"Str(TEXTO.val)",
             |                          z1.val = 

    z2       : conteudo                 z2.val = conteudo.val
             | TEXTO                    z2.val = "@":"Str(TEXTO.val)"
             |                          z2.val = 

    '''

    @_('ABRE_TAG f FECHA_TAG conteudo ABRE_TAG BARRA f FECHA_TAG')
    def e(self, p):
        return "{" + p.f + ": {" + p.conteudo + "}}"

    @_('empty')
    def e(self, p):
        pass

    @_('TEXTO')
    def f(self, p):
        return '"' + p.TEXTO + '"'

    @_('z1 e z2')
    def conteudo(self, p):
        return p.z1 + p.e + p.z2 
    
    @_('empty')
    def conteudo(self, p):
        pass

    @_('conteudo')
    def z1(self, p):
        return p.conteudo

    @_('TEXTO')
    def z1(self, p):
        return '"@"' + ':' + '"' + p.TEXTO + '",'

    @_('empty')
    def z1(self, p):
        pass

    @_('conteudo')
    def z2(self, p):
        return p.conteudo

    @_('TEXTO')
    def z2(self, p):
        return '"@"' + ':' + '"' + p.TEXTO + '"'

    @_('empty')
    def z2(self, p):
        pass

    @_('')
    def empty(self, p):
        pass


if __name__ == '__main__':
    lexer = XmlToJsonLexer()
    parser = XmlToJsonParser()

    
    try:
        #abre xml como uma string
        data = open("/home/fxavier/cefet-rj/comp-2022.1/xml-to-json-compiler/entrada.xml", "r")
        data = data.read()
        
        #passa o xml para o parser
        result = parser.parse(lexer.tokenize(data))
        
        #cria o arquivo traduzido
        saida = open("/home/fxavier/cefet-rj/comp-2022.1/xml-to-json-compiler/saida.json", "w")
        saida.write(str(result))
        saida.close()
    except EOFError:
        print(EOFError)
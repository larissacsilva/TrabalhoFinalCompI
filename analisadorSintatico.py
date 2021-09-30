'''
Aluna: Larissa do Carmo Silva           
RGA: 20171131040

'''

import sys

from analisadorLexico import AnalisadorLexico

class AnalisadorSintatico():

  def __init__(self):
    self.currentLine = 0
    self.currentLexema = 0
    self._allTokens = []
    self.amountLines = 0
    self.amountLexema = 0
    self.tokens = [[]]

  def setTokens(self, generatedTokens):
    self._allTokens = generatedTokens
    self.amountLines = len(self._allTokens)
    self.amountLexema = sum([ len(lineTokens) for lineTokens in self._allTokens])
    self.tokens = self._allTokens


  def _isEmptyLine(self, line):
    return len(line) == 0

  def _nextToken(self):
    
    if(self.currentLexema <= self.amountLexema):       
      self.currentLexema += 1

      print(self.tokens[self.currentLexema])
    else :
      print(" *** [terminatedtokens] *** ")
  
  def _currentToken(self):

    if(len(self.tokens) > 0):
      return self.tokens[self.currentLexema]
    
    return []

  def _getChaveToken(self):
    return (self._currentToken()[0] if len(self._currentToken())> 0 else 'erroReadKey')

  def _getValorToken(self):
    return  (self._currentToken()[1] if len(self._currentToken())> 0 else 'erroReadToken')


# --- --- --- --- Analisador Sintatico --- --- --- ---

  def analyse(self):
    print("\n Rodando [Analisador Sintatico] ------------ \n")
    self._Programa ()
  

  def _Programa(self):
    if(self._getValorToken() == 'program'):
      self._nextToken()
    
      if(self._getChaveToken() == 'ident'):
        self._nextToken()
        self._Corpo()
        if(self._getValorToken() == '.'):
            self._SuccessCode()
        else:
            print("[Programa]- Era esperado um '.'")
            self._Erro()  
      else:
        print("[Programa]- Era esperado um identificador válido ")
        self._Erro()
    else :      
      print("[Programa]- Era esperado program ")
      self._Erro()


  def _Corpo(self):
    self._Dc()

    if(self._getValorToken() == 'begin'):
      self._nextToken()
      self._Comandos()
          
      if(self._getValorToken() == 'end'):
        self._nextToken()
      else:
        print("[Corpo]- Era esperado 'end' " )
        self._Erro()
    else:
      print("[Corpo]- Era esperado 'begin' ")
      self._Erro()


  def _Dc(self):
    if(self._getValorToken() in ['real', 'integer']):
      self._Dc_v()
      self._Mais_dc()
    else:
      self._Vazio()


  def _Mais_dc(self):
    if(self._getValorToken() == ';'):
      self._nextToken()
      self._Dc()
    else:
      self._Vazio()
    

  def _Dc_v(self):
    self._Tipo_var()
          
    if(self._getValorToken() == ':'):
        self._nextToken()
        self._Variaveis()
    else:
        print("[Dc_v]- Era esperado ':' " )
        self._Erro()
    

  def _Tipo_var(self):
    if(self._getValorToken() in ['real', 'integer']):
      self._nextToken()
    else:
      print("[Tipo_var] - Era esperado 'real' ou 'integer'")
      self._Erro()


  def _Variaveis(self):
    if(self._getChaveToken() == 'ident'):
      self._nextToken()
      self._Mais_var()
    else:
      print("[Variaveis] - Era esperado 'identificador' ")
      self._Erro()


  def _Mais_var(self):   
    if(self._getValorToken() == ','):
      self._nextToken()
      self._Variaveis()
    else:
      self._Vazio()


  def _PFalsa(self):
    if(self._getValorToken() == 'else'):
      self._nextToken()
      self._Comandos()
    else:
      self._Vazio()


  def _Comandos(self):
    self._Comando()
    self._Mais_comandos()


  def _Mais_comandos(self):
    if(self._getValorToken() == ';'):
      self._nextToken()
      self._Comandos()
    else: 
      self._Vazio()


  def _Comando(self):
    itemKey = self._getChaveToken()
    itemValue = self._getValorToken()
    if(itemValue == 'read' or itemValue == 'write' ):
      self._nextToken()
      
      if(self._getValorToken() == '('):
        self._nextToken()

        if(self._getChaveToken() == 'ident'):
          self._nextToken()
          if(self._getValorToken() == ')'):
            self._nextToken()
          else :
            print("[Comando]- Era esperado ')'")
            self._Erro()
        else:
          print("[Variaveis] - Era esperado 'identificador' ")
          self._Erro()

      else:
       print("[Comando]- Era esperado '('")
       self._Erro()

    elif(self._getChaveToken() == 'ident'):
      self._nextToken()
      if(self._getValorToken() == ':='):
        self._nextToken()
        self._Expressao()
      else:
        print("[Comando] - Era esperado ':=' ")
        self._Erro()  

    elif(itemValue == 'if'):
      self._nextToken()
      self._Condicao()

      if(self._getValorToken() == 'then'):
        self._nextToken()
        self._Comandos()
        self._PFalsa()
        
        if(self._getValorToken() == '$'):
          self._nextToken()
        else :
          print("[Comando]- Era esperado '$'")
          self._Erro()
      else:
        print("[Comando]- Era esperado 'then'")
        self._Erro()

    else:
      print("[Comando]- Era esperado 'comando' ou 'identificador'")
      self._Erro()



  def _Condicao(self):
    self._Expressao()
    self._Relacao()
    self._Expressao()


  def _Relacao(self):
    if(self._getValorToken() in ["=",">","<",">=","<=","<>"]):
      self._nextToken()
    else:
      print("[Relacao]- Era esperado 'simbolo de relacao'")
      self._Erro()


  def _Expressao(self):
    self._Termo()
    self._Outros_termos()


  def _Op_un(self):
    if(self._getValorToken() in ['-']):
      self._nextToken()
    else:
      self._Vazio()


  def _Outros_termos(self):
    if(self._getValorToken() in ['+', '-']):
      self._Op_ad()
      self._Termo()
      self._Outros_termos()
    else :
      self._Vazio()


  def _Op_ad(self):
    if(self._getValorToken() in ['+', '-']):
      self._nextToken()
    else:
      print("[Op_ad]- Era esperado '+' ou '-'")
      self._Erro()


  def _Termo(self):
    self._Op_un()
    self._Fator()
    self._Mais_fatores()


  def _Mais_fatores(self):
    if(self._getValorToken() in ['*','/']):
      self._Op_mul()
      self._Fator()
      self._Mais_fatores()
    else:
      self._Vazio()


  def _Op_mul(self):
    if(self._getValorToken() in ['*','/']):
      self._nextToken()
    else:
      print("[Op_mul]- Era esperado '*' ou '/'")
      self._Erro()



  def _Fator(self):
    if(self._getValorToken()=="("):
      self._nextToken()
      self._Expressao()
      
      if(self._getValorToken() ==")"):
        self._nextToken()
      else : 
        print("Era esperado ')'")   
        self._Erro()
    elif(self._getChaveToken() in ['ident','num_integer', 'num_real']):
      self._nextToken()
      
    else:
      print("[Fator]- Era esperado '(', 'identificador' ou 'numero'")
      self._Erro()


  def _Vazio (self) :
    pass

  def _Erro (self):
    print('\nEncerrando programa... \n')
    sys.exit()

  def _SuccessCode(self):
    print('[SyntacticAnalyzer] -End \n' )



lex = AnalisadorLexico()
lex.analyse()
tokens = lex._PegarToken()
sint = AnalisadorSintatico()
sint.setTokens(tokens)
sint.analyse()

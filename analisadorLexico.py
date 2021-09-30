'''
Aluna: Larissa do Carmo Silva           
RGA: 20171131040

'''
import sys

class Token():
  def __init__(self, tipo, termo):
    self.tipo = tipo
    self.termo = termo

class AnalisadorLexico () :
  RESERVADAS = ["var", "integer", "real", "if", "then", "while", "do", "write", "read", "begin", "end", "program"]

  def __init__(self):
    self.conteudo = []
    self.table = []
    self.buffer = []
    self.estado = 0
    self.pos = 0
    self.linha = 1
    self.atual = ''
    self.erro = False
    self.token = None
    self.completo = False

  def abrirArquivo (self, filename) :
    with open(filename) as file:
      self.conteudo = file.read()
    self.conteudo += ' '

  def fecharArquivo(self):
    return self.pos == len(self.conteudo)


  def espaco(self, char):
    if(char in ['', ' ', '\n', '\t', '\r'] ):
       if(char=='\n'):
         self.linha += 1
       return True
    return False

  
  def digito(self, char):
    if(char in ['0','1','2','3','4','5','6','7','8','9']):
      self.buffer.append(char)
      return True
    return False 

  def simbolo(self, char):
    if(char in ['(',')','+','-','*','/',',',';',':','.','>','<','=']):
      self.buffer.append(char)
      return True
    return False 

  def alpha(self, char):
    if( char >= 'A' and char <= 'Z' or  char >= 'a' and char <= 'z'):
      self.buffer.append(char)
      return True
    return False


  def apenasAlpha(self, char):
    return char.isalpha()
  
  def apenasNum(self, char):
     return char.isdigit() 

  def apenasSimbolo(self, char):
     return char in '()+-*/.;:<>='
      
      

  def proximoChar(self):
    if( self.fecharArquivo()):
      self.completo = True
      return ' '

    aux = self.conteudo[self.pos]
    
    self.pos += 1

    return aux

  def back(self):
    self.pos -= 1
    self.buffer = []
    return self.conteudo[self.pos]

  def print_table(self):
    for i in self.table:
      print(i)

  def _PegarToken(self):
    return self.table
      

  def analyse(self):
    self.abrirArquivo('exemplo.txt')
    print("\n - Rodando -... ")

    while True : 
      self.proximoSimbolo()
      if (self.token == None):
        break


    print("\n ... - end - ")



  def proximoSimbolo(self):

    self.estado = 0
    self.token = None

    while( not self.completo):

      if(self.estado == 0):
        self.estado0()

      elif(self.estado == 1):
        self.estado1()

      elif(self.estado == 2):
        self.estado2()

      elif(self.estado == 3):
        self.estado3()
      
      elif(self.estado == 4):
        self.estado4()

      elif(self.estado == 5):
        self.estado5()
      
      elif(self.estado == 6):
        self.estado6()

      elif(self.estado == 7):
        self.estado7()
      
      elif(self.estado == 8):
        self.estado8()

      elif(self.estado == 9):
        self.estado9()

      elif(self.estado == 10):
        self.estado10()

      elif(self.estado == 11):
        self.estado11()

      elif(self.estado == 12):
        self.estado12()    
      
      elif(self.estado == 13):
        self.estado13()  
      
  # Estados impl 

  def estado0 (self):
    if(self.espaco(self.atual)):
      self.estado = 0
      self.atual = self.proximoChar()

    elif(self.digito(self.atual)):
      self.estado = 1
      self.atual = self.proximoChar()

    elif(self.alpha(self.atual)):
      self.estado = 6
      self.atual = self.proximoChar()

    elif(self.atual in ['(',')','+','-','*','/',',',';','.','$','=']):
      self.buffer.append(self.atual)
      self.estado = 8
      self.atual = self.proximoChar()

    elif(self.atual in [':', '>']):
      self.buffer.append(self.atual)
      self.estado = 10
      self.atual = self.proximoChar()

    elif(self.atual == '<'):
      self.buffer.append(self.atual)
      self.estado = 12
      self.atual = self.proximoChar()

    else :
      print(f'\n Erro:  estado 0 - char {self.atual}\n')
      self.erro = True
      sys.exit()


  def estado1(self):

    if(self.digito(self.atual)):
      self.estado = 1
      self.atual = self.proximoChar()
    elif(self.atual == '.'):
      self.buffer.append(self.atual)
      self.estado = 3
      self.atual = self.proximoChar()
    elif (self.apenasAlpha(self.atual) or self.espaco(self.atual) or self.apenasSimbolo(self.atual)):
      self.estado = 2
    else : 
      print(f'\n Erro:  estado 1 - char {self.atual}\n')
      self.erro = True
      sys.exit()
      

  def estado2(self): 
    termo = ''.join(self.buffer)
    self.token =  Token(termo=termo, tipo='INTEGER')
    self.table.append(['num_integer', termo])
    self.buffer = []

    self.estado = 0



  def estado3(self):
    if(self.digito(self.atual)):
      self.estado = 4
      self.atual = self.proximoChar()
    else : 
      print(f'\n Erro:  estado 3 - char {self.atual}\n')
      self.erro = True
      sys.exit()

    
  def estado4(self):
    if(self.digito(self.atual)):
      self.estado = 4
      self.atual = self.proximoChar()
    elif (self.alpha(self.atual) or self.espaco(self.atual) or self.simbolo(self.atual)):
      self.estado = 5
      
    else : 
      print(f'\n Erro:  estado 4 - char {self.atual}\n')
      self.erro = True
      sys.exit()


  def estado5(self):
    termo = ''.join(self.buffer)
    self.token = Token(termo=termo, tipo='REAL')
    self.table.append(['num_real', termo])
    self.buffer = []

    self.estado = 0 
    self.atual = self.proximoChar()


  
  def estado6(self):  
    if (self.alpha(self.atual) or self.digito(self.atual)):
      self.estado = 6
      self.atual = self.proximoChar()
    elif(self.espaco(self.atual) or self.atual in ['(',')','+','-','*','/',',',';',':','.','>','<','=']):
      self.estado = 7

    else : 
      print(f'\n Erro:  estado 6 - char {self.atual}\n')
      self.erro = True
      sys.exit()


  def estado7(self):
    termo = ''.join(self.buffer)
    tipo='IDENTIFICADOR'
    if(termo in self.RESERVADAS):
      tipo = 'RESERVADA'
      self.table.append(['reserv', termo])
    else:
       self.table.append(['ident', termo])
    self.token = Token(termo=termo, tipo=tipo)
    
    self.buffer = []
    self.estado = 0 
    

    
  def estado8(self):
    self.estado = 9

  def estado9(self):
    termo = ''.join(self.buffer)
    self.token  = Token(termo=termo, tipo='SYMBOL')
    self.table.append(['symbol', termo])
    self.buffer = []
    self.estado = 0 
    


  def estado10(self):
    if (self.alpha(self.atual) or self.espaco(self.atual) or self.digito(self.atual)):
      self.estado = 9
      self.atual = self.proximoChar()
    elif(self.atual == '='):
      self.buffer.append(self.atual)
      self.estado = 11
      self.atual = self.proximoChar()
    else : 
      print(f'\n Erro: estado 10 - char {self.atual}\n')
      self.erro = True
      sys.exit()


  def estado11(self):
    if (self.alpha(self.atual) or self.espaco(self.atual) or self.simbolo(self.atual)):
      self.estado = 9
      self.atual = self.proximoChar()
    else : 
      print(f'\n Erro: estado 11 - char {self.atual}\n')
      self.erro = True
      sys.exit()


  def estado12(self):
    if (self.alpha(self.atual) or self.espaco(self.atual) or self.digito(self.atual)):
      self.estado = 9
      self.atual = self.proximoChar()
    elif(self.atual in ['=', '>']):
      self.buffer.append(self.atual)
      self.estado = 13
      self.atual = self.proximoChar()
    else : 
      print(f'\n Erro: estado 12 - char {self.atual}\n')
      self.erro = True
      sys.exit()

  def estado13(self): 
    if (self.alpha(self.atual) or self.espaco(self.atual) or self.digito(self.atual)):
      self.estado = 9
      self.atual = self.proximoChar()
    else : 
      print(f'\n Erro: estado 13 - char {self.atual}\n')
      self.erro = True
      sys.exit()



# anLex = AnalisadorLexico()
# anLex.analyse()
# anLex.print_table()

#!/usr/bin/env python
import sys
import re

class JackTokenizer:
    _keywords = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
    _symbol = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
    _integerConstant = "\d{1,5}"
    _stringConstant = "\"\S*\""
    _identifier = "\w+"
    _space = "\n|\t| "
    
    Keyword = 1
    Symbol = 2
    IntegerConstant = 3
    StringConstant = 4
    Identifier = 5
    
    
    def __init__(self, jack_filename):
        """Opens the input file/stream and gets ready to tokenize it."""
        self.jackfile = open(jack_filename, "rU")
        self.currentToken = ""
    
           
    def hasMoreTokens(self):
        """Do we have more tokens in the input?"""
        peekchar = self._peeknextchar()

        if peekchar == "":
            return False
        else:
            return True
        
         
    def advance(self):
        """Gets the next token from the input and makes it the current token."""
        if not self.hasMoreTokens():
            return
        
        self.currentToken = ""
        currentchar = self._getnextchar()            
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            currentchar = self._getnextchar()
            
        while currentchar == "/" and self._peeknextchar() == "/":
            # // comment line
            self._skipwholeline()
            currentchar = self._getnextchar() #get next char after comment line
                    
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            currentchar = self._getnextchar()
        
        while currentchar == "/" and self._peeknextchar() == "*":
            # /* multline comment
            self._getnextchar() # skip * in /*
            while True:
                currentchar = self._getnextchar()
                if currentchar == "*" and self._peeknextchar() == "/":
                    self._getnextchar() #advance past /
                    currentchar = self._getnextchar() 
                    break
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            currentchar = self._getnextchar()
        
        
        while True:          
            if not self.hasMoreTokens():
                return

            self.currentToken += currentchar
            
            if re.match(self._space, self._peeknextchar()) is not None:
                #next char is a space, current is token
                return
                
            if self._peeknextchar() in self._symbol:
                #next char is a symbol, so current is token
                return
            
            if self.currentToken in self._symbol:
                #current char is a symbol, special case, so token
                return
                
            currentchar = self._getnextchar()
                    

    def tokenType(self):
        """Returns the type of the current token."""
        if self.currentToken in self._keywords:
            return self.Keyword
        
        if self.currentToken in self._symbol:
            return self.Symbol
            
        if re.match(self._integerConstant, self.currentToken) is not None:
            return self.IntegerConstant
            
        if re.match(self._stringConstant, self.currentToken) is not None:
            return self.StringConstant
            
        if re.match(self._identifier, self.currentToken) is not None:
            return self.Identifier

            
    def keyWord(self):
        """Returns the keyword which is the current token."""
        if self.tokenType() == JackTokenizer.Keyword:
            return self.currentToken

        
    def symbol(self):
        """Returns the character which is the current token."""
        if self.tokenType() == JackTokenizer.Symbol:
            return self.currentToken

        
    def identifier(self):
        """Returns the identifier which is the current token."""
        if self.tokenType() == JackTokenizer.Identifier:
            return self.currentToken

        
    def intVal(self):
        """Returns the integer value of the current token."""
        if self.tokenType() == JackTokenizer.IntegerConstant:
            return int(self.currentToken)


    def stringVal(self):
        """Returns the string value of the current token, without the double quotes."""
        if self.tokenType() == JackTokenizer.StringConstant:
            return self.currentToken

    
    def printToken(self):
        if self.tokenType() == JackTokenizer.Keyword:
            return "<keyword> %s </keyword>" % self.currentToken
        elif self.tokenType() == JackTokenizer.Symbol:
            return "<symbol> %s </symbol>" % self.currentToken
        elif self.tokenType() == JackTokenizer.Identifier:
            return "<identifier> %s </identifier>" % self.currentToken
        elif self.tokenType() == JackTokenizer.IntegerConstant:
            return "<integerConstant> %d </integerConstant>" % self.currentToken
        elif self.tokenType() == JackTokenizer.StringConstant:
            return "<stringConstant> %s </stringConstant>" % self.currentToken
        else:
            return "Token: %s" % self.currentToken    

        
    def _getnextchar(self):
        return self.jackfile.read(1)


    def _skipwholeline(self):
        self.jackfile.readline()

        
    def _peeknextchar(self):
        next_char = self.jackfile.read(1)
        
        if next_char != "":
            self.jackfile.seek(-1, 1)
            
        return next_char
   
       
def main(argv):
    import os.path
    jackfilename = argv[1]
    
    #getting jack file name
    (jfilename, jextension) = os.path.splitext(jackfilename)
    jtokresultfilename = jfilename + "T.xml" #just to be consistent with the book
    
    jtok = JackTokenizer(jackfilename)
    
    with open(jtokresultfilename, "w") as jtokresult:
        jtokresult.write("<tokens>")
        jtok.advance()
        while jtok.hasMoreTokens():
            jtokresult.write(jtok.printToken())
            jtok.advance()

        jtokresult.write("</tokens>")

if __name__ == "__main__":
    import sys
    main(sys.argv)

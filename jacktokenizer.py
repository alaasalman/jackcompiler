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
        self.jackfile = open(jack_filename, "rU")
        self.currentToken = ""
           
    def hasMoreTokens(self):
        peekchar = self._peeknextchar()

        if peekchar == "":
            return False
        else:
            return True
        
         
    def advance(self):
    
        if not self.hasMoreTokens():
            return
        
        self.currentToken = ""
        currentchar = self._getnextchar()            
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            #print "skip empty2"
            currentchar = self._getnextchar()
            
        while currentchar == "/" and self._peeknextchar() == "/":
            # // comment line
            #print "line is comment, skipping"
            self._skipwholeline()
            currentchar = self._getnextchar() #get next char after comment line
                    
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            #print "skip empty1"
            currentchar = self._getnextchar()
        
        while currentchar == "/" and self._peeknextchar() == "*":
            # /* multline comment
            #print "line is multi comment, skipping"
            self._getnextchar() # skip * in /*
            while True:
                currentchar = self._getnextchar()
                if currentchar == "*" and self._peeknextchar() == "/":
                    self._getnextchar() #advance past /
                    currentchar = self._getnextchar() 
                    break
        
        #skip spaces and empty lines     
        while re.match(self._space, currentchar) is not None:
            #print "skip empty2"
            currentchar = self._getnextchar()
        
        
        while True:
            
            if not self.hasMoreTokens():
                return

            self.currentToken += currentchar
            #print self.currentToken
            
            if re.match(self._space, self._peeknextchar()) is not None:
                #next char is a space, current is token
                #print "token %s" % self.currentToken
                return
                
            if self._peeknextchar() in self._symbol:
                #next char is a symbol, so current is token
                return
            
            if self.currentToken in self._symbol:
                #current char is a symbol, special case, so token
                return
                
            currentchar = self._getnextchar()
            
        #print self.currentToken
                
            
        
    def tokenType(self):
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
        if self.tokenType() == JackTokenizer.Keyword:
            print "<keyword> %s </keyword>" % self.currentToken
            return self.currentToken
        
    def symbol(self):
        if self.tokenType() == JackTokenizer.Symbol:
            print "<symbol> %s </symbol>" % self.currentToken
            return self.currentToken
        
    def identifier(self):
        if self.tokenType() == JackTokenizer.Identifier:
            print "<identifier> %s </identifier>" % self.currentToken
            return self.currentToken
        
    def intVal(self):
        if self.tokenType() == JackTokenizer.IntegerConstant:
            print "<integerConstant> %d </integerConstant>" % self.currentToken
            return int(self.currentToken)
        
    def stringVal(self):
        if self.tokenType() == JackTokenizer.StringConstant:
            print "<stringConstant> %s </stringConstant>" % self.currentToken
            return self.currentToken
        
    def _getnextchar(self):
        return self.jackfile.read(1)

    def _skipwholeline(self):
        self.jackfile.readline()
        
    def _peeknextchar(self):
        next_char = self.jackfile.read(1)
        
        if next_char != "":
            self.jackfile.seek(-1, 1)
            
        return next_char
        
    def printchar(self, currchar):
        if currchar == "\n":
            print "NewLine"
        elif currchar == " ":
            print "Space"
        elif currchar == "":
            print "EmptySpace"
        elif currchar == "\r":
            print "Return"
        elif currchar == "\r\n":
            print "Cr\lf"
        else:
            print "Looking at %s with length %d" % (currchar, len(currchar))
          
def main(argv):
    jackfilename = argv[1]
    
    jtok = JackTokenizer(jackfilename)
    print "<tokens>"
    while jtok.hasMoreTokens():
        jtok.advance()
        if jtok.tokenType() == JackTokenizer.Keyword:
            jtok.keyWord()
        elif jtok.tokenType() == JackTokenizer.Symbol:
            jtok.symbol()
        elif jtok.tokenType() == JackTokenizer.IntegerConstant:
            jtok.intVal()
        elif jtok.tokenType() == JackTokenizer.StringConstant:
            jtok.stringVal
        elif jtok.tokenType() == JackTokenizer.Identifier:
            jtok.identifier()
    print "</tokens>"          

if __name__ == "__main__":
    import sys
    main(sys.argv)

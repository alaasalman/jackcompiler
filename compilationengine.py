#!/usr/bin/env python

import re
from jacktokenizer import JackTokenizer


class CompilationEngine:
    def __init__(self, infile, outfile):
        self.tokenizer = JackTokenizer(infile)
        self.xmlout = open(outfile, "w")
        
        comParse = self.CompileClass()
        
        if comParse == False:
            print "Invalid parse"
            
        self.xmlout.close()
        
    def CompileClass(self):
        """Compiles a complete class."""
        self._output("<class>")

        self.tokenizer.advance()
        #expect class
        if self.tokenizer.keyWord() != "class":
            return False
        
        self._output(self.tokenizer.printToken())
                            
        self.tokenizer.advance()
        #expect class name
        if not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        #expect {
        if self.tokenizer.symbol() != "{":
            return False
            
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        
        #check if there are any field var declarations
        
        while self.tokenizer.keyWord() in ("static", "field"):
            self.CompileClassVarDec()
       
        while self.tokenizer.keyWord() in ("constructor", "function", "method"):     
            self.CompileSubroutine()

        #expect }
        if self.tokenizer.symbol() != "}":
            return False
        
        self._output(self.tokenizer.printToken())
        
        self._output("</class>")
        
    def CompileClassVarDec(self):
        """Compiles a static declaration or a field declaration."""
        self._output("<classVarDec>")
        if self.tokenizer.keyWord() not in ("static", "field"):
            return False

        self._output(self.tokenizer.printToken())

        self.tokenizer.advance()
        #expect var type
        if not self.tokenizer.identifier() and not self.tokenizer.keyWord() in ("int", "char", "boolean"):
            return False

        self._output(self.tokenizer.printToken())
                    
        self.tokenizer.advance()
        #expect var name
        if not self.tokenizer.identifier():
            return False

        self._output(self.tokenizer.printToken())
                    
        self.tokenizer.advance()

        #check for ,varname
        while self.tokenizer.symbol() == ",":
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            #expect identifier
            if not self.tokenizer.identifier():
                return False
            
            self._output(self.tokenizer.printToken())
            self.tokenizer.advance()
                
        if not self.tokenizer.symbol() == ";":
            return False

        self._output(self.tokenizer.printToken())
                    
        self.tokenizer.advance()
        self._output("</classVarDec>")              
        
    def CompileSubroutine(self):
        """Compiles a complete method, function, or constructor."""
        self._output("<subroutineDec>")
        #expecting class ctor, function or method
        if self.tokenizer.keyWord() not in ("constructor", "function", "method"):
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        
        #expecting func return type
        if not self.tokenizer.identifier() and self.tokenizer.keyWord() not in ("void", "int", "char", "boolean"):
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        #expecting function name
        if not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        #expecting ( symbol
        if self.tokenizer.symbol() != "(":
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        #check for parameter list
        self._output("<parameterList>")
        self.CompileParameterList()
        self._output("</parameterList>")
        
        #expecting ) symbol
        if self.tokenizer.symbol() != ")":
            return False
            
        self._output(self.tokenizer.printToken())
        self._output("<subroutineBody>")
        self.tokenizer.advance()
        if self.tokenizer.symbol() != "{":
            return False
            
        self._output(self.tokenizer.printToken())
        
        #checking for var declarations
        self.tokenizer.advance()
        while self.tokenizer.keyWord() == "var":
            self.CompileVarDec()

        #check for statements
        while self.tokenizer.keyWord() in ("let", "if", "while", "do", "return"):
            self.CompileStatements() 
        
        #expecting } to end subroutine
        if self.tokenizer.symbol() != "}":
            return False
            
        self._output(self.tokenizer.printToken())
        self.tokenizer.advance()
        self._output("</subroutineBody>")
        self._output("</subroutineDec>")
        
    def CompileParameterList(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing '()'."""

        if self.tokenizer.keyWord() not in ("void", "int", "char", "boolean") and not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        #expecting var name
        if not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self._output(self.tokenizer.printToken())

            self.tokenizer.advance()
            #expect var type
            if self.tokenizer.keyWord() not in ("int", "char", "boolean") and not self.tokenizer.identifier():
                return False

            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            #expect var name
            if not self.tokenizer.identifier():
                return False

            self._output(self.tokenizer.printToken())
                            
            self.tokenizer.advance()
        
    def CompileVarDec(self):
        """Compiles a var declaration."""
        self._output("<varDec>")
        #expecting var keyword
        if self.tokenizer.keyWord() != "var":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expect var type
        if self.tokenizer.keyWord() not in ("int", "char", "boolean") and not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expect var name
        if self.tokenizer.tokenType() != JackTokenizer.Identifier:
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            #expect var name
            if not self.tokenizer.identifier():
                return False
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            
        #expect ;
        if self.tokenizer.symbol() != ";":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self._output("</varDec>")
        
    def CompileStatements(self):
        """Compiles a sequence of statements, not including the enclosing '{}'."""
        self._output("<statements>")
        while self.tokenizer.keyWord() in ("let", "if", "while", "do", "return"):
            if self.tokenizer.keyWord() == "let":
                self.CompileLet()
            elif self.tokenizer.keyWord() == "if":
                self.CompileIf()
            elif self.tokenizer.keyWord() == "while":
                self.CompileWhile()
            elif self.tokenizer.keyWord() == "do":
                self.CompileDo()
            elif self.tokenizer.keyWord() == "return":
                self.CompileReturn()
                #TODO is this right?
                break

        self._output("</statements>")

    def CompileDo(self):
        """Compiles a do statement."""
        self._output("<doStatement>")
        if self.tokenizer.keyWord() != "do":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expecting subroutine call
        self.CompileSubroutineCall()

        #expecting ;
        if self.tokenizer.symbol() != ";":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self._output("</doStatement>")
                
    def CompileLet(self):
        """Compiles a let statement."""
        self._output("<letStatement>")
        if self.tokenizer.keyWord() != "let":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expect identifier
        if not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        
        if self.tokenizer.symbol() == "[":
            #array access
            self._output(self.tokenizer.printToken())
            self.tokenizer.advance()
            #expect expresson
            self.CompileExpression()
            
            #expect closing ]
            if self.tokenizer.symbol() != "]":
                return False
            
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()        
        
        if self.tokenizer.symbol() != "=":
            #expect = 
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expecting expression
        self.CompileExpression()

        if self.tokenizer.symbol() != ";":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self._output("</letStatement>")
            
    def CompileWhile(self):
        """Compiles a while statement."""
        self._output("<whileStatement>")
        if self.tokenizer.keyWord() != "while":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expext (
        if self.tokenizer.symbol() != "(":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self.CompileExpression()
        
        #expext )
        if self.tokenizer.symbol() != ")":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        #expext {
        if self.tokenizer.symbol() != "{":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self.CompileStatements()
        
        #expect }
        if self.tokenizer.symbol() != "}":
            return False
        
        self._output(self.tokenizer.printToken())
                
        self.tokenizer.advance()
        self._output("</whileStatement>")

    def CompileReturn(self):
        """Compiles a return statement."""
        self._output("<returnStatement>")
        if self.tokenizer.keyWord() != "return":
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()

        if self.tokenizer.symbol() != ";":
            #expecting expression
            self.CompileExpression()
        
        if self.tokenizer.symbol() != ";":
            #expecting ;
            return False
        
        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        self._output("</returnStatement>")
        
    def CompileIf(self):
        """Compiles an if statement, possible with a trailing else clause."""
        self._output("<ifStatement>")
        
        if self.tokenizer.keyWord() != "if":
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        
        #expect (
        if self.tokenizer.symbol() != "(":
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()
        self.CompileExpression()
        
        #expect )
        if self.tokenizer.symbol() != ")":
            return False

        self._output(self.tokenizer.printToken())
                        
        self.tokenizer.advance()
        #expect {
        if self.tokenizer.symbol() != "{":
            return False

        self._output(self.tokenizer.printToken())

        self.tokenizer.advance()
        
        self.CompileStatements()
        
        #expect }
        if self.tokenizer.symbol() != "}":
            return False

        self._output(self.tokenizer.printToken())
            
        self.tokenizer.advance()
        
        if self.tokenizer.keyWord() == "else":
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            self.CompileStatements()
            
            if self.tokenizer.symbol() != "}":
                return False

            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            
        self._output("</ifStatement>")
        
    def CompileExpression(self):
        """Compiles an expression."""
        self._output("<expression>")
        self.CompileTerm()
        
        #(op term)*
        while self.tokenizer.symbol() in ("+", "-", "*", "/", "&", "|", "<", ">", "="):
            self._output(self.tokenizer.printToken())
            self.tokenizer.advance()
            self.CompileTerm()

        self._output("</expression>")
        
    def CompileTerm(self):
        """Compiles a term."""
        self._output("<term>")
        thisisterm = False
        
        if self.tokenizer.intVal(): #integer constant
            thisisterm = True
            self._output(self.tokenizer.printToken())
            
        elif self.tokenizer.stringVal(): #string constant
            thisisterm = True
            self._output(self.tokenizer.printToken())
            
        elif self.tokenizer.keyWord(): #keyword constant
            keyterm = self.tokenizer.keyWord()

            #can only be true, false, null, this
            if keyterm not in ("true", "false", "null", "this"):
                return False
                
            thisisterm = True
            self._output(self.tokenizer.printToken())
                        
        elif self.tokenizer.symbol() == "(":
            #check for (expression)
            self._output(self.tokenizer.printToken())

            self.tokenizer.advance()
            self.CompileExpression()

            if self.tokenizer.symbol() != ")":
                return False

            thisisterm = True                
            self._output(self.tokenizer.printToken())

        elif self.tokenizer.symbol() in ("-", "~"):
            #expect term
            self._output(self.tokenizer.printToken())
            self.tokenizer.advance()

            self.CompileTerm()
            
        elif self.tokenizer.identifier(): #variable name
            #lookahead checking for array access signs or subroutine calls sign
            self._output(self.tokenizer.printToken())
            self.tokenizer.advance()

            if self.tokenizer.symbol() == "[":
                #array access
                self._output(self.tokenizer.printToken())
                self.tokenizer.advance()
                self.CompileExpression()
                
                if self.tokenizer.symbol() != "]":
                    return False

                thisisterm = True
                self._output(self.tokenizer.printToken())
                
            elif self.tokenizer.symbol() == "(":
                #direct subroutine call
                self._output(self.tokenizer.printToken())

                self.tokenizer.advance()
                self.CompileExpressionList()
                self.tokenizer.advance()

                #expect ending )
                if self.tokenizer.symbol() != ")":
                    return False

                thisisterm = True
                self._output(self.tokenizer.printToken())
                
            elif self.tokenizer.symbol() == ".":
                #var subroutine call
                self._output(self.tokenizer.printToken())
                
                self.tokenizer.advance()
                #expecting identifier
                if not self.tokenizer.identifier():
                    return False
                
                self._output(self.tokenizer.printToken())
                    
                self.tokenizer.advance()
                #expecting (
                if self.tokenizer.symbol() != "(":
                    return False

                self._output(self.tokenizer.printToken())
                self.tokenizer.advance()
                
                self.CompileExpressionList()

                #expecting closing )
                if self.tokenizer.symbol() != ")":
                    return False

                thisisterm = True
                self._output(self.tokenizer.printToken())
                
        if thisisterm == True:
            self.tokenizer.advance()
            
        self._output("</term>")
        
    def CompileExpressionList(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._output("<expressionList>")
        #expression?
        self.CompileExpression()
        
        #(, expression)*
        while self.tokenizer.symbol() == ",":
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            self.CompileExpression()
            
        self._output("</expressionList>")
        
    def CompileSubroutineCall(self):
        """Compile a subroutine call."""
        if not self.tokenizer.identifier():
            return False
        
        self._output(self.tokenizer.printToken())
        
        self.tokenizer.advance()

        if self.tokenizer.symbol() == "(":
            #direct func call

            self._output(self.tokenizer.printToken())

            self.tokenizer.advance()
            self.CompileExpressionList()

            #expect ending )
            if self.tokenizer.symbol() != ")":
                return False

            self._output(self.tokenizer.printToken())

        elif self.tokenizer.symbol() == ".":
            #method call

            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            #expecting identifier for method name
            if not self.tokenizer.identifier():
                return False
            
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            #expecting (
            if self.tokenizer.symbol() != "(":
                return False
            
            self._output(self.tokenizer.printToken())
            
            self.tokenizer.advance()
            self.CompileExpressionList()
            
            if self.tokenizer.symbol() != ")":
                return False 
            self._output(self.tokenizer.printToken())
        else:
            return False
        
        self.tokenizer.advance()
        
    def _output(self, strtowrite):
        """Write string to xml output file."""
        self.xmlout.write(strtowrite)

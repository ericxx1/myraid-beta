from rply import ParserGenerator, LexerGenerator, ParsingError
from myraid import lexer
from myraid import compiler
from myraid.BaseBox import Boxes
from myraid.memory import memory
from myraid.memory.memory import Collector
from myraid.functions import myraid_socket
from myraid.functions import myraid_print
from myraid.memory.memory import stack
import os
from rpython.rlib import rstring
import socket
class Parser():
	pg = ParserGenerator(["NUMBER", "STRING", 'MULTIPLY', "PLUS", "MINUS", "DIVIDE", "NEW", "SOCKET", "OPEN_PAREN",
	                      "CLOSED_PAREN", "COLON", "COMMA", "CONNECT", "SEND", "OBJECT", "IF", "ELSEIF", "ELSE", "QUOTE",
	                      "CONDITIONAL", "EQUAL", "NAME", "ATOM", "COMMENT", "END", "GREATER_THAN_OR_EQUAL_TO", 
	                      "LESS_THAN_OR_EQUAL_TO", "IN", "PERIOD"],
	        precedence=[("left", ['PLUS', 'MINUS']), ("left", ['MULTIPLY', 'DIVIDE'])], cache_id="myparser")
	
	
	#Define a production for comments @pg.production("comment: DIVIDE DIVIDE (.*) DIVIDE DIVIDE") or just remove anything that starts with // and ends with //
	#In the _parse function
	@pg.production("main : string")
	@pg.production("main : expr")
	@pg.production("main : variable")
	def main(p):
	    # p is a list, of each of the pieces on the right hand side of the
	    # grammar rule
	    return p[0]
	    
	@pg.production("variable : ATOM")
	def var_op(p):
		return p[0];
	    
	@pg.production("variable : ATOM  ATOM  EQUAL  NUMBER")    
	@pg.production("variable : ATOM  ATOM  EQUAL  ATOM")
	@pg.production("variable : ATOM  ATOM  EQUAL  STRING")
	def var(p):
		if(p[0].getstr() == ("var" or "Var")):
			var_name = p[1].getstr()
			if p[3].gettokentype() == "STRING":
				value = p[3].getstr().strip('"')
			elif p[3].gettokentype() == "NUMBER":
				value = p[3].getstr().strip('"')			
			elif p[3].gettokentype() == "ATOM":
				print "Var name: " + var_name
				value = memory.Memory.Select(p[3].getstr())
			else:
				value = p[3].getstr()
			op = "VAR(" + var_name + "," + value + ")"
			memory.Memory_Stack.Add(op)	
			return None;
	
	@pg.production("string : STRING")
	def string_op(s):
		return Boxes.BoxStr(s[0])
	
	@pg.production("expr : NUMBER")
	def expr_num(p):
	    return Boxes.BoxInt(int(p[0].getstr()))
	
	@pg.production("expr : expr DIVIDE expr")    
	@pg.production("expr : expr MULTIPLY expr")
	@pg.production("expr : expr PLUS expr")
	@pg.production("expr : expr MINUS expr")
	@pg.production("expr : expr CONDITIONAL expr")
	def expr_op(p):
	    lhs = p[0].getint()
	    rhs = p[2].getint()
	    if p[1].gettokentype() == "PLUS":
	        return Boxes.BoxInt(lhs + rhs)
	    elif p[1].gettokentype() == "MINUS":
	        return Boxes.BoxInt(lhs - rhs)
	    elif p[1].gettokentype() == "MULTIPLY":
	        return Boxes.BoxInt(lhs * rhs)
	    elif p[1].gettokentype() == "DIVIDE":
	        return Boxes.BoxInt(lhs / rhs)
	    elif p[1].gettokentype() == "CONDITIONAL":
	        op = p[1].getstr()
	        if op == ">":
				if (lhs > rhs):
					print "true";
				else:
					print "false"
	        return None                       
	    else:
	        raise AssertionError("A problem occured parsing the script.")
	            
	@pg.production("string : NEW SOCKET OPEN_PAREN string CLOSED_PAREN COLON")  
	def socket_op(p):
		name = p[3]
		assert isinstance(name, Boxes.BoxStr);
		name = Boxes.BoxStr.get_str(name)
		name = name.getstr().strip('"')
		print name
		op = "CREATE_SOCKET(" + name + ")"
		memory.Memory_Stack.Add(op);
		return Boxes.BoxStr(p[3])
	
	#Operations
	@pg.production("string : OBJECT CONNECT OPEN_PAREN string COMMA NUMBER CLOSED_PAREN")
	def socket_connect_op(p):
		name = p[0].getstr().strip('.')
		print name #<----Strip name of '"' and "."
		host = p[3]
		assert isinstance(host, Boxes.BoxStr);
		host = Boxes.BoxStr.get_str(host)
		host = host.getstr().strip('"')
		print host
		port = p[5].getstr()
		print port
		op = "SOCKET_CONNECT(" + name + "," + host + "," + port + ")"
		memory.Memory_Stack.Add(op);
		return None
		
	@pg.production("object : OBJECT")
	def object(p):	
		return Boxes.BoxStr(p[0])
	
	@pg.production("string : OBJECT SEND OPEN_PAREN string CLOSED_PAREN") #Change SEND to ATOM eventually
	def socket_send_op(p):
		name = p[0].getstr().strip(".")
		#assert isinstance(name, Boxes.BoxStr);
		#name = Boxes.BoxStr.get_str(name)
		#name = name.getstr().strip(".")
		if(p[1].getstr() == "send"):
			to_send = p[3] #Fix this. Key error for some reason
			assert isinstance(to_send, Boxes.BoxStr);
			to_send = Boxes.BoxStr.get_str(to_send)
			to_send = to_send.getstr().strip('"')
			op = "SOCKET_SEND(" + name + "," + '"' + to_send + '"' + ")"
			memory.Memory_Stack.Add(op);
		return None
	
	@pg.production("string : OBJECT ATOM OPEN_PAREN NUMBER CLOSED_PAREN")	#Fix not being able to name a socket "Socket/socket. Change the New Socket (SOCKET) token to just a ATOM and identify it as a "socket""
	def socket_recv_op(p):
		name = p[0].getstr().strip(".")
		bytes_per_chunk = p[3].getstr()	
		op = "SOCKET_RECV(" + name + "," + bytes_per_chunk + ")"
		memory.Memory_Stack.Add(op);
		return None;
	
	@pg.production("string : ELSEIF OPEN_PAREN NUMBER CONDITIONAL NUMBER CLOSED_PAREN")
	@pg.production("string : ELSEIF OPEN_PAREN ATOM CONDITIONAL ATOM CLOSED_PAREN")
	@pg.production("string : ELSEIF OPEN_PAREN ATOM CONDITIONAL NUMBER CLOSED_PAREN") #Work on this
	@pg.production("string : ELSEIF OPEN_PAREN NUMBER CONDITIONAL ATOM CLOSED_PAREN") #Work on this
	@pg.production("string : IF OPEN_PAREN NUMBER CONDITIONAL NUMBER CLOSED_PAREN")
	@pg.production("string : IF OPEN_PAREN ATOM CONDITIONAL ATOM CLOSED_PAREN")
	@pg.production("string : IF OPEN_PAREN ATOM CONDITIONAL NUMBER CLOSED_PAREN") #Work on this
	@pg.production("string : IF OPEN_PAREN NUMBER CONDITIONAL ATOM CLOSED_PAREN") #Work on this
	#Add if( x in y ) or just x in y: without if. Add support for strings. String in x etc.
	def if_op(p):
		x = p[2];
		y = p[3];
		z = p[4];
		x_ = None;
		y_ = None;
		z_ = None;
		op = None;
		x_isvar = None;
		if(x.gettokentype() == "ATOM" and z.gettokentype() == "ATOM"):
			x_ = memory.Memory.Select(x.getstr())
			y_ = str(p[3].getstr())
			z_ = memory.Memory.Select(z.getstr())
		if(x.gettokentype() == "ATOM" and z.gettokentype() == "NUMBER"):
			x_ = memory.Memory.Select(x.getstr())
			y_ = str(y.getstr())
			z_ = str(z.getstr())
		if(x.gettokentype() == "NUMBER" and z.gettokentype() == "ATOM"):
			x_ = str(x.getstr())
			y_ = str(y.getstr())
			z_ = memory.Memory.Select(z.getstr())	
		if(x.gettokentype() == "NUMBER" and z.gettokentype() == "NUMBER"): #Vars are broken for some reason. var x = and int x = ;
			x_ = str(x.getstr())
			y_ = str(y.getstr())
			z_ = str(z.getstr())
		if(p[0].gettokentype() == "IF"):
			op = "IF(" + str(x_) + str(y_) + str(z_) + ")";
		elif(p[0].gettokentype() == "ELSEIF"):
			op = "ELSEIF(" + str(x_) + str(y_) + str(z_) + ")";
		memory.Memory_Stack.Add(op);
		return None;
	@pg.production("string : ELSE")
	def else_op(p):
		memory.Memory_Stack.Add("ELSE");
		return None;
		
	@pg.production("string : END")
	def end_op(p):
		memory.Memory_Stack.Add("END")
		return None;
	@pg.production("string : ATOM OPEN_PAREN CLOSED_PAREN")
	def function_op(p):
		if(p[0].getstr() == "dstack"):
			i = 0;
			for value in stack:
				i+=1;
				print stack[i];
		return None;		
	@pg.production("string : OBJECT ATOM OPEN_PAREN string CLOSED_PAREN")
	def _os_exec(p):
		if(p[0].getstr() == "_os." and p[1].getstr() == "exec"):
			x = p[3];
			assert isinstance(x, Boxes.BoxStr);
			cm = Boxes.BoxStr.get_str(x)
			cm = cm.getstr().strip('"')
			op = "OS(" + '"' + cm + '"' + ")"
			memory.Memory_Stack.Add(op);
			return None;
	@pg.production("string : ATOM ATOM")
	def load_module_op(p):
		if(p[0].getstr() == "load"):
			op = "load(" + p[1].getstr() + ")"
			memory.Memory_Stack.Add(op)
			x = 0; #Not Implemented
		return None;
	parser = pg.build()
	def _parse(line):
		for token in lexer.lexer.lex(line):
			if token.gettokentype() == "COMMENT":
				line = rstring.replace(line, token.getstr(), "", 1)
			if token.gettokentype() in lexer.keywords or lexer.operations:
				pass
			else:
				print "Invalid token", token, token.gettokentype()
				os._exit(1)		#if token is in keywords: continue; else: print "Invalid token found"; os_exit(1);
			print("TOKEN:('"+token.gettokentype()+"','"+token.getstr()+"')")
		result = Parser.parser.parse(lexer.lexer.lex(line));
	

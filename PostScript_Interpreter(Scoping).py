##########################################
#  Freya Varez                           #
#  Assignment 5                          #
#  4/15/2019                             #
#  Static Post-Script Interpereter (SSPS)#
##########################################
import re

opstack = [] #operand stack
dictstack = [] #dictionary stack
scope = 'dynamic' #scoping variable (defaults to dynamic)

#------------------------- 10%: Operand Methods-----------------------------
def opPop(): # opPop should return the popped value
    if len(opstack) > 0:
        return opstack.pop()
    else:
        return None
    
def opPush(value):
    opstack.append(value)

#-------------------------- 20% Dictionary Methods--------------------------
def dictPop(): # dictPop pops the top dictionary from the dictionary stack.
    if len(dictstack) > 0:
        return dictstack.pop()
    else:
        return None

def dictPush(d, frame): #dictPush pushes the dictionary ‘d’ to the dictstack.
    dictstack.append((frame, d))
   
def define(name, value): #add name:value pair to the top dictionary in the dictionary stack.
    if len(dictstack) > 0:
        dictstack[-1][1][name] = value #define new dict element
    #else:
        #newDict = {}
        #newDict[name] = value
        #dictstack.append((0,newDict))

def psDef():
    value = opPop()
    name = opPop()
    define(name, value)
    
def lookupStatic(key, startIndex):          #Helper function, allows static search through dictstack
    activationIndex = startIndex
    if dictstack == []:
        return (activationIndex, None)
    def getNext(tup):           #given current tuple, find next tuple
        return dictstack[tup[0]]
    if key in dictstack[startIndex][1]:     #check last index
        return (activationIndex, dictstack[startIndex][1][key])
    index = getNext(dictstack[startIndex])  #get next tuple
    activationIndex = dictstack[startIndex][0]
    n = 0;
    while not(key in index[1]):  #search dictionary at current tuple, if key found - exit and return value
        activationIndex = index[0]
        index = getNext(index)   #"increment" tuple
        if index == dictstack[startIndex] or n > len(dictstack):       #If loop found return None
            return (activationIndex, None)
        n+=1
    return (activationIndex, index[1][key])        #if key found, return respective value

def lookup(name, frame): # return the value associated with name
    if scope == 'Dynamic' or scope == 'dynamic':
        for tup in reversed(dictstack):
            curDict = tup[1]
            if curDict.get('/' + name, None) != None:
                return (0, curDict.get('/' + name, None))
        print("Error: " + str(name) + " undefined")
        return None
    elif scope == 'Static' or scope == 'static':
        return lookupStatic('/' + name, frame)
    else:
        print("Error: Invalid scoping argument")
        return None
        
#--------------------------- 10% -------------------------------------
def add():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 + op1)
    else:
        print("Error: Missing operand(s)")

def sub():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 - op1)
    else:
        print("Error: Missing operand(s)")
        
def mul():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 * op1)
    else:
        print("Error: Missing operand(s)")

def div():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 / op1)
    else:
        print("Error: Missing operand(s)")

def mod():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 % op1)
    else:
        print("Error: Missing operand(s)")

def eq():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 == op1)
    else:
        print("Error: Missing operand(s)")
        
def lt():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 < op1)
    else:
        print("Error: Missing operand(s)")
        
def gt():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op2 > op1)
    else:
        print("Error: Missing operand(s)")

#--------------------------- 15% -------------------------------------
def length():
    if len(opstack) > 0:
        L = opPop()
        if(isinstance(L, str)): #checks for valid type
            opPush(len(L) - 2)
        else:
            print("Error: operand is not of type list")
    else:
        print("Error: Stack is empty")

def get():
    if len(opstack) > 1:
        index = opPop()
        S = opPop()
        if isinstance(S, str) and isinstance(index, int): #checks valid type(s)
            try:
                opPush(ord(S[index + 1]))
            except:
                print("Error: index is out of range")
        else:
            print("Error: Invalid types")
    else:
        print("Error: Stack is empty")

def getinterval():
    if len(opstack) > 1:
        length = opPop()
        start = opPop()
        S = opPop()
        if isinstance(S, str) and isinstance(start, int) and isinstance(length, int): #checks valid type(s)
            try:
                opPush("(" + S[(start + 1):(start + length + 1)] + ")")
            except:
                print("Error: interval out of range")
        else:
            print("Error: Invalid types")
    else:
        print("Error: Stack is empty")

def put():
    if len(opstack) > 2:
        char = opPop()
        index = opPop()
        string = opPop()
        if isinstance(string, str) and isinstance(index, int) and isinstance(char, int):
            ###################################################Helper function swaps old<->new values in opstack and dictstack
            def swap(old, new):
                for curDict in dictstack:
                    for key, value in curDict.items():
                        if id(value) == id(old):
                            curDict[key] = new
                for i in range(len(opstack)):
                    if id(opstack[i]) == id(old):
                        opstack[i] = new
            ##################################################
            newStr = string[:index + 1] + chr(char) + string[(index + 2):]
            swap(string, newStr)
            opPush(newStr)
        else:
            print("Error: Incorrect argument types")
    else:
        print("Error: Not enough arguments")
        
#--------------------------- 25% -------------------------------------
def dup():# duplicates and pushes top of opstack
    if len(opstack) > 0:
        temp = opPop()
        opPush(temp)
        opPush(temp)
    else:
        print("Error: Stack is empty")

def copy():
    if len(opstack) > 0:
        L = []
        end = opPop()
        for i in range(0, end):
            L.append(opPop())
        for i in reversed(L):
            opPush(i)
        for i in reversed(L):
            opPush(i)
    else:
        print("Error: Stack is empty") 

def pop():
    return opPop()

def clear():
    del opstack[:]
    del dictstack[:]

def exch():
    if(len(opstack) > 1):
        temp1 = opPop()
        temp2 = opPop()
        opPush(temp1)
        opPush(temp2)
    else:
        print("Error: Not enough arguments")

def roll():
    j = opPop()
    i = opPop()
    L = []
    for element in range(i):
        L.append(opPop())
    L.reverse()
    for roll in range(i):
        opPush(L[(roll-j)%i])
        
def stack():
    print(scope)
    print("====================  opstack")
    for i in reversed(opstack):
        print(i)
    print("====================  dictstack")
    m = len(dictstack) - 1
    for tup in reversed(dictstack):
        n, dictionary = tup
        print('----', m, '----', n, '----')
        for key, value in dictionary.items():
            print(key," ", value)
        m -= 1
    print("====================")
    
########################################_________________Part2________________#######################################################
def psIf(frame):
    if len(opstack) > 1:
        function = opPop()
        condition = opPop()
        if isinstance(condition, bool):
            if condition == True:
                interpretSPS(function, frame)
        else:
            print("Error: Incorrect operands type")
    else:
        print("Error: Missing operands")
        
def psIfElse(frame):
    if len(opstack) > 2:
        elseStatement = opPop()
        ifStatement = opPop()
        condition = opPop()
        if isinstance(condition, bool):
            if(condition == True):
                interpretSPS(ifStatement, frame)
            else:
                interpretSPS(elseStatement, frame)
        else:
            print("Error: Incorrect operands type")
    else:
        print("Error: Missing operands")


def psFor(frame):
    if len(opstack) > 3:
        function = opPop()
        end = opPop()
        increment = opPop()
        start = opPop()

        if start == end:
            opPush(start)
            interpretSPS(function)
        elif start < end:
            while start <= end:
                opPush(start)
                interpretSPS(function, frame)
                start += increment
        else:
            while start >= end:
                opPush(start)
                interpretSPS(function, frame)
                start += increment
        return

##################################################
def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

def groupMatching(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            res.append(groupMatching(it))
        else:
            try:
                res.append(int(c))
            except:
                if c == 'true':
                    res.append(True)
                elif c == 'false':
                    res.append(False)
                else:
                    res.append(c)
    return False

def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':
            return False
        elif c=='{':
            res.append(groupMatching(it))
        else:
            try:
                res.append(int(c))
            except:
                if c == 'true':
                    res.append(True)
                elif c == 'false':
                    res.append(False)
                else:
                    res.append(c)
    return res
    
psFunctions = {'def' : psDef, 'add' : add, 'sub' : sub, 'mul' : mul,
               'div' : div, 'mod' : mod, 'eq' : eq, 'lt' : lt, 'gt' : gt, 'length' : length,
               'get' : get, 'getinterval' : getinterval, 'put' : put, 'dup' : dup, 'copy' : copy,
               'pop' : pop, 'clear' : clear, 'exch' : exch, 'roll' : roll, 'stack' : stack}
psConditionals = {'if':psIf, 'ifelse':psIfElse, 'for':psFor}

def interpretSPS(code, frame): # code is a code array
    for item in code:
        if isinstance(item, str):
            if(item[0] == '/') or (item[0] == '('):
                opPush(item)
            elif psFunctions.get(item, False):
                psFunctions.get(item)()
            elif psConditionals.get(item, False):
                psConditionals.get(item)(frame)
            else:
                frame, var = lookup(item, frame)
                if var != None:
                    if isinstance(var, list): #code array
                        dictPush({}, frame)
                        interpretSPS(var, len(dictstack) - 1)
                        dictPop()
                    else:
                        opPush(var)
        elif isinstance(item, int) or isinstance(item, bool) or isinstance(item, list):
            opPush(item)
        else:
            print("Error: ", item, " is undefined") 

def interpreter(s, setScope): # s is a string
    global scope
    scope = setScope
    dictPush({}, 0) #prepare dictstack with empty dictionary
    interpretSPS(parse(tokenize(s)), 0)
    
def menu():
    while True:
        string = input("ps> ")
        interpreter(string, scope)

#clear opstack and dictstack
def clear():
    del opstack[:]
    del dictstack[:]
    global activationIndex
    activationIndex = 0

#######################################________________Test Inputs___________########################################################
input1 = "/x 4 def /g { x stack } def /f { /x 7 def g } def f "
input2 = "/m 50 def /n 100 def /egg1 {/m 25 def n} def /chic { /n 1 def /egg2 { n } def m n egg1 egg2 stack } def n chic"
input3 = "/x 10 def /A { x } def /C { /x 40 def A stack } def /B { /x 30 def /A { x } def C } def B"
input4 = "/out true def /xand { true eq {pop false} {true eq { false } { true } ifelse} ifelse  dup /x exch def stack} def /myput { out dup /x exch def xand } def /f { /out false def  myput } def false f"
input5 = "/x 10 def /A { x } def /B { /x 30 def /A { x stack } def /C { /x 40 def A } def C } def B"
#######################################________________MAIN PROGRAM__________########################################################


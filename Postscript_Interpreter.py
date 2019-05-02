#######################################
#  Freya Varez                        #
#  3/20/2019                          #
#  Post-Script Interpereter Part 1    #
#######################################

opstack = [] #operand stack
dictstack = [] #dictionary stack

#------------------------- 10%: Operand Methods-----------------------------
def opPop(): # opPop should return the popped value
    if len(opstack) > 0:
        return opstack.pop()
    else:
        return None
    
def opPush(value):
    opstack.append(value)

def opstack_test(): # tests opPop and opPush
    print("opStack test")
    opPush(2)
    opPush(3)
    opPush(False)
    test1 = opPop() == False
    test2 = opPop() == 3
    test3 = opPop() == 2
    test4 = opPop() == None
    print("Test1: " + str(test1))
    print("Test2: " + str(test2))
    print("Test3: " + str(test3))
    print("Test4: " + str(test4))

#-------------------------- 20% Dictionary Methods--------------------------
def dictPop(): # dictPop pops the top dictionary from the dictionary stack.
    if len(dictstack) > 0:
        return dictstack.pop()
    else:
        return None

def dictPush(d): #dictPush pushes the dictionary ‘d’ to the dictstack.
    dictstack.append(d)
   
def define(name, value): #add name:value pair to the top dictionary in the dictionary stack.
    if len(dictstack) > 0:
        dictstack[-1][name] = value #define new dict element
    else:
        newDict = {}
        newDict[name] = value
        dictstack.append(newDict)

def psDef():
    value = opPop()
    name = opPop()
    define(name, value)

def psDict():
    opPop()
    dictPush({})

def lookup(name): # return the value associated with name
    for curDict in reversed(dictstack):
        if curDict.get('/' + name, None) != None:
            return curDict.get('/' + name, None)
    print("Error: " + str(name) + " undefined")
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
        if(isinstance(L, list)): #checks for valid type
            opPush(len(L))
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
                opPush(ord(S[index]))
            except:
                print("Error: index is out of range")
        else:
            print("Error: Invalid types")
    else:
        print("Error: Stack is empty")

def getinterval():
    if len(opstack) > 1:
        end = opPop()
        start = opPop()
        S = opPop()
        if isinstance(S, str) and isinstance(start, int) and isinstance(end, int): #checks valid type(s)
            try:
                opPush(S[start:(end + 1)])
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
        if isinstance(string, str) and isinstance(index, int) and isinstance(char, int): #checks valid type(s)
            opPush(string[:index] + chr(char) + string[(index + 1):])
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
    opstack[:] = []

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
        opPush(L[(roll+j)%i])
        
def stack():
    for element in reversed(opstack):
        print(element)

def dict():
    opPop()
    dictPush({})

def begin():
    dictPush(opPop())

def end():
    dictPop()
    
#######################################________________TESTING FUNCTIONS_______________###############################################
#_________________ARITHMETIC TESTING__________________#

def testAdd():
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3:
        return False
    return True

def testSub():
    opPush(1)
    opPush(2)
    sub()
    if opPop() != -1:
        return False
    return True

def testMul():
    opPush(3)
    opPush(2)
    mul()
    if opPop() != 6:
        return False
    return True

def testDiv():
    opPush(6)
    opPush(2)
    div()
    if opPop() != 3:
        return False
    return True

def testMod():
    opPush(7)
    opPush(2)
    mod()
    if opPop() != 1:
        return False
    return True

def testEq():
    opPush(1)
    opPush(2)
    eq()
    if opPop() != False:
        return False
    return True

def testGt():
    opPush(1)
    opPush(2)
    gt()
    if opPop() != False:
        return False
    return True

def testLt():
    opPush(1)
    opPush(2)
    lt()
    if opPop() != True:
        return False
    return True
#_________________DICTIONARY STACK OPERATOR TESTING_______________#
                 
def testDefine():
    opPush("/this")
    opPush("that")
    psDef()
    if lookup("this") != "that":
        return False
    return True
    
def testLookup():
    opPush("/n1")
    opPush(3)
    psDef()
    if lookup("n1") != 3:
        return False
    return True

def testLength():
    opPush([1,2,3,4,5,6])
    length()
    if opPop() != 6:
        return False
    return True
    
def testGet():
    opPush("Hello")
    opPush(3)
    get()
    if opPop() != ord('l'):
        return False
    return True

def testPut():
    opPush("Hello!")
    opPush(2)
    opPush(ord('N'))
    put()
    if opPop() != 'HeNlo!':
        return False
    return True

def testGetinterval():
    opPush("Hello world!")
    opPush(6)
    opPush(10)
    getinterval()
    if opPop() != 'world':
        return False
    return True

def testDup():
    opPush(1)
    dup()
    if opstack != [1,1]:
        return False
    return True

def testpsDef():
    opPush('/var1')
    opPush(3)
    psDef()
    if lookup('var1') != 3:
        return False
    return True

def testpsDef2():
    opPush('/var2')
    opPush("Hello")
    psDef()
    if lookup('var2') != 'Hello':
        return False
    return True

def testExch():
    opPush(10)
    opPush("/x")
    exch()
    if opPop()!=10 and opPop()!="/x":
        return False
    return True

def testPop():
    l1 = len(opstack)
    opPush(10)
    pop()
    l2= len(opstack)
    if l1!=l2:
        return False
    return True

def testRoll():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(4)
    opPush(-2)
    roll()
    if opPop()!=3 and opPop()!=2 and opPop()!=5 and opPop()!=4 and opPop()!=1:
        return False
    return True

def testCopy():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(2)
    copy()
    if opPop()!=5 and opPop()!=4 and opPop()!=5 and opPop()!=4 and opPop()!=3 and opPop()!=2:
        return False
    return True

def testClear():
    opPush(10)
    opPush("/x")
    clear()
    if len(opstack)!=0:
        return False
    return True

def testDict():
    opPush(1)
    psDict()
    if opPop() != None or dictPop() != {}:
        return False
    return True

def testBeginEnd():
    opPush("/x")
    opPush(3)
    psDef()
    opPush({})
    begin()
    opPush("/x")
    opPush(4)
    psDef()
    end()
    if lookup("x")!=3:
        return False
    return True
#_______________________OTHER TESTING________________________________#
def arithmetic_test(): #tests various arithmetic 
    opPush(2)
    opPush(3)
    add()
    test1 = opPop() == 5

    opPush(2)
    opPush(3)
    sub()
    test2 = opPop() == -1

    opPush(2)
    opPush(3)
    mul()
    test3 = opPop() == 6

    opPush(4)
    opPush(2)
    div()
    test4 = opPop() == 2

    opPush(7)
    opPush(3)
    mod()
    test5 = opPop() == 1

    opPush(2)
    opPush(3)
    eq()
    test6 = opPop() == False

    opPush(2)
    opPush(3)
    lt()
    test7 = opPop() == True

    opPush(2)
    opPush(3)
    gt()
    test8 = opPop() == False

    print("Test1: " + str(test1))
    print("Test2: " + str(test2))
    print("Test3: " + str(test3))
    print("Test4: " + str(test4))
    print("Test5: " + str(test1))
    print("Test6: " + str(test2))
    print("Test7: " + str(test3))
    print("Test8: " + str(test4))

def dictstack_test(): # tests opPop and opPush
    print("opStack test")
    dictPush({'/this':'that', '/other':'done'})
    test1 = lookup('this') == 'that'
    test2 = lookup('DNE') == None

    define('/other', 5)
    test3 = lookup('other') == 5
    define('/another', 77)
    test4 = lookup('another') == 77

    test5 = dictPop() == {'/another':77}
    test6 = dictPop() == {'/this':'that', '/other':'done'}
    test7 = dictPop() == None
    
    print("Test1: " + str(test1))
    print("Test2: " + str(test2))
    print("Test3: " + str(test3))
    print("Test4: " + str(test4))
    print("Test5: " + str(test1))
    print("Test6: " + str(test2))
    print("Test7: " + str(test3))

#######################################________________MAIN PROGRAM__________########################################################    
def main_part1():
    testCases = [('define',testDefine),('lookup',testLookup),('add', testAdd), ('sub', testSub),('mul', testMul),
                 ('div', testDiv),  ('mod', testMod), ('lt', testLt), ('gt', testGt), ('eq', testEq),
                 ('length', testLength),('get', testGet), ('getinterval', testGetinterval),
                 ('put', testPut), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('roll', testRoll),
                 ('copy', testCopy), ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd),
                 ('psDef', testpsDef), ('psDef2', testpsDef2)]
    
    failedTests = [testName for (testName, testProc) in testCases if not testProc()]
    if failedTests:
        return ('Some tests failed', failedTests)
    else:
        return ('All part-1 tests OK')
    
if __name__ == '__main__':
    print(main_part1())


# -*- coding: utf-8 -*-
# LR 总控程序(查表程序)
# Created by Shengjia Yan@2016-5-30
grammar_rule = [
    ['exp', ['exp', '+', 'exp1']],           # 0  exp  -> exp + exp1
    ['exp', ['exp1']],                       # 1  exp  -> exp1
    ['exp1', ['exp1', '*', 'exp2']],         # 2  exp1 -> exp1 * exp2
    ['exp1', ['exp2']],                      # 3  exp1 -> exp2
    ['exp2', ['(', 'exp', ')']],             # 4  exp2 -> ( exp )
    ['exp2', ['number']]                     # 5  exp2 -> number
]

def func_0(p):
    p[0] = p[1] + p[3]
def func_1(p):
    p[0] = p[1]
def func_2(p):
    p[0] = p[1] * p[3]
def func_3(p):
    p[0] = p[1]
def func_4(p):
    p[0] = p[2]
def func_5(p):
    p[0] = p[1]

func_rule = [func_0, func_1, func_2, func_3, func_4, func_5]



# LR 分析表 非终结符和终结符长度都大于1
parsing_table = {
    0:{'ACTION':{'number':'S5', '(':'S4'}, 'GOTO':{'exp':1, 'exp1':2, 'exp2':3}},
    1:{'ACTION':{'+':'S6', '$':'acc'}, 'GOTO':{}},
    2:{'ACTION':{'+':'r1', '*':'S7', ')':'r1', '$':'r1'}, 'GOTO':{}},
    3:{'ACTION':{'+':'r3', '*':'r3', ')':'r3', '$':'r3'}, 'GOTO':{}},
    4:{'ACTION':{'number':'S5', '(':'S4'}, 'GOTO':{'exp':8, 'exp1':2, 'exp2':3}},
    5:{'ACTION':{'+':'r5', '*':'r5', ')':'r5', '$':'r5'}, 'GOTO':{}},
    6:{'ACTION':{'number':'S5', '(':'S4'}, 'GOTO':{'exp1':9, 'exp2':3}},
    7:{'ACTION':{'number':'S5', '(':'S4'}, 'GOTO':{'exp2':10}},
    8:{'ACTION':{'+':'S6', ')':'S11'}, 'GOTO':{}},
    9:{'ACTION':{'+':'r0', '*':'S7', ')':'r0', '$':'r0'}, 'GOTO':{}},
    10:{'ACTION':{'+':'r2', '*':'r2', ')':'r2', '$':'r2'}, 'GOTO':{}},
    11:{'ACTION':{'+':'r4', '*':'r4', ')':'r4', '$':'r4'}, 'GOTO':{}}
}


# 终结符
def terminalSymbols():
    return ['i', '+', '*', '(', ')', '#']

# 非终结符
def nonTerminalSymbols():
    return ['E', 'T', 'F']

# 是终结符？
def isTerminalSymbol(char):
    return char in terminalSymbols()

# 是非终结符？
def isNonTerminalSymbols(char):
    return char in nonTerminalSymbols()


class Token():
    def __init__(self, name, value=''):
        self.name = name
        if value == '':
            self.value = name
        else:
            self.value = value

# 总控程序
def allControl(input_stack):
    state_stack  = []        # 状态栈
    symbol_stack = []        # 符号栈
    value_stack  = []        # 值栈
    pointer      = 0         # 输入串的读头
    move         = ""        # 总控程序的动作

    state_stack.append(0)             # 状态栈的初始状态为0
    symbol_stack.append(Token('$'))   # 符号栈的栈底符为 $
    input_stack.append(Token('$'))    # 输入Token栈以 $ 结尾

    print "%-30s%-30s%-30s%-30s%-30s" %("State Stack", "Symbol Stack", "Input Token", "Value Stack", "Move")

    # 开始分析输入串，总控程序每做一个动作循环一次
    while 1:
        state_string  = ' '.join(map(str, state_stack))                                          # 状态栈转成字符串
        symbol_string = ' '.join(symbol_stack[i].name for i in range(len(symbol_stack)))         # 符号栈转成字符串
        input_string  = ' '.join(input_stack[i].name for i in range(pointer, len(input_stack)))  # 输入Token栈转成字符串
        value_string  = ''
        for i in range(len(value_stack)):
            value_string += str(value_stack[i])
        print "%-30s%-30s%-30s%-30s%-30s" %(state_string, symbol_string, input_string, value_string, move)

        input_token = input_stack[pointer]       # 当前读入符，应该是一个终结符
        input_token_name = input_token.name
        current_state = state_stack[-1]          # 当前状态为状态栈栈顶元素

        # 遇到空白格，报错
        if parsing_table[current_state]['ACTION'].has_key(input_token_name) == False:
            print 'error'
            break

        symbol_in_table = parsing_table[current_state]['ACTION'][input_token_name]    # 表中符号

        # 遇到 'acc'，分析成功
        if symbol_in_table == 'acc':
            print 'Analyse Successfully!'
            break

        action = symbol_in_table[0]          # Shift or Reduce
        number = int(symbol_in_table[1:])    # 'S' 或 'r' 后的数字

        # Shift
        if action == 'S':
            state_stack.append(number)              # 移进的目标状态压入状态栈
            symbol_stack.append(input_token)        # 当前读入符压入符号栈
            value_stack.append(input_token.value)   # 当前读入符的值压入值栈
            move = symbol_in_table + " Shift"       # 当前动作为『移进』
            pointer += 1                            # 读头前进一格

        reduce_error = True     # 产生式是否有错

        # Reduce
        if action == 'r':
            len_production = len(grammar_rule[number])         # 符号栈按照 产生式[number] 归约

            # 遍历产生式右部用'|'分割开的部分，寻找适合归约的产生式右部
            for i in range(1, len_production):
                len_right = len(grammar_rule[number][i])     # 归约产生式第 i 个右部的长度
                len_symbol = len(symbol_stack)               # 符号栈的长度

                # 避免数组越界
                if len_right > (len_symbol-1):
                    continue
                else:
                    temp_production_right = ''.join(grammar_rule[number][i])         # 归约产生式第 i 个右部转成字符串
                    temp_symbol_string    = ''.join(symbol_stack[j].name for j in range(len(symbol_stack)-len_right, len(symbol_stack)))  # 符号栈最后 len_right 个元素转成字符串

                    if temp_production_right in temp_symbol_string:        # 用于归约的产生式右部
                        reduce_error = False                               # 产生式没有错误
                        production_left  = grammar_rule[number][0]         # 归约产生式的左部列表
                        production_right = grammar_rule[number][i]         # 归约产生式的右部列表

                        len_right = len(production_right)                  # 产生式右部的长度

                        p = []
                        p.append(0)

                        # 弹出栈顶的 len_right 项
                        for j in range(len_right):
                            temp_symbol = symbol_stack.pop()
                            state_stack.pop()
                            temp_value = value_stack.pop()
                            p.append(temp_value)

                        # 语义动作 p[0]保存当前归约产生式运算后的结果
                        func_rule[number](p)

                        symbol_stack.append(Token(production_left, p[0]))     # 将产生式左部和对应的值压入符号栈中
                        value_stack.append(p[0])                 # 归约完的值压入值栈
                        temp_current_state = state_stack[-1]     # 当前状态为状态栈栈顶元素

                        # 遇到空白格，报错
                        if parsing_table[temp_current_state]['GOTO'].has_key(production_left) == False:
                            print 'error'
                            break

                        next_state = parsing_table[temp_current_state]['GOTO'][production_left] # 下一状态
                        state_stack.append(next_state)           # 将下一状态压入状态栈

                        break

            move = symbol_in_table + " Reduce"       # 当前动作为『归约』

            if reduce_error == True:
                print "Production "+ str(number) + " error!"
                break



if __name__ == "__main__":
    TokenArr = [Token('number',2), Token('+'), Token('number',2), Token('*'), Token('number',3)]
    allControl(TokenArr)

# -*- coding: utf-8 -*-
# LR 总控程序(查表程序)
# Created by Shengjia Yan@2016-5-30

# 表达式文法
grammar_rule = {
    0:['E', 'E+T'],
    1:['E', 'T'],
    2:['T', 'T*F'],
    3:['T', 'F'],
    4:['F', '(E)'],
    5:['F', 'i']
}

# LR 分析表
parsing_table = {
    0:{'ACTION':{'i':'S5', '(':'S4'}, 'GOTO':{'E':1, 'T':2, 'F':3}},
    1:{'ACTION':{'+':'S6', '#':'acc'}, 'GOTO':{}},
    2:{'ACTION':{'+':'r1', '*':'S7', ')':'r1', '#':'r1'}, 'GOTO':{}},
    3:{'ACTION':{'+':'r3', '*':'r3', ')':'r3', '#':'r3'}, 'GOTO':{}},
    4:{'ACTION':{'i':'S5', '(':'S4'}, 'GOTO':{'E':8, 'T':2, 'F':3}},
    5:{'ACTION':{'+':'r5', '*':'r5', ')':'r5', '#':'r5'}, 'GOTO':{}},
    6:{'ACTION':{'i':'S5', '(':'S4'}, 'GOTO':{'T':9, 'F':3}},
    7:{'ACTION':{'i':'S5', '(':'S4'}, 'GOTO':{'F':10}},
    8:{'ACTION':{'+':'S6', ')':'S11'}, 'GOTO':{}},
    9:{'ACTION':{'+':'r0', '*':'S7', ')':'r0', '#':'r0'}, 'GOTO':{}},
    10:{'ACTION':{'+':'r2', '*':'r2', ')':'r2', '#':'r2'}, 'GOTO':{}},
    11:{'ACTION':{'+':'r4', '*':'r4', ')':'r4', '#':'r4'}, 'GOTO':{}}
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


# 总控程序
def allControl(input_string):
    state_stack  = []        # 状态栈
    symbol_stack = []        # 符号栈
    input_string += '#'      # 输入串以#结尾
    pointer      = 0         # 输入串的读头
    move         = ""        # 总控程序的动作

    state_stack.append(0)       # 状态栈的初始状态为0
    symbol_stack.append('#')    # 符号栈的栈底符为#

    print "%-30s%-30s%-30s%-30s" %("State Stack", "Symbol Stack", "Input String", "Move")

    # 开始分析输入串，总控程序每做一个动作循环一次
    while 1:
        state_string  = ' '.join(map(str, state_stack))  # 状态栈转成字符串
        symbol_string = ''.join(symbol_stack)           # 符号栈转成字符串
        print "%-30s%-30s%-30s%-30s" %(state_string, symbol_string, input_string[pointer:], move)

        input_char = input_string[pointer]  # 当前读入符，应该是一个终结符
        current_state = state_stack[-1]     # 当前状态为状态栈栈顶元素

        # 遇到空白格，报错
        if parsing_table[current_state]['ACTION'].has_key(input_char) == False:
            print 'error'
            break

        symbol_in_table = parsing_table[current_state]['ACTION'][input_char]    # 表中符号

        # 遇到 'acc'，分析成功
        if symbol_in_table == 'acc':
            print 'Analyse Successfully!'
            break

        action = symbol_in_table[0]         # Shift or Reduce 
        number = int(symbol_in_table[1])    # 'S' 或 'r' 后的数字

        # Shift
        if action == 'S':
            state_stack.append(number)          # 移进的目标状态压入状态栈
            symbol_stack.append(input_char)     # 当前读入符压入符号栈
            move = symbol_in_table + " Shift"    # 当前动作为『移进』
            pointer += 1                        # 读头前进一格

        # Reduce
        if action == 'r':
            # 目前不具备直接处理带有'|'的表达式文法的功能，带'|'的产生式最好需要提前拆分
            production_left  = grammar_rule[number][0]  # 归约产生式的左部
            production_right = grammar_rule[number][1]  # 归约产生式的右部
            len_right = len(production_right)           # 产生式右部的长度

            # 弹出栈顶的 len_right 项
            for i in range(len_right):
                symbol_stack.pop()
                state_stack.pop()

            temp_symbol_string = ''.join(symbol_stack)  # 符号栈转成符号字符串
            temp_symbol_string += production_left       # 将产生式左部压入栈中
            symbol_stack = list(temp_symbol_string)     # 符号字符串转成符号栈

            temp_current_state = state_stack[-1]     # 当前状态为状态栈栈顶元素

            # 遇到空白格，报错
            if parsing_table[temp_current_state]['GOTO'].has_key(production_left) == False:
                print 'error'
                break

            next_state = parsing_table[temp_current_state]['GOTO'][production_left] # 下一状态
            state_stack.append(next_state)           # 将下一状态压入状态栈

            move = symbol_in_table + " Reduce"    # 当前动作为『归约』


if __name__ == "__main__":
    string = raw_input("Enter the input_string: ")
    allControl(string)

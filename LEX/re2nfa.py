# -*- coding: utf-8 -*-
# RegEx -> NFA
# Created by Shengjia Yan @2016-5-21

import networkx as nx               # 调用各种图算法的计算，通过调用python画图包matplotlib能实现图的可视化。
import os                           # 包含普遍的操作系统功能
import Image

class MyGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()    # 构建有向图
        self.first = -1       # 起点
        self.last  = -1       # 终点

    def __str__(self):
        return str(self.first) + '--' + str(self.graph[self.first]) + '--' + str(self.last)


# 将 nfa 存储成 .dot 文件，再转成图片
def storeAsPNG(mg, name='nfa'):
    nx.draw_graphviz(mg)
    nx.write_dot(mg, name + '.dot')
    os.system('dot -Tpng ' + name + '.dot -o ' + name + '.png')
    os.system('open ' + name + '.png')

# 确保节点的标号不同
next_node = -1
def nextNode():
    global next_node
    next_node += 1
    return next_node


# 处理圆括号()，返回右圆括号)的位置
def findParenthesis(string, pos):
    temp = -1
    i = pos
    while i != len(string) and temp != 0:
        if string[i] == '(':
            temp -= 1
        if string[i] == ')':
            temp += 1
            if temp == 0:
                return i
        i += 1
    raise Exception("无法找到对应的圆括号")


# 处理方括号[]，将方括号中的内容转成『或』的形式
def convertSquareBrackets(string):
    i = 0
    small = ''
    big = ''
    m = 0
    n = 0
    newstr = ""
    flag = False    # 是否进入方括号内
    while i != len(string):
        if string[i] == '[':
            newstr += '('
            flag = True
        elif string[i] == ']':
            newstr += ')'
            flag = False
        elif string[i] == '-':    # 必然出现在方括号内
            small = string[i-1]
            big = string[i+1]
            m = ord(small)
            n = ord(big)
            for j in range(m, n+1):
                if j == n and string[i+2] == ']':
                    newstr += chr(j)
                else:
                    newstr += chr(j)
                    newstr += "|"
        else:
            if flag == False:   # 方括号外
                newstr += string[i]
            if flag == True:    # 方括号内
                if string[i-1] != '-' and string[i+1] != '-':
                    if string[i+1] == ']':
                        newstr += string[i]
                    else:
                        newstr += string[i]
                        newstr += '|'
        i += 1
    return newstr
    raise Exception("神秘字符出现在了不该出现的位置")


def convertTerminal2MG(terminal):
    mg = MyGraph()
    mg.first = nextNode()
    mg.last = nextNode()
    mg.graph.add_edge(mg.first, mg.last, label=terminal)
    return mg


# 将 RegEx 转换成 NFA
def convert(input_str):
    length = len(input_str)
    if length == 0:
        return False

    mg_stack = []
    i = 0

    while i < length:
        char = input_str[i]
        if isControlSymbol(char):   # 是控制符
            if char == '(':
                pos = findParenthesis(input_str, i + 1)
                sub_mg = convert(input_str[i + 1 : pos])
                mg_stack.append(sub_mg)
                i = pos + 1
            if char == '*':
                prev = mg_stack.pop()
                sub_mg = repeat(prev)
                mg_stack.append(sub_mg)
                i += 1
            if char == '|':
                mg_stack.append(char)
                i += 1
        elif isTerminalSymbol(char):
            mg_stack.append(convertTerminal2MG(char))
            i += 1

    ret_mg = MyGraph()
    ret_mg.first = nextNode()
    ret_mg.last = nextNode()
    ret_mg.graph.add_nodes_from([ret_mg.first, ret_mg.last])

    prev = None
    for now in mg_stack:
        if now == '|':
            union(ret_mg, prev)
            prev = None
        else:
            if prev is not None:
                prev = concat(prev, now)
            else:
                prev = now
    if prev is not None:
        union(ret_mg, prev)
    return ret_mg


# 合并
def union(mg1, mg2):
    mg1.graph = nx.union(mg1.graph, mg2.graph)
    mg1.graph.add_edge(mg1.first, mg2.first, label='epsilon')
    mg1.graph.add_edge(mg2.last, mg1.last, label='epsilon')
    return mg1


# 重复
def repeat(mg):
    first_nexts = [(i, mg.graph[mg.first][i][0]['label']) for i in mg.graph[mg.first]]
    for n, v in first_nexts:
        mg.graph.add_edge(mg.last, n, label=v)
    mg.graph.remove_node(mg.first)
    mg.first = mg.last
    return mg


# 串联
def concat(mg1, mg2):
    mg1.graph = nx.union(mg1.graph, mg2.graph)
    mg1.graph.add_edge(mg1.last, mg2.first, label='epsilon')
    mg1.last  = mg2.last
    return mg1


# 控制符
def controlSymbols():
    return ['(', ')', '*', '|']


# 是控制符？
def isControlSymbol(char):
    return char in controlSymbols()


# 是终结符？
def isTerminalSymbol(char):
    return not char in controlSymbols()


# 获取所有终结符
def getAllTerminals(re):
    return set([char for char in re if isTerminalSymbol(char)])


def re2nfa(input_str):
    mg = convert(input_str)
    global next_node
    next_node = -1
    return mg


if __name__ == '__main__':
    re = raw_input('Regular Expression: ')
    re = convertSquareBrackets(re)
    nfa = re2nfa(re)
    storeAsPNG(nfa.graph)
    NFA = {}
    for node, nbrsdict in nfa.graph.adjacency_iter():
        EDGE = {}
        NBR = []
        for nbr, attr in nbrsdict.items():
            try:
                EDGE[attr[0]['label']].append(nbr)
            except:
                EDGE[attr[0]['label']] = [nbr]
        NFA[node] = EDGE

print NFA

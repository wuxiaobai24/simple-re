from fa import *

def getLastElem(s):
    res = []
    count = 0
    for i in range(len(s)-1, -1, -1):
        # print(i)
        if s[i] == ')':
            count += 1
        elif s[i] == '(':
            count -= 1
        res.append(s[i])
        if count == 0:
            break
    return ''.join(res[::-1])

def plus2kleene(s):
    output = ''
    for c in s:
        if c == '+':
            output += getLastElem(output)
            output += '*'
        else:
            output += c
    return output

def addConcatOp(s):
    if len(s) == 0:
        return s
    output = s[0]
    for i in range(len(s) - 1):
        L, R = s[i], s[i+1]
        if L not in '(|' and R not in '*)|':
            output += '-'
        output += R
    return output

def infix2postfix(s):
    output = ''
    st = []
    for c in s:
        if c in '(|-':
            st.append(c)
        elif c == ')':
            assert(len(st) != 0)
            assert(st[-1] == '(')
            st.pop()
        else:
            output += c
            # print(st, c)
            if len(st) != 0 and st[-1] != '(':
                output += st[-1]
                st.pop()
    while len(st) != 0:
        output += st[-1]
        st.pop()
    return output

def preprocess(s):
    s = s.replace('{', '(')
    s = s.replace('}', ')')
    s = s.replace(',', '|')
    # print(s)
    s = plus2kleene(s)
    # print(s)
    s = addConcatOp(s)
    # print(s)
    s = infix2postfix(s)
    # print(s)
    return s
    

def re2nfa(pattern):
    st = []
    for c in pattern:
        if c == '|':
            assert(len(st) >= 2)
            nfa1, nfa2 = st[-2], st[-1]
            st.pop(), st.pop()
            st.append(NFA.OR(nfa1, nfa2))
        elif c == '-':
            assert(len(st) >= 2)
            nfa1, nfa2 = st[-2], st[-1]
            st.pop(), st.pop()
            st.append(NFA.CONCAT(nfa1, nfa2))
        elif c == '*':
            assert(len(st) >= 1)
            nfa = st[-1]
            st.pop()
            st.append(NFA.CLOSURE(nfa))
        else:
            st.append(NFA.BASIC(c))
    return st[-1]

if __name__ == "__main__":
    s = 'abc{a,b,c}*(e|f)+kkk'
    s = preprocess(s)
    nfa = re2nfa(s)
    state2index = nfa.toGraph()
    state2index = nfa.geneState2Index()
    text = 'abcacbacbeekkk'
    print(nfa.match(text))
    print(nfa.match('abckkk'))
    
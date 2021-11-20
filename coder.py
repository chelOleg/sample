import math
from os.path import getsize


class TxTCoder:
    def __init__(self):
        self.sym = []  # Список символов
        self.count = []  # Частота
        self.ent = []  # Энтропия
        self.sh_fn = []  # Коды Шенон Фано
        self.hfmn = []  # Коды Хафман
        self.unfrm = []  # Коды равномерные

    def count_sym(self, text): # Функция для подсчета уникальных символов и их энтропии
        l = len(text)
        _sym = []
        _count = []
        _ent = []
        _sh_fn = []
        for el in text:
            if el in _sym:
                _count[_sym.index(el)] += 1
            else:
                _sym.append(el)
                _count.append(1)
        for i in _count:
            _ent.append(i / l * math.log2(l / i))

        j = list(zip(_sym, _count, _ent))
        j.sort(key=lambda x: x[1], reverse=True)
        self.sym, self.count, self.ent = zip(*j)
        self.sym, self.count, self.ent = list(self.sym), list(self.count), list(self.ent)

    def extend(self, elements):  # Добавление символов, которые не встречались в тексте
        for el in elements:
            self.sym.append(el)
            self.count.append(0)
            self.ent.append(0)

    def get_codes(self):  # Функциявызывающае создание шифров 3 видов
        self.sh_fn = [''] * len(self.sym)
        j = list(zip(self.sym, self.count, self.ent, self.sh_fn))
        j = self.shenon_fano(j)
        self.sym, self.count, self.ent, self.sh_fn = zip(*j)
        self.uniform()
        self.hafman()

    def shenon_fano(self, syms):  # Кодирование Шенона-Фано
        if len(syms) > 2:
            dif = 99999
            for i in range(len(syms) - 1):
                l = 0
                r = 0
                for j in syms[:i + 1]:
                    l += j[1]
                for k in syms[i + 1:]:
                    r += k[1]
                if dif > abs(l - r):
                    dif = abs(l - r)
                else:
                    syms[:i] = list(map(lambda x: [x[0], x[1], x[2], x[3] + '1'], syms[:i]))
                    syms[i:] = list(map(lambda x: [x[0], x[1], x[2], x[3] + '0'], syms[i:]))
                    break

            if len(syms[:i]) > 1:
                syms[:i] = self.shenon_fano(syms[:i])
            if len(syms[i:]) > 1:
                syms[i:] = self.shenon_fano(syms[i:])
        else:
            syms[0][3] += '1'
            syms[1][3] += '0'
        return syms

    def hafman(self): # Кодирование Хафмана
        p = [''] * len(self.sym)
        l = []
        for i in range(len(self.sym)):
            l.append([self.count[i], [[self.sym[i], '']]])
        while len(l) > 1:
            l.sort(key=lambda x: x[0])
            for el in l[0][1]:
                el[1] = '0' + el[1]
            for el in l[1][1]:
                el[1] = '1' + el[1]
            l[0][0] += l[1][0]
            l[0][1].extend(l[1][1])
            del l[1]
        for el in l[0][1]:
            p[self.sym.index(el[0])] = el[1]
        self.hfmn = p

    def uniform(self): # Равномерное кодирование
        syms = self.sym
        n = math.ceil(math.log2(len(syms)))
        r = [''] * len(syms)
        for i in range(len(syms)):
            b = str(bin(i))[2:]
            r[i] = '0' * (n - len(b)) + b
        self.unfrm = r

    def coder(self, cod): # Создание ключ словаря
        d = {}
        if cod == 'h':
            c = self.hfmn
        if cod == 'sh':
            c = self.sh_fn
        if cod == 'u':
            c = self.unfrm
        for i in range(len(self.sym)):
            d[self.sym[i]] = c[i]
        return d

    def decoder(self, text, cod): # Декодирование
        d = {}
        res = ''
        if cod == 'h':
            c = self.hfmn
        if cod == 'sh':
            c = self.sh_fn
        if cod == 'u':
            c = self.unfrm
        for i in range(len(self.sym)):
            d[c[i]] = self.sym[i]
        i = 2
        while text:
            if text[:i] in d.keys():
                res += d[text[:i]]
                text = text[i:]
                i = 2
            else:
                i += 1
                if i > 20:
                    print('Ошибка кодирвания')
                    break
        return res

    def avg_len(self):
        print('uniform, shefon_fano, hafman')
        for l in [self.unfrm, self.sh_fn, self.hfmn]:
            n = ''
            for el in l:
                n += el
            if l: print(len(n) / len(l))

if __name__ == '__main__':


    with open('jack18.txt', 'r') as f:
        jack = f.read()
    with open('lolita18.txt', 'r') as f:
        lolita = f.read()

    coder1 = TxTCoder()
    coder1.count_sym(jack)
    coder2 = TxTCoder()
    coder2.count_sym(lolita)
    sym1 = set(coder1.sym)
    sym2 = set(coder2.sym)
    coder2.extend(sym1 - sym2)
    coder1.extend(sym2 - sym1)
    coder1.get_codes()
    coder2.get_codes()
    jack_hafman = coder1.coder('h')
    jack_fano = coder1.coder('sh')
    jack_uni = coder1.coder('u')
    lolita_hafman = coder2.coder('h')
    lolita_fano = coder2.coder('sh')
    lolita_uni = coder2.coder('u')
    b_jj_hafman = ''
    b_jj_fano = ''
    b_lj_hafman = ''
    b_lj_fano = ''
    b_j_u = ''
    for el in jack:
        b_jj_hafman += jack_hafman[el]
        b_jj_fano += jack_fano[el]
        b_lj_hafman += lolita_hafman[el]
        b_lj_fano += lolita_fano[el]
        b_j_u += jack_uni[el]
    b_ll_hafman = ''
    b_ll_fano = ''
    b_jl_hafman = ''
    b_jl_fano = ''
    b_l_u = ''
    for el in lolita:
        b_ll_hafman += lolita_hafman[el]
        b_ll_fano += lolita_fano[el]
        b_jl_hafman += jack_hafman[el]
        b_jl_fano += jack_fano[el]
        b_l_u += lolita_uni[el]

    with open('jack_fano18.txt', 'w') as f:
        f.write(b_jj_fano)

    with open('lolita_fano18.txt', 'w') as f:
        f.write(b_ll_hafman)

    with open('info.txt', 'w') as f:
        lines = [f"Количество символов\n",
                 f"             джек хафман:{len(b_jj_hafman)}; Шенон-Фано {len(b_jj_fano)};"
                 f" равномерное {len(b_j_u)}; количество символов {len(jack)}\n",
                 f"       Чужой джек хафман:{len(b_lj_hafman)}; Шенон-Фано {len(b_lj_fano)};\n",
                 f"           лолита хафман:{len(b_ll_hafman)}; Шенон-Фано {len(b_ll_fano)}; "
                 f"равномерное {len(b_l_u)}; количество символов {len(lolita)}\n",
                 f"     Чужой лолита хафман:{len(b_jl_hafman)}; Шенон-Фано {len(b_jl_fano)};\n",
                 f"Энтропия джек: {round(sum(coder1.ent),4)} Лолита: {round(sum(coder2.ent),4)}\n",
                 "Средняя длинна кодового слова\n",
                 f"        джек хафман:{round(len(b_jj_hafman)/len(jack),4)}; Шенон-Фано {round(len(b_jj_fano)/len(jack),4)};\n",
                 f"      лолита хафман:{round(len(b_ll_hafman)/len(lolita),4)}; Шенон-Фано {round(len(b_ll_fano)/len(lolita),4)};\n",
                 f"  Чужой джек хафман:{round(len(b_lj_hafman)/len(jack),4)}; Шенон-Фано {round(len(b_lj_fano)/len(jack),4)};\n",
                 f"Чужой лолита хафман:{round(len(b_jl_hafman)/len(lolita),4)}; Шенон-Фано {round(len(b_jl_fano)/len(lolita),4)};\n",
                 f" Вес файлов\n",
                 f"         Вес джек: {getsize('jack18.txt')} Байт\n",
                 f"       Вес лолита: {getsize('lolita18.txt')} Байт\n",
                 f"  Вес джек хафман: {math.ceil(len(b_jj_fano)/8)}  Байт\n",
                 f"Вес лолита хафман: {math.ceil(len(b_ll_fano)/8)}  Байт\n"
                 ]
        f.writelines(lines)
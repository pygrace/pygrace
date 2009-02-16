# -*- coding: utf-8 -*-

lookup = {
    r'\alpha': r'\xa\f{}',
    r'\leq': r'\x�\f{}',
    r'\geq': r'\x�\f{}',
    }

grace_symbols = r' ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïñòóôõö÷øùúûüýþ'

class LatexString(str):
    def __str__(self):
        result = self
        for (latex, grace) in lookup.iteritems():
            result = result.replace(latex, grace)
        return result

if __name__ == '__main__':

    s = LatexString(r'\alpha \leq 0.5')

    print s


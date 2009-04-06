CONVERT = {
    r'$\pm$': r'\f{Symbol}\c1\C\f{}',
    r'$\aleph$': r'\f{Symbol}\c@\C\f{}',
    r'$\ge$': r'\f{Symbol}\c3\C\f{}',
    r'$\le$': r'\f{Symbol}\c#\C\f{}',
    r'$\propto$': r'\f{Symbol}\c5\C\f{}',
    r'$\in$': r'\f{Symbol}\cN\C\f{}',
    r'$\infty$': r'\f{Symbol}\c%\C\f{}',
    r'$\partial$': r'\f{Symbol}\c6\C\f{}',
    r'$\Rightarrow$': r'\f{Symbol}\c^\C\f{}',
    r'$\spadesuit$': r'\f{Symbol}\c*\C\f{}',
    r'$\ne$': r'\f{Symbol}\c9\C\f{}',
    r'$\diamondsuit$': r'\f{Symbol}\c(\C\f{}',
    r'$\heartsuit$': r'\f{Symbol}\c)\C\f{}',
    r'$\uparrow$': r'\f{Symbol}\c-\C\f{}',
    r'$\Downarrow$': r'\f{Symbol}\c_\C\f{}',
    r'$\mid$': r'\f{Symbol}\c=\C\f{}',
    r'$\leftrightarrow$': r'\f{Symbol}\c+\C\f{}',
    r'$\rangle$': r'\f{Symbol}\cq\C\f{}',
    r'$\int$': r'\f{Symbol}\cr\C\f{}',
    r'$\rceil$': r'\f{Symbol}\cy\C\f{}',
    r'$\lceil$': r'\f{Symbol}\ci\C\f{}',
    r'$\nabla$': r'\f{Symbol}\cQ\C\f{}',
    r'$\oplus$': r'\f{Symbol}\cE\C\f{}',
    r'$\prod$': r'\f{Symbol}\cU\C\f{}',
    r'$\supset$': r'\f{Symbol}\cI\C\f{}',
    r'$\notin$': r'\f{Symbol}\cO\C\f{}',
    r'$\angle$': r'\f{Symbol}\cP\C\f{}',
    r'$\Leftrightarrow$': r'\f{Symbol}\c[\C\f{}',
    r'$\rfloor$': r'\f{Symbol}\c{\C\f{}',
    r'$\Uparrow$': r'\f{Symbol}\c]\C\f{}',
    r'$\langle$': r'\f{Symbol}\ca\C\f{}',
    r'$\lfloor$': r'\f{Symbol}\ck\C\f{}',
    r'$\otimes$': r'\f{Symbol}\cD\C\f{}',
    r'$\cap$': r'\f{Symbol}\cG\C\f{}',
    r'$\cup$': r'\f{Symbol}\cH\C\f{}',
    r'$\subseteq$': r'\f{Symbol}\cJ\C\f{}',
    r'$\supset$': r'\f{Symbol}\cL\C\f{}',
    r'$\approx$': r'\f{Symbol}\c;\C\f{}',
    r'$\equiv$': r'\f{Symbol}\c:\C\f{}',
    r'$\copyright$': r'\f{Symbol}\cc\C\f{}',
    r'$\leftarrow$': r'\f{Symbol}\c,\C\f{}',
    r'$\rightarrow$': r'\f{Symbol}\c.\C\f{}',
    r'$\downarrow$': r'\f{Symbol}\c/\C\f{}',
    r'$\Re$': r'\f{Symbol}\cB\C\f{}',
    r'$\supseteq$': r'\f{Symbol}\cM\C\f{}',
    r'$\ldots$': r'\f{Symbol}\c<\C\f{}',
    }

SORTED_CONVERT = CONVERT.items()
SORTED_CONVERT = [(len(key), (key, value)) for (key, value) in SORTED_CONVERT]
SORTED_CONVERT.sort(reverse=True)
SORTED_CONVERT = [(key, value) for (len, (key, value)) in SORTED_CONVERT]

class LatexString(str):

    def __str__(self):
        result = self
        for (latex, grace) in SORTED_CONVERT:
            result = result.replace(latex, grace)
        return result

    def __add__(self,other):
        return str(self) + other

    def __radd__(self,other):
        return other + str(self)

if __name__ == '__main__':

    s = LatexString(r'Q $\in$ 0.5')
    print s

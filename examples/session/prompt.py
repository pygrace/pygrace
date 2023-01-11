from pygrace.session import grace

if __name__ == "__main__":
    x = list(range(1,15))
    y = []
    for i in x:
        y.append(i*i)
    g = grace()
    g.plot(x,y)
    g.put('x',x)
    g.put('y',y)
    g.prompt()
    print(g.who())
    g.exit()


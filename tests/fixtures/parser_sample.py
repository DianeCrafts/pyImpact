def a():
    b()
    c()

def b():
    pass

async def d():
    a()

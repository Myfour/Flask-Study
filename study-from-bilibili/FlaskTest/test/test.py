import a
from b import B

print(a.A)
print(B)

'''
此番测试得到的结论就是不管是import还是from一个模块，这个模块中的所有内容都会被执
行，而不只是模块中的某个被用到的对象
'''
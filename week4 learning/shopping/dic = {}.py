dic = {}
string = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"
x = string.split()
for i in range(12):
    dic[x[i]] = i

print(dic)

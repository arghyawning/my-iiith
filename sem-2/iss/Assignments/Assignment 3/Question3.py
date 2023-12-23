a=[]

for i in range(10):
    x=input()
    a.append(x)

print(*a)

x=input("ascending/descending:")
if(x=="ascending"):
    c=1
elif(x=="descending"):
    c=2
else:
    print("invalid input!")
    quit()

if(c==1):
    a.sort()
else:
    a.sort(reverse=True)
print(*a)

x=input()
a.append(x)

if(c==1):
    a.sort()
else:
    a.sort(reverse=True)
print(*a)
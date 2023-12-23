n=int(input("Enter a number between 8 and 20: "))

# if(n<8 or n>20):
#     print("Invalid Input")
# else:
for i in range((int)(n/2), 0, -1):
    for j in range((int)(n/2)-i):
        print(" ",end="")
    for j in range(2*i):
        print("*", end="")
    print()

for i in range(1, ((int)(n/2))+1):
    for j in range((int)(n/2)-i):
        print(" ", end="")
    for j in range(2*i):
        print("*", end="")
    print()
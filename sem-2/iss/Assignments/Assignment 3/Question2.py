class student:
    name: str
    rollnumber: int
    maths: int
    cse: int
    science: int

    def __init__(self, nm, rn, math, cs, sci):
        self.name = nm
        self.rollnumber = rn
        self.maths = math
        self.cse = cs
        self.science = sci

    def displayLite(self):
        print("Name: "+self.name)
        print("Roll Number: "+self.rollnumber)

    def displayMarks(self):
        print("Maths marks: "+str(self.maths))
        print("CSE marks: "+str(self.cse))
        print("Science marks: "+str(self.science))

    def totalMarks(self) -> int:
        return (self.cse+self.maths+self.science)

    def mean(self) -> float:
        return (self.cse+self.maths+self.science)/3.0

    def median(self) -> int:
        marks = []
        marks.append(self.cse)
        marks.append(self.maths)
        marks.append(self.science)
        marks.sort()
        return marks[1]


repo = []
n = int(input("Enter number of students (>=10): "))
print()

# if(n < 10):
#     print("Invalid input")
#     quit()

for i in range(n):
    nm = input("Enter student "+str(i+1)+"'s name: ")
    rn = input("Enter "+nm+"'s roll number: ")
    math = int(input("Enter "+nm+"'s Maths marks: "))
    cs = int(input("Enter "+nm+"'s CSE marks: "))
    sci = int(input("Enter "+nm+"'s Science marks: "))
    print()
    repo.append(student(nm, rn, math, cs, sci))

print("Users:")
for i in range(n):
    repo[i].displayLite()
    print()

print("To see a student's marks, firstly enter")
print("1 to search via name")
print("2 to search via roll number")
choice = input("Enter your choice: ")

sno = -1
if choice == "1":
    nm = input("Enter the name: ")
    for i in range(n):
        if repo[i].name == nm:
            sno = i
            break
    if sno == -1:
        print("Invalid Input")
        quit()

elif choice == "2":
    rn = int(input("Enter the roll number: "))
    for i in range(n):
        if int(repo[i].rollnumber) == int(rn):
            sno = i
            print(n)
            break
    if sno == -1:
        print("Invalid Input")
        quit()
else:
    print("Invalid input")
    quit()

rank = 1
total = repo[sno].totalMarks()
for i in range(n):
    if(i != sno):
        if(total < repo[i].totalMarks()):
            rank = rank+1

print()
repo[sno].displayLite()
repo[sno].displayMarks()
print("Mean marks: "+str(repo[sno].mean()))
print("Median marks: "+str(repo[sno].median()))
print("Rank: "+str(rank))

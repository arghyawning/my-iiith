import csv

def mean(x):
    return sum(x) / len(x)

def calc_corr(x, y):
    x_mean = mean(x)
    y_mean = mean(y)

    a = 0
    b = 0
    c = 0

    for x_i, y_i in zip(x, y):
        diff_x = x_i - x_mean
        diff_y = y_i - y_mean
        a += diff_x * diff_y
        b += diff_x ** 2
        c += diff_y ** 2

    corr = a / ((b * c) ** 0.5)
    return corr

def read(filepath):
    x = []
    with open(filepath, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            x.append(row)
    return x


file1 = "coalstates.csv"
file2 = "hdistates.csv"
X = read(file1)
Y = read(file2)

compX = {}
compY = {}

for i in range (2,11):
    compX = {}
    compY = {}

    for x, y in zip(X, Y):
        state_x = x[0]
        state_y = y[0]
        compX[state_x] = x[i+7]#year
        compY[state_y] = y[i]

    del compX["States"]
    del compY["States"]

    compcoal = []
    comphdi = []

    states = sorted(list(compX.keys()))
    for state in states:
        if state in compY:
            compcoal.append(float(compX[state]))
            comphdi.append(float(compY[state]))

    print(2008+i,"-",9+i,": ", calc_corr(compcoal, comphdi),sep="")

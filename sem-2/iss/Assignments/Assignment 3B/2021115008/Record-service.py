import sqlite3
import csv

# creating a database Record.db
database = sqlite3.connect('Record.db')
cursor = database.cursor()

# creating the ticker table in the database
cursor.execute(
    '''
    CREATE TABLE Ticker
    (Date text, "Company Name" text, Industry text, "Previous Day Price" text,
    "Current Price" text, "Change In Price (%)" text, Confidance text)
    '''
)

# creating the ticker table in the database
cursor.execute(
    '''
    CREATE TABLE Metrics
    (KPIs text, Metrics text)
    '''
)

# extracting the data from the control file
with open('./Control/control-table.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    controlTable = list(reader)  # a list of lists for each day's data
    controlTable.pop(0)
    controlTable.pop(len(controlTable) - 1)


# string manipulation to format the conditions
for i in range(len(controlTable)):
    condition = controlTable[i][1]
    condition = condition.replace('%', '')
    condition = condition.strip()
    condition = condition.replace('&', 'and')
    condition = condition.replace('>', '{0}>')
    condition = condition.replace('<', '{0}<')
    condition = condition.replace('==', '{0}==')
    controlTable[i][1] = condition


tickerDictionary = {}  # this sill store all the supplied data for each day

for i in range(20, 25):
    with open('Record/2021115008-' + str(i) + '-05-2022.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        list_of_rows = list(reader)  # a list of lists for each day's data
        list_of_rows.pop(0)  # removing the header row
    # assigning it with the correct key in dictionary
    tickerDictionary[i] = list_of_rows


# tickerList = []
# dicitionaries to count the number of Highs and Lows for each industry
highs = {
    'Auto Ancillaries': 0,
    'Finance - General': 0,
    'Ceramics & Granite': 0,
}
lows = {
    'Auto Ancillaries': 0,
    'Finance - General': 0,
    'Ceramics & Granite': 0,
}


for i in range(20, 25):
    for j in range(len(tickerDictionary[i])):

        # a list to store the data for each company on each day
        thisRow = []

        thisRow.append(str(i)+'-May-2022')  # date

        thisRow.append(tickerDictionary[i][j][0])  # company name

        thisRow.append(tickerDictionary[i][j][1])  # industry

        if i == 20:
            # if it is the first day, previous day price is not applicable
            previous = 'NA'
        else:
            previous = tickerDictionary[i-1][j][2]
        thisRow.append(previous)
        thisRow.append(tickerDictionary[i][j][2])

        if i == 20:
            # if it is the first day, change in price is not applicable
            changepc = 'Previous day not listed'
        else:
            # calculating change in price %
            changepc = float(tickerDictionary[i][j][2]) - float(previous)
            changepc = changepc / float(previous)
            changepc = changepc * 100
        thisRow.append(str(changepc))

        if i == 24:
            if j == 0:
                # initialising the maximum values
                increment_max = float(tickerDictionary[i][j][2])
                increment_max -= float(tickerDictionary[20][j][2])
                gainpc_max = increment_max
                gainpc_max = gainpc_max / float(tickerDictionary[20][j][2])
                gainpc_max = gainpc_max * 100

                decrement_max = float(tickerDictionary[20][j][2])
                decrement_max -= float(tickerDictionary[i][j][2])
                losspc_max = decrement_max
                losspc_max = losspc_max / float(tickerDictionary[20][j][2])
                losspc_max = losspc_max * 100

                best = tickerDictionary[i][j][0]
                worst = tickerDictionary[20][j][0]
            else:
                increment = float(tickerDictionary[i][j][2])
                increment -= float(tickerDictionary[20][j][2])
                gainpc = increment
                gainpc = gainpc / float(tickerDictionary[20][j][2])
                gainpc = gainpc * 100

                decrement = float(tickerDictionary[20][j][2])
                decrement -= float(tickerDictionary[i][j][2])
                losspc = decrement
                losspc = losspc / float(tickerDictionary[20][j][2])
                losspc = losspc * 100

                # checking if it is the maximum gain
                if gainpc > gainpc_max:
                    gainpc_max = gainpc
                    increment_max = increment
                    best = tickerDictionary[i][j][0]
                elif gainpc == gainpc_max:
                    if increment > increment_max:
                        increment_max = increment
                        gainpc_max = gainpc
                        best = tickerDictionary[i][j][0]
                    elif increment == increment_max:
                        if tickerDictionary[i][j][0] < best:
                            best = tickerDictionary[i][j][0]
                            increment_max = increment
                            gainpc_max = gainpc

                # checking if it is the maximum loss
                if losspc > losspc_max:
                    losspc_max = losspc
                    decrement_max = decrement
                    worst = tickerDictionary[i][j][0]
                elif losspc == losspc_max:
                    if decrement > decrement_max:
                        decrement_max = decrement
                        losspc_max = losspc
                        worst = tickerDictionary[i][j][0]
                    elif decrement == decrement_max:
                        if tickerDictionary[i][j][0] > worst:
                            worst = tickerDictionary[i][j][0]
                            decrement_max = decrement
                            losspc_max = losspc

        if i == 20:
            confidance = 'Listed New'
        else:
            # checking the conditions for confidance
            for k in range(len(controlTable)):
                if tickerDictionary[i][j][1] == controlTable[k][0]:
                    if eval(controlTable[k][1].format(changepc)):
                        confidance = controlTable[k][2]
                        break

        if confidance == 'High':
            highs[thisRow[2]] += 1
        elif confidance == 'Low':
            lows[thisRow[2]] += 1

        thisRow.append(confidance)
        cursor.execute(
            '''
            INSERT INTO Ticker VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', thisRow
        )
        # tickerList.append(thisRow)


# incserting the data for the Metrics table
cursor.executemany(
    '''
    INSERT INTO Metrics VALUES (?, ?)
    ''', [
        ('Best listed Industry', max(highs, key=highs.get)),
        ('Best Company', best),
        ('Gain %', str(gainpc_max)),
        ('Worst listed Industry', max(lows, key=lows.get)),
        ('Worst Company', worst),
        ('Loss %', str(losspc_max))
    ]
)

# saving all changes
database.commit()
database.close()

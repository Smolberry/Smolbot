
#Not an assignment, a module made by me to make the rest of my assignments easier

#A function that makes a pretty chart when given a header, names of the categories and the values
usage = """
A module that will help in the making of pretty charts

The usage is as follows:
    The header as a string object
    the categories in a list
    the values in a list
    
This will produce a chart that has colons seperating the categories and values in a single
column, and a seperator between the header and chart equal to the longest line length.

You cannot enter a number of items and values that don't match up
"""
def makeChart(header, items, values):
    biggest = 0
    biggestVal = 0
    seperator = ""
    lines = []
    counter = 0
    sepChar = ":"
    result = ""
    
    #Checks if the number of categories is equal to the number of values
    if len(items) == len(values):
        #Checks for the biggest category
        for i in items:
            if len(i) > biggest:
                biggest = len(i)
                
        #Creates the starter of the lines "foobar :"
        for i in items:
            if len(i) == biggest:
                lines.append(i+sepChar)
            else:
                tempVar = (biggest - len(i)) * " "
                lines.append(i+tempVar+sepChar)
                
        #Adds in the rest of the lines "foobar : foobar"
        #Also gets the biggest value
        for i in values:
            lines[counter] += " "+i
            counter += 1
            if len(i) > biggestVal:
                biggestVal = len(i)
                
        #Creating the seperator by the longest line length "==============="
        seperator = (biggest + biggestVal + len(sepChar) + 1) * "="

        #Printing the chart
        result += header+"\n" \
                  " " +seperator+"\n" \
                  " "
        for i in lines:
            result+=i+"\n" \
                     ""
    else:
        result+="Number of items must be equal to the number of values"
    return result
        
def makeChartList(stuff):
    header, items, values = stuff[0], stuff[1], stuff[2]
    biggest = 0
    biggestVal = 0
    seperator = ""
    lines = []
    counter = 0
    sepChar = ":"
    
    #Checks if the number of categories is equal to the number of values
    if len(items) == len(values):
        #Checks for the biggest category
        for i in items:
            if len(i) > biggest:
                biggest = len(i)
                
        #Creates the starter of the lines "foobar :"
        for i in items:
            if len(i) == biggest:
                lines.append(i+sepChar)
            else:
                tempVar = (biggest - len(i)) * " "
                lines.append(i+tempVar+sepChar)
                
        #Adds in the rest of the lines "foobar : foobar"
        #Also gets the biggest value
        for i in values:
            lines[counter] += " "+i
            counter += 1
            if len(i) > biggestVal:
                biggestVal = len(i)
                
        #Creating the seperator by the longest line length "==============="
        seperator = (biggest + biggestVal + len(sepChar) + 1) * "="

        #Printing the chart
        print("<br/>"+header)
        print(seperator)
        for i in lines:
            print(i)
    else:
        print("Number of items must be equal to the number of values")

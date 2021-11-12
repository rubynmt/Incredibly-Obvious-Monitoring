from tabulate import tabulate

def displayCPUTable(data):
    #This function will take CPU date and display in a table for console
    header=['DATE', 'TIME', 'CPU LOAD']
    print(tabulate(data, headers=header))



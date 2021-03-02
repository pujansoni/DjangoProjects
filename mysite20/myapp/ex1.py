# Defining the list
mylist = [5, -3, 0, 12, 7, 4]

# Iterating through the list using the for loop
for element in mylist:
    # Print 'Zero' if the element is zero
    if element == 0:
        print('Zero')
    # Print 'Positive' if the element is positive
    elif element > 0:
        print('Positive')
    # Print 'Negative' if the element is negative
    elif element < 0:
        print('Negative')

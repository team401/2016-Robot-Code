#Function definition, this code DOES NOT RUN.
#fiz is a parameter. When we call the function we have to pass something into it
def redFrisbee(fiz):
    number = 5 + 7 + fiz
    testStr = 'hi'
    
    #This shows how you can return multiple values out of a function.
    return number,testStr

#Uncomment line 12 for an example of how you can't access variables that are
#inside of a function - we have to pass it in the return or modify a global!
#otherNum = number

#This works because we returned multiple values out of the redFrisbee function.
otherNum,newName = redFrisbee(10)
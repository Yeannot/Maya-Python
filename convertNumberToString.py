ones    = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
tens1   = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens2   = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
hundred = "hundred"

#
def numToStr(number):
    result = ""
    #strNum = str(number)
    strNum = number
    
    while strNum[0] == "0":
        strNum = strNum[1:]
            
    if len(strNum) > 2:
        firstNum  = int(strNum[0])
        secondNum = int(strNum[1:3])
        result = numbers[firstNum] + " " + hundred + " " + numbers[secondNum]
    else:
        result = numbers[number]
    

    return result.replace(" zero", "")

#    
def convertNumber():
    number = raw_input("Type number :")
    result = numToStr(number)
    
    print ( number, result )
    
    
    
###
convertNumber()

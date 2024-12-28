import tabulate #imports the tabulate library
from colorama import  Fore, Style #imports the colorama library
import pyttsx3 #imports the text to speech library

engine =pyttsx3.init ('sapi5')
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)

def speak (audio):
    engine.say(audio)
    engine.runAndWait()

#initializing global variables
itemAmountInput = 0
selectionItemInput = 0
totalItemPrice = 0
userMoneyInput = 0

Items = { #Dictionary where the key is the number for the item, then value is the price of the item
    1:["1. Water", 1.0, 3], #This Dictionary utilizes a 3D array (a list within a dictionary)
    2:["2. Boca Bola", 2.5, 4],
    3:["3. Crite Spranberry", 3.5, 2],
    4:["4. Loritos", 5.5, 2],
    5:["5. Bheetos", 7.5, 4],
    6:["6. Pizza", 15.0, 1],
    7:["7. Cup Noodles", 22.0, 3],
    8:["8. Gold plated Wings", 25.0, 2],
    9:["9. Truffles", 50.0, 1],
    10:["10. Caviar", 100.0, 0]
 }

print (Fore.YELLOW + Style.BRIGHT +'''****************************************************************
       
       
             The Totally Normal Vending Machine.            
             
             
****************************************************************''' + Style.RESET_ALL) #Styled heading for the vending machine

       
def processScreen(): #A function made to show the payment process of the item
    global itemAmountInput
    global selectionItemInput
    global totalItemPrice
    global userMoneyInput
    
    #item selection
    for i in Items.keys(): #checks the keys of the dictionary
        if selectionItemInput == i:
            #Shows the user what they have picked and their price using the .get function
            print (Style.BRIGHT+ Fore.BLUE + f"You selected '{Items.get(i)[0]}'. Price is ${Items.get(i)[1]}.\n'Y' to confirm or 'N' to go back."+ Style.RESET_ALL)
            speak(f"You selected '{Items.get(i)[0]}'. Price is ${Items.get(i)[1]}.'Y' to confirm or 'N' to go back.")
            confirmInput = input().lower()
            if confirmInput == "y":#for loop breaks when y is selected
                break
            elif confirmInput == "n":
                mainScreen()#returns to the main screen when n is selected
            else:
                print(Style.BRIGHT+ Fore.RED + "That is not an option, re-do the process."+ Style.RESET_ALL)
                speak("That is not an option, re-do the process")
                processScreen()
                
    
    #asks how many items the user wants    
    while True:
        try:
            #checks if the user wants more of the specific item
            print(Style.BRIGHT+ Fore.BLUE + "How many do you want? "+ Style.RESET_ALL)
            speak("How many do you want?")
            itemAmountInput = int(input())
            if itemAmountInput > Items.get(selectionItemInput)[2]:
                print(Style.BRIGHT+ Fore.RED + f"There are only {Items.get(selectionItemInput)[2]} left in stock, you can not get more than that"+ Style.RESET_ALL)
                speak(f"There are only {Items.get(selectionItemInput)[2]} left in stock, you can not get more than that")
                continue
            if itemAmountInput <= 0:#checks if the user has entered 0 or below
                print (Style.BRIGHT+ Fore.RED + "You cannot enter 0 or negative numbers."+ Style.RESET_ALL)
                speak("You cannot enter 0 or negative numbers.")
                continue
            else:
                totalItemPrice = itemAmountInput * Items.get(selectionItemInput)[1] #otherwise the total price will be calculated by the item price multiplied by the amount of items bought
                print(Style.BRIGHT+ Fore.BLUE + f"You want {itemAmountInput} amount of '{Items.get(selectionItemInput)[0]}'. The total price is ${totalItemPrice}."+ Style.RESET_ALL)
                speak(f"You want {itemAmountInput} amount of '{Items.get(selectionItemInput)[0]}'. The total price is ${totalItemPrice}.")
            break
        except:#checks if the user has entered the appropriate data type
            print(Style.BRIGHT+ Fore.RED + "That is not a number, Please re-enter."+ Style.RESET_ALL)
            speak("That is not a number, Please re-enter.")
        
    #asking for the amount of payment
    while True:
        try:
            #asks for the user's money
            print (Style.BRIGHT+ Fore.BLUE + "Enter the amount of money you have ON HAND: "+ Style.RESET_ALL)
            speak("Enter the amount of money you have ON HAND: ")
            userMoneyInput = float(input())
            #calculate the amount needed for change if the user has payed more than they needed to
            totalChange = userMoneyInput - totalItemPrice
            
            # confirm payment
            if userMoneyInput < totalItemPrice:
                #checks if the user has payed less than the amount needed, if y is selected then it will continue to ask until the user puts in the right amount
                print(Style.BRIGHT+ Fore.RED + "This is an insufficient amount, do you want to continue? (Y/N)"+ Style.RESET_ALL)
                speak("This is an insufficient amount, do you want to continue? (Y/N)")
                confirmInput = input().lower()
                if confirmInput == "y":
                    continue
                elif confirmInput == "n":
                    mainScreen() #returns to the main screen if the user chose n
                else:
                      print(Style.BRIGHT+ Fore.RED + "That is not an option, re-do the process."+ Style.RESET_ALL)
                      speak("That is not an option, re-do the process.")
                      processScreen()
                    
                    #this shows the item bought and the amount of change the user has gotten
            print (Style.BRIGHT+ Fore.YELLOW + f"The '{Items.get(selectionItemInput)[0]}' has been dropped and you received a total change of ${totalChange}"+ Style.RESET_ALL)
            speak(f"The '{Items.get(selectionItemInput)[0]}' has been dropped and you received a total change of ${totalChange}")
            #Reduce item stock
            Items.get(selectionItemInput)[2] -= itemAmountInput
            break
        except: #this checks if the user has entered the appropriate data type.
            print(Style.BRIGHT+ Fore.RED + "That is not a number, Please re-enter your cash in hand."+ Style.RESET_ALL)
            speak("That is not a number, Please re-enter your cash in hand.")
            
    mainScreen()
    
            
def mainScreen(): #A function made to show the table of the items and the starting area for the vending machine
   global Items #global variables that needs to be accessed outside of the function
   global selectionItemInput
   
   # Print the table of items using the tabulate function
   table = tabulate.tabulate(Items.values(),headers = ["Items", "Price ($)", "Stock"], tablefmt="pipe", floatfmt=".1f")
   print(table)
   
   while True:
       try:
           #asks the user for the desired item
           print(Style.BRIGHT+ Fore.BLUE + "Please enter the desired Item (1-10): " + Style.RESET_ALL)
           speak("Please enter the desired Item (1-10):")
           selectionItemInput = int(input())
           
           
           if Items.get(selectionItemInput)[2] <= 0:#This is used to check if the item is out of stock
               print (Style.BRIGHT+ Fore.RED + "This item is out of stock"+ Style.RESET_ALL)
               speak("This item is out of stock")
               mainScreen()
               
       except:
           print(Style.BRIGHT+ Fore.RED + "Please input numbers only"+ Style.RESET_ALL) #Checks if only integers are entered
           speak ("Please input numbers only")
           continue 
       
       if selectionItemInput <1 or selectionItemInput >10:
           print (Style.BRIGHT+ Fore.RED + "Please enter between 1 - 10"+ Style.RESET_ALL) #Checks if 1 - 10 is entered
           speak("Please enter between 1-10")
           continue
       else:
           break
       
   processScreen() #goes to the payment screen

mainScreen() #Starts the whole program on the mainScreen

    
    
        

        
        
    

        

import cs50

def main():
    while True:
        print("O hai! How much change is owed?")
        amount = cs50.get_float()
        if amount >= 0:
            break
    
    numberofcoins = 0
    cents = int(round(amount * 100))
    
    numberofcoins += cents // 25
    cents %= 25
    
    numberofcoins += cents // 10
    cents %= 10
    
    numberofcoins += cents // 5
    cents %= 5
    
    numberofcoins += cents
    
    print("{}".format(numberofcoins))
    
if __name__ == "__main__":
    main()
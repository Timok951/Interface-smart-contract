from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract
import re


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = w3.eth.contract(address=address_contract, abi=abi)

def login():
    try:
        login=input("login ")
        password=input("password ")
        w3.geth.personal.unlock_account(login, password)
        return(login)
    except Exception as e:
        print(f"Incorrect password or user{e}")
        return None

def passwordCheck(password):
        # Проверка длины пароля
    if len(password) < 12:
        print("Password must be mor then 12 character")
        return False
    
    # Проверка наличия заглавных букв
    if not re.search(r'[A-Z]', password):
        print("Must be one upper character")
        return False
    
    # Проверка наличия строчных букв
    if not re.search(r'[a-z]', password):
        print("Must be one lower character")
        return False
    
    # Проверка наличия цифр
    if not re.search(r'\d', password):
        print("Must be one number")
        return False
    
    # Проверка наличия специальных символов
    if not re.search(r'[!@#\$%]', password):
        print("Must be one special character")
        return False
    
    # Проверка на простые шаблоны
    if re.search(r'password|qwerty', password):
        print("Must be not common")
        return False
    
    return True

def register(password):
    if passwordCheck(password) == True:
        new_account = w3.geth.personal.new_account(password)
        print(new_account)
    else:
        pass

def balance(account_address): 
    try:
        balance =  w3.eth.get_balance(account_address)  
    except Exception as e:
        print(e)
    return balance

def createEstate(account_address):
    try:
        size = int(input("size "))
        memory = input("adress ")
        es_type = int(input("es type "))
        estate = contract.functions.createEstate(size,memory,es_type).transact({'from': account_address})
        print(f"transaction was send {estate.hex()}")
    except Exception as e:
        print(e)

def create_add(account_address):
    try:
        price = input("price")
        idad = input("id add")
        adstatus = input("adstatus")

        ad = contract.functions.createAd(price, idad,adstatus).transact({'from': account_address})
        print(f"add was created {ad.hex()}")
    except Exception as e:
        print(e)

def updateEstateStatus():
    try:
        idestate = input("id estate")
        status = input("status")

        updateEstateStatus = contract.functions.updateEstateStatus(idestate,status).transact()
        print(f"estate was update {updateEstateStatus.hex()}")

    except Exception as e:
        print(e)

def updateAdStatus(account_address):
    try:
        idAd= input("id estate")
        status = input("status ad")

        updateadStatus = contract.functions.updateAdStatus(idAd,status).transact({'from': account_address}) 
        print(f"add was update {updateadStatus.hex()}")

    except Exception as e:
        print(e)

def withDraw(account_address):
    try:
        amount = input("amount")
        withDraw = contract.functions.withDraw(amount).transact({'from': account_address}) 
        print(f"withdraw sucess {withDraw.hex()}" )
    except Exception as e:
        print(e)

def buyEstate(account_address):
    try:
        idad = input("id ad")
        buy = contract.functions.buyEstate(idad).transact({'from': account_address}) 
        print(f"buy sucess {buy.hex()}")

    except Exception as e:
        print(e)

def main(): 

    choice = input("1-registration. 2-login ")
    match choice:
        case "1":
            password = input("password ") 

            register(password)
        case "2":                
            while True: 
                user = login() 
                if user: 
                    print("login success")
                    while True:
                        choice = input("1-get balance, 2-create estate, 3 create add, 4 update estate, 5 update add, 6 withdraw, 7 buy estate, 0-exit ") 
                        match choice:
                            case "1":
                                print (balance(user))
                            case "2":
                                createEstate(user)
                            case "3":
                                create_add(user)
                            case "4":
                                updateEstateStatus(user)
                            case "5":
                                updateAdStatus(user)
                            case "6":
                                withDraw(user)
                            case "7": 
                                buyEstate(user)
                            case "0":
                                break
if __name__ == "__main__":
    main()   


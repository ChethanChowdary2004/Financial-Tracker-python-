from datetime import datetime
date_format = "%d-%m-%Y"
categories  =  {'I':"Income",'E':"Expense"}

     
def get_date(prompt,allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Enter an valid date format")
        return get_date(prompt,allow_default)
    

def get_amount():
    try:
        amount = float(input("Enter the amount: ")) 
        if amount == 0:
            raise ValueError("Enter numbers greater than zero")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()    

def get_category():
    category = input("Enter category ('I' for Income or 'E' for Expense): ").upper()
    if category in categories:
        return categories[category]
    print("Enter an valid category")
    return get_category()

def get_description():
    des = input("Enter an description: ")
    if len(des) == 0:
        print("Enter an valid description")
        return get_description()
    else:
        return des


      
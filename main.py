import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_date,get_category,get_description
import matplotlib.pyplot as plt
from io import StringIO

class CSV:

    CSV_file = "Financial_data.csv"
    COLUMNS = ["Date","amount","category","description"]    
    FORMAT = "%d-%m-%Y"

    @classmethod
    def intiate_csv(self):
        try:
            pd.read_csv(self.CSV_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns = self.COLUMNS)
            df.to_csv(self.CSV_file,index = False)
    @classmethod
    
    def add_entry(self,Date,amount,category,description):

        new_data = {"Date" : Date,
                    "amount" : amount,
                    "category" : category,
                    "description" : description}
        
        with open(self.CSV_file,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=self.COLUMNS)
            writer.writerow(new_data)
        print("Data Entered Successfully")

    @classmethod
    def get_transactions(self,start_date,end_date):
        df = pd.read_csv(self.CSV_file)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date_date = datetime.strptime(end_date,CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No Transactons in the give dates")
        else:
            print(f"Transactions from {start_date} to {end_date}")

            df_show = (filtered_df.to_string(index = False, formatters= {"date" : lambda x : x.strftime(CSV.FORMAT)}))
            print(df_show)

        total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
        total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

        print("\n Summary :")
        print("Total income : {}".format(round(total_income,2)))
        print("Total Expense : {}".format(round(total_expense,2)))
        print("Net Savings : {}".format(round(total_income-total_expense,2)))

        return df_show

    @classmethod
    def del_transaction(self,del_date):
        df = pd.read_csv(self.CSV_file)
        if not del_date:
            del_date = datetime.today().strftime("%d-%m-%Y")
        df["date"] = pd.to_datetime(df["date"],format="%d-%m-%Y")

        in_date = pd.to_datetime(del_date)
        
        df_updated = df[df["date"] != in_date]
        df_updated["date"] = df_updated["date"].dt.strftime(CSV.FORMAT)
        df_updated.to_csv(self.CSV_file,index=False)
        print("Transaction Deleted sucessefully")
        
        

def add():
    CSV.intiate_csv()
    Date = get_date("Enter date in format dd-mm-yyyy or press enter for today's date: ",allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    print(description)

    CSV.add_entry(Date,amount,category,description)

def plot_transactions(df):
    
    data = df
    data_df = StringIO(data)
    df = pd.read_csv(data_df,delimiter=',')
    df.set_index('date',inplace = True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value = 0)

    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value = 0)

    plt.figure(figsize = (20,10))
    plt.plot(income_df.index,income_df["amount"],label = "Income", color = "g")
    plt.plot(expense_df.index,expense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("amount")
    plt.title("Income and Expenses over a Date range")
    plt.legend()
    plt.grid(True)
    plt.show()



def main():
    while True:
        print("\n1.Add a Transaction.")
        print("2.View Transactions with in a date range.")
        print("3.Delete an Transaction")
        print("4.Exit")

        choice = int(input("Eneter number from 1-4: "))
        if choice == 1:
            add()
        elif choice == 2:
            start_date = get_date("Enter the Start Date in the format(dd-mm-yyyy)")
            end_date = get_date("Enter the end date in the format(dd-mm-yyyy)")
            df = CSV.get_transactions(start_date,end_date)
            if input("Do you want to dispaly it in a graph(y/n)").lower() == 'y':
                plot_transactions(df)
        
        elif choice == 3:
            del_date = input("Enter the transaction date in the format(dd-mm-yyyy) or Press enter for today's Date")
            CSV.del_transaction(del_date)


        elif choice == 3:
            print("Exciting.....!")
            break
        else:
            print("Invalid Input please enter 1,2 or 3")

if __name__ == "__main__":
    main()

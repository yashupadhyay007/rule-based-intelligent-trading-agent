import csv
import matplotlib.pyplot as plt 

day_list= []
price_list= []

with open("stock_data.csv","r") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        day_list.append(int(row[0]))
        price_list.append(float(row[1]))

change_list = []
decision_list = []

for i in range(len(price_list)):
    if i == 0:
        change_list.append("-")
        decision_list.append("HOLD")
    else:
        yesterday_price= price_list[ i - 1 ]
        today_price= price_list[ i ]

        change = (( today_price - yesterday_price ) / yesterday_price ) * 100
        change = round( change , 2 )

        change_list.append(change)

        if change <= -2:
            decision_list.append( "BUY" )
        elif change >= 2:
            decision_list.append( "SELL" )
        else:
            decision_list.append( "HOLD" )

profit_list = []
have_stock = False
buy_value = 0
total_profit = 0

buy_day_list =[]
buy_price_list = []
sell_day_list = []
sell_price_list = []

for i in range(len(day_list)):
    today_decision = decision_list[ i ]
    today_price = price_list[ i ]
    today_day = day_list[ i ]

    profit = 0

    if today_decision == "BUY" and have_stock == False:
        buy_value = today_price
        have_stock = True
        buy_day_list.append(today_day)
        buy_price_list.append(today_price)

    elif today_decision == "SELL" and have_stock == True:
        sell_value = today_price
        profit = sell_value - buy_value
        total_profit = total_profit + profit
        have_stock = False
        sell_day_list.append(today_day)
        sell_price_list.append(today_price)

    profit_list.append(profit)

with open("output_table.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Day", "Price", "Change%", "Decision", "Profit"])

    for i in range(len(day_list)):
        writer.writerow([
            day_list[ i ],
            price_list[ i ],
            change_list[ i ],
            decision_list[ i ],
            profit_list[ i ]
        ])

print("Trading Result")
print("-" * 45)
print("Day\tPrice\tChange%\tDecision\tProfit")

for i in range(len(day_list)):
    print(
        str(day_list[ i ]) + "\t" +
        str(price_list[ i ]) + "\t" +
        str(change_list[ i ]) + "\t" +
        str(decision_list[ i ]) + "\t\t" +
        str(profit_list[ i ])
    )

print("\nTotal Profit:", total_profit)
print("Output saved in output_table.csv")

plt.plot(day_list, price_list, marker="o", label="Price")
plt.scatter(buy_day_list, buy_price_list, marker="^", s=100, label="BUY")
plt.scatter(sell_day_list, sell_price_list, marker="v", s=100, label="SELL")
plt.title("Rule-Based Intelligent Trading Agent")
plt.xlabel("Day")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

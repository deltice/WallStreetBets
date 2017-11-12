import ita

client = ita.Account("kuo.yikai@gmail.com", "charlieisaweeb")

status = client.get_portfolio_status()
print(status.account_val)
print(status.buying_power)
print(status.cash)
print(status.annual_return)

open_trades = client.get_open_trades()

for open_trade in open_trades:
    print(open_trade.date_time)
    print(open_trade.description)
    print(open_trade.symbol)
    print(open_trade.quantity)
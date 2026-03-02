import yfinance as yf
import pprint

ticker = yf.Ticker("PNG.V")  # change symbol here

print("\n===== INFO =====")
pprint.pprint(ticker.info)

print("\n===== FAST INFO =====")
pprint.pprint(ticker.fast_info)

print("\n===== FINANCIALS =====")
print(ticker.financials)

print("\n===== BALANCE SHEET =====")
print(ticker.balance_sheet)

print("\n===== CASH FLOW =====")
print(ticker.cashflow)

print("\n===== EARNINGS =====")
print(ticker.earnings)

print("\n===== RECOMMENDATIONS =====")
print(ticker.recommendations)

print("\n===== ANALYST PRICE TARGET =====")
pprint.pprint(ticker.analyst_price_target)

print("\n===== CALENDAR =====")
print(ticker.calendar)
import discord
from discord.ext import commands
import yfinance as yf
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def format_number(value):
    if value is None:
        return "N/A"
    try:
        if abs(value) >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"
        elif abs(value) >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        else:
            return f"{value:.2f}"
    except:
        return "N/A"


def format_percent(value):
    if value is None:
        return "N/A"
    try:
        return f"{value * 100:.2f}%"
    except:
        return "N/A"


def calculate_trend(price, ma200, earnings_growth):
    try:
        if price > ma200 and earnings_growth and earnings_growth > 0:
            return "🟢 Bullish"
        elif price < ma200 and earnings_growth and earnings_growth < 0:
            return "🔴 Bearish"
        else:
            return "🟡 Neutral"
    except:
        return "N/A"

def calculate_peg(pe_ratio, earnings_growth):
    try:
        if pe_ratio is None or earnings_growth is None:
            return "N/A"

        # If growth is decimal (0.20), convert to percent (20)
        if -1 < earnings_growth < 1:
            growth_percent = earnings_growth * 100
        else:
            growth_percent = earnings_growth

        if growth_percent <= 0:
            return "N/A"

        peg = pe_ratio / growth_percent
        return round(peg, 2)

    except:
        return "N/A"

@bot.command()
async def watch(ctx, symbol: str):
    await ctx.send(f"Analyzing {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        fast = ticker.fast_info

        # Basic Info
        company_name = info.get("longName", "N/A")
        exchange = info.get("exchange", "N/A")
        market_cap = fast.get("marketCap")
        current_price = fast.get("lastPrice")

        # Valuation
        pe_ratio = info.get("trailingPE")
        earnings_growth = info.get("earningsGrowth")
        peg_ratio = calculate_peg(pe_ratio, earnings_growth)
        eps = info.get("trailingEps")

        # Balance Sheet
        total_cash = info.get("totalCash")
        total_debt = info.get("totalDebt")
        debt_to_equity = info.get("debtToEquity")
        current_ratio = info.get("currentRatio")
        quick_ratio = info.get("quickRatio")

        # Growth
        revenue = info.get("totalRevenue")
        earnings_growth = info.get("earningsGrowth")

        # Quality
        roe = info.get("returnOnEquity")

        # 52 Week
        week_high = fast.get("yearHigh")
        week_low = fast.get("yearLow")

        # 200-day Moving Average
        hist = ticker.history(period="1y")
        ma200 = hist["Close"].rolling(window=200).mean().iloc[-1]

        trend_signal = calculate_trend(current_price, ma200, earnings_growth)

        response = f"""
**{company_name}** ({symbol})
Exchange: {exchange}

📊 Market Data
• Market Cap: {format_number(market_cap)}
• Current Price: {format_number(current_price)}
• 52W High / Low: {format_number(week_high)} / {format_number(week_low)}
• P/E Ratio: {pe_ratio if pe_ratio else "N/A"}
• PEG Ratio: {peg_ratio if peg_ratio else "N/A"}
• EPS: {eps if eps else "N/A"}

📈 Growth & Quality
• Revenue: {format_number(revenue)}
• Earnings Growth: {format_percent(earnings_growth)}
• Return on Equity (ROE): {format_percent(roe)}

🏦 Balance Sheet
• Total Cash: {format_number(total_cash)}
• Total Debt: {format_number(total_debt)}
• Debt/Equity: {debt_to_equity if debt_to_equity else "N/A"}
• Current Ratio: {current_ratio if current_ratio else "N/A"}
• Quick Ratio: {quick_ratio if quick_ratio else "N/A"}

📡 Trend Signal: {trend_signal}
"""

        await ctx.send(response)

    except Exception as e:
        print(e)
        await ctx.send("Error retrieving data. Check ticker symbol.")


@bot.event
async def on_ready():
    print(f"TickerBot is live as {bot.user}")


# Adding Flask Web Server for Render
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Watcher is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# My Bot Login Should Use ENV Variable
import time

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")

while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        print("Bot crashed:", e)
        print("Sleeping for 60 seconds before retrying...")
        time.sleep(60)
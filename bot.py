import discord
from discord.ext import commands
import yfinance as yf
import pandas as pd
import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

# Load .env locally (Render ignores it, uses ENV vars)
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found")

# -------- Minimal HTTP Server for Render --------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"TickerBot is running")

def run_http():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()

threading.Thread(target=run_http, daemon=True).start()
# -------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- Utility Functions ----------------

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

# ---------------- Command ----------------

@bot.command()
async def watch(ctx, symbol: str):
    await ctx.send(f"Analyzing {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        fast = ticker.fast_info

        company_name = info.get("longName", "N/A")
        exchange = info.get("exchange", "N/A")
        market_cap = fast.get("marketCap")
        current_price = fast.get("lastPrice")

        pe_ratio = info.get("trailingPE")
        earnings_growth = info.get("earningsGrowth")
        peg_ratio = calculate_peg(pe_ratio, earnings_growth)
        eps = info.get("trailingEps")

        total_cash = info.get("totalCash")
        total_debt = info.get("totalDebt")
        debt_to_equity = info.get("debtToEquity")
        current_ratio = info.get("currentRatio")
        quick_ratio = info.get("quickRatio")

        revenue = info.get("totalRevenue")
        roe = info.get("returnOnEquity")

        week_high = fast.get("yearHigh")
        week_low = fast.get("yearLow")

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

# ---------------- Events ----------------

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# ---------------- Safe Run Loop ----------------

while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        print("Bot crashed:", e)
        print("Retrying in 300 seconds...")
        time.sleep(300)
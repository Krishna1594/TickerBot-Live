# 📈 TickerBot – Your Personal Stock Tracker Discord Bot

![10272116](https://github.com/user-attachments/assets/067a1a32-e55e-4405-9bc3-7dc03d442ca0)


TickerBot is a Discord bot that lets you track live stock prices, company fundamentals, and trend signals in real-time. Built with Python, yfinance, and discord.py, it’s perfect for small communities, investing groups, or personal tracking.

## 🚀 Features

Live stock price lookup for NASDAQ, TSX, BSE tickers

**Key company fundamentals:**

Market Cap, P/E, PEG ratio, EPS

Revenue, Earnings Growth, ROE

Debt/Equity, Cash, Current & Quick Ratio

52-week High/Low and 200-day moving average trend signal

Bullish / Bearish / Neutral indicators

24/7 uptime via Flask + cloud deployment

Easily configurable using .env for Discord token

Python-based, lightweight, and fast

## ⚙ Usage

**Command Prefix: !**

**Example:**

!watch AAPL

**Outputs:**

Analyzing AAPL...

**Apple Inc.** (AAPL)

Exchange: NASDAQ

Market Cap: 2.47T

Current Price: 158.34

52W High / Low: 180.50 / 125.60

P/E Ratio: 28.5

PEG Ratio: 1.8

EPS: 5.52

Revenue: 394.3B

Earnings Growth: 0.15%

Return on Equity (ROE): 32%

Total Cash: 50.3B

Total Debt: 110.2B

Debt/Equity: 1.2

Current Ratio: 1.36

Quick Ratio: 1.2

Trend Signal: 🟢 Bullish

## 🏗 Deployment (24/7)

To host 24/7:

Deploy on Render (or similar cloud service)

Add DISCORD_TOKEN in environment variables on Render

The bot uses Flask keep-alive to stay online 24/7

Push your repo to GitHub (do not commit .env)

## ⚡ Notes / Best Practices

Do not commit .env — your token is private

Small communities (~15 users) run fine on free-tier hosting

Use yfinance unofficial API — light and no rate limits

Optional: add caching for faster responses

## 📁 Project Structure
TickerBot-Live/
├── bot.py           # Main Python bot file
├── requirements.txt # Python dependencies
├── .gitignore       # Ignore .env and __pycache__
├── README.md
└── banner.png       # Optional Discord banner

Extra files such as 'metric.py' file will let you explore what other parameters Yahoo Finance is able to offer to include in your main code. (I did not want to make this output more clutered anymorer).

## 📌 Credits

discord.py
 – Discord bot framework

yfinance
 – Yahoo Finance API

Python 3.10+

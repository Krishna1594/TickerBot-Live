import os
import requests
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
FINNHUB_KEY = os.getenv("FINNHUB_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!watch"):
        args = message.content.split()

        if len(args) < 2:
            await message.channel.send("Usage: !watch TICKER")
            return

        symbol = args[1].upper()

        try:
            # Company profile
            profile = requests.get(
                f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={FINNHUB_KEY}"
            ).json()

            # Quote
            quote = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
            ).json()

            # Metrics
            metrics = requests.get(
                f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={FINNHUB_KEY}"
            ).json().get("metric", {})

            if not profile or quote.get("c") == 0:
                await message.channel.send("Invalid ticker or no data found.")
                return

            company_name = profile.get("name", "N/A")
            exchange = profile.get("exchange", "N/A")
            market_cap = metrics.get("marketCapitalization")
            pe_ratio = metrics.get("peBasicExclExtraTTM") or metrics.get("peTTM") or "N/A"
            eps = metrics.get("epsBasicExclExtraTTM") or metrics.get("epsTTM") or "N/A"
            peg_ratio = metrics.get("pegRatio") or "N/A"
            current_price = quote.get("c", "N/A")

            # Format Market Cap
            if market_cap:
                market_cap = f"${market_cap/1000:.2f}B"
            else:
                market_cap = "N/A"

            embed = discord.Embed(
                title=f"{company_name} ({symbol})",
                description=f"Listed on: {exchange}",
                color=discord.Color.blue()
            )

            embed.add_field(name="Current Price", value=f"${current_price}", inline=True)
            embed.add_field(name="Market Cap", value=market_cap, inline=True)
            embed.add_field(name="P/E (TTM)", value=str(pe_ratio), inline=True)
            embed.add_field(name="Basic EPS (TTM)", value=str(eps), inline=True)
            embed.add_field(name="PEG Ratio", value=str(peg_ratio), inline=True)

            embed.set_footer(text="TickerBot • Powered by Finnhub")

            await message.channel.send(embed=embed)

        except Exception:
            await message.channel.send("Error fetching stock data.")


bot.run(TOKEN)
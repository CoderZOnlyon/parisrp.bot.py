import discord

client = discord.Client()

@client.event
async def on_ready():
    print("bot prêt à l'usage")

client.run("OTAyODQ3MTg3ODU4MzU4MzIy.YXkX9w.aroj1pCz195Hb8afF_D5e3J7EVQ")
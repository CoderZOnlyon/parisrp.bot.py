import discord
from discord import emoji
from discord.ext import commands
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *

bot = commands.Bot(command_prefix = "#", description = "Bot de Onlyon")
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
	print("Ready !")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
    reason = "".join(reason)
    await ctx.guild.kick(user, reason = reason)
    await ctx.send(f"{user} à été expulsé")

@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def Info(ctx):
    await ctx.send("**Coucou** ! Je suis le bot de Onlyon ! Mon site internet : https://discordon-00.webselfsite.net/ ajoute moi la-bas !")

@bot.command()
async def serverInfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

@bot.command()
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)

@bot.command()
async def kiss(ctx, member : discord.Member):
	await ctx.send(f"Vous avez embrassé {member.mention} https://tenor.com/view/beyhadh2-mayra-jennifer-winget-shivin-narang-shivjen-gif-22189873 !")

@bot.command()
async def punch(ctx, member : discord.Member):
	await ctx.send(f"Vous avez donner un coup de poing à {member.mention} ! Bien joué soldat ! https://tenor.com/view/jinzhan-lily-and-marigold-lili-punching-punch-gif-14583039")

@bot.command()
async def mariage(ctx, member : discord.Member):
	await ctx.send(f"{member.mention} vous êtes demandé en mariage ! Faites #yes ou #no pour accepter la demande de mariage !")

@bot.command()
async def yes(ctx, member : discord.Member):
    await ctx.send(f"{member.mention} votre demande de mariage à été accepté !")

@bot.command()
async def no(ctx, member : discord.Member):
    await ctx.send(f"{member.mention} votre demande de mariage à été refusé !")

@bot.command()
async def help2(ctx):
    buttons = [
        create_button(
            style=ButtonStyle.blue,
            label="Modération",
            custom_id="oui"
        ),
        create_button(
            style=ButtonStyle.danger,
            label="Autre",
            custom_id="non"
        )
    ]
    action_row = create_actionrow(*buttons)
    fait_choix = await ctx.send("Help, Mon préfix est **#** !", components=[action_row])

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

    button_ctx = await wait_for_component(bot, components=action_row, check=check)
    if button_ctx.custom_id == "oui":
        await button_ctx.edit_origin(content= "__Commandes modération :__ ban (#ban [user] [raison]) / unban (#unban [userid]) / mute (#mute [user] [raison]) / unmute (#unmute [user] [raison]) / kick (#kick [user] [raison]) / clear (#clear [nombre])")
    else:
        await button_ctx.edit_origin(content="__Commandes Autre :__ kiss (#kiss [user]) / punch (#punch [user]) / mariage (#mariage [user]) / print (#print [message]) / Info (#Info) / ServerInfo (#serverInfo) / help (#help2) / ping (#ping)")


bot.run("OTAyODQ3MTg3ODU4MzU4MzIy.YXkX9w.jJ48i--nsYAOdbjUcBVeVi3aZh8")
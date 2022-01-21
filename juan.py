import discord
from discord.ext import commands
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
from os import system
import subprocess as sp
import shlex
import random
import asyncio
import pickle
import time
import asyncpraw
import re
from hentai import Utils, Sort, Option, Tag, Hentai
from pathlib import Path
import sys

reddit = asyncpraw.Reddit(client_id="dB_ham309t2MZhMKNibzDA", client_secret="7YT-RgeSuEaCArx4mzPDG3bUjtsrSg", username="juanMan34", password="JuanTheDiscordHorse1234", user_agent="juan")

class AllBot(commands.Bot):
	async def process_commands(self, message):
		ctx = await self.get_context(message)
		await self.invoke(ctx)

	async def get_context(self, message, *, cls=discord.ext.commands.context.Context):
		view = discord.ext.commands.view.StringView(message.content)
		ctx = cls(prefix=None, view=view, bot=self, message=message)

		prefix = await self.get_prefix(message)
		invoked_prefix = prefix

		if isinstance(prefix, str):
			if not view.skip_string(prefix):
				return ctx
		else:
			try:
				if message.content.startswith(tuple(prefix)):
					invoked_prefix = discord.utils.find(view.skip_string, prefix)
				else:
					return ctx

			except TypeError:
				if not isinstance(prefix, list):
					raise TypeError("get_prefix must return either a string or a list of string, "
							"not {}".format(prefix.__class__.__name__))

				for value in prefix:
					if not isinstance(value, str):
						raise TypeError("Iterable command_prefix or list returned from get_prefix must "
							"contain only strings, not {}".format(value.__class__.__name__))
				raise

		if self.strip_after_prefix:
			view.skip_ws()

		invoker = view.get_word()
		ctx.invoked_with = invoker
		ctx.prefix = invoked_prefix
		ctx.command = self.all_commands.get(invoker)
		return ctx


prefix = "j!"
client = AllBot(command_prefix=prefix)
dictionary = PyDictionary()
lastCommand = "echo No last command saved"
horsebirths = pickle.load(open("horsebirth.dat", "rb"))

commandStatus = ["p", "l", "lt"]

@client.event
async def on_ready():
	global queue
	system("mkdir pythonFiles")
	print("KONO DIO DA")


@client.command(aliases=['hb', 'birth'])
async def horsebirth(ctx):
	global horsebirths
	i = 1
	count = 1
	horseMessage = ""
	horses = []
	while i != 17:
		emoji = discord.utils.get(client.emojis, name=f'horse{i}')
		horses.append(str(emoji))
		i = i + 1
	while len(horses) > 0:
		num = random.randint(0, (len(horses)-1))
		if (count % 4) == 0:
			horseMessage = horseMessage + horses[num] + "\n"
		else:
			horseMessage = horseMessage + horses[num]
		horses.pop(num)
		count = count + 1
	await ctx.send(horseMessage)
	horsebirths = horsebirths + 16
	pickle.dump(horsebirths, open("horsebirth.dat", "wb"))
	await ctx.send(f"Total Horse births: {horsebirths}")


@client.command(aliases=['asearch', 'as'])
async def animesearch(ctx, *, query):

	search = query.replace(" ", "+")
	search = f"//search.html?keyword={search}"

	url = f"https://gogoanime.vc"
	searchUrl = url + search

	r = requests.get(searchUrl)

	soup = BeautifulSoup(r.content, 'html.parser')


	animes = soup.select(".name a")
	if len(animes) != 0:

		i = 0
		searchList = "Search Results:"
		while i != len(animes):
			searchList = searchList + (f"\n{i + 1}) {(animes[i])['title']}")
			i = i + 1
		await ctx.send(searchList)

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel
		try:
			msg = await client.wait_for("message", check=check, timeout=30)
		except asyncio.TimeoutError:
			await ctx.send("Search Timeout")

		msg = str(msg.content)
		try:
			ans = int(msg)
			link = (f"{url}{(animes[ans - 1])['href']}")
			anime = requests.get(link)
			soup2 = BeautifulSoup(anime.content, 'html.parser')
			enName = soup2.select_one(".anime_info_body_bg h1")
			enName = str(enName)
			enName = enName.replace("<h1>", "")
			enName = enName.replace("</h1>", "")



			aniInfo = soup2.select(".type a")

			aniType = soup2.select_one(".type a")
			aniType = aniType['title']

			desc = soup2.select(".type")

			description = str(desc[1])
			description = description.replace("<p class=\"type\"><span>Plot Summary: </span>", "")
			description = description.replace("</p>", "")

			otherName = str(desc[len(desc)-1])
			otherName = otherName.replace("<p class=\"type\"><span>Other name: </span>", "")
			otherName = otherName.replace("</p>", "")

			genres = []
			i = 1
			while i != (len(aniInfo)-1):
				genres.append((aniInfo[i])['title'])
				i = i + 1

			genres = ", ".join(genres)

			status = (aniInfo[len(aniInfo) - 1])['title']
			status = status.replace(" Anime", "")
			coverImage = soup2.select_one(".anime_info_body_bg img")
			coverImage = coverImage['src']
			coverPart = discord.Embed(title="", description="", color=discord.Color.blue())
			coverPart.set_image(url=coverImage)
			await ctx.send(embed=coverPart)

			field1 = f"**Type**: {aniType}\n**Status**: {status}\n**Genres**: {genres}\n**Aliases**: {otherName}"
			embed = discord.Embed(title=enName, description=description, color=discord.Color.blue())
			embed.add_field(name="----------------", value=field1, inline=True)
			await ctx.send(embed=embed)

		except ValueError:
			await ctx.send("Search Selection Error")
	else:
		await ctx.send(f"No results found for {query}")

@client.command(aliases=['ranime', 'ra'])
async def randomanime(ctx):
	url = "https://9anime.to/random"

	r = requests.get(url)

	soup = BeautifulSoup(r.content, 'html.parser')


	#Anime Name
	animeName = soup.select_one(".title")
	animeName = str(animeName)
	animeName = animeName.replace("<h1 class=\"title\" data-jtitle=\"", "JP: ", 1)
	animeName = animeName.replace("<h1 class=\"title\" data-jtitle=\'", "JP: ", 1)
	animeName = animeName.replace("\" itemprop=\"name\">", "\nEN: ")
	animeName = animeName.replace("\' itemprop=\"name\">", "\nEN: ")
	animeName = animeName.replace("</h1>", "")

	#Name Alias
	aliases = soup.select_one(".alias")
	aliases = str(aliases)
	aliases = aliases.replace("<div class=\"alias\">", "Alt. Names: ")
	aliases = aliases.replace("</div>", "")


	#Description
	description = soup.select_one("p", itemprop="description")
	description = str(description)
	description = description.replace("<p class=\"shorting\" itemprop=\"description\">", "")
	description = description.replace("</p>", "")


	#Column 1
	info = soup.select_one(".col1")
	info = str(info)

	#Column 2
	info2 = soup.select_one(".col2")
	info2 = str(info2)


	#Production Studio
	studioX = (info.find("title") + 7)
	studioY = (info.find("\"", (studioX)))
	studio = info[studioX:studioY]


	#Type
	aniTypeX = (info.find("Type:") + 22)
	aniTypeY = (info.find("\"", aniTypeX))
	aniType = info[aniTypeX:aniTypeY].capitalize()


	#Date Aired
	dateX = (info.find("Date aired:") + 19)
	dateY = (info.find("<", dateX))
	date = info[dateX:dateY]


	#Status
	statusX = (info.find("Status: ") + 14)
	statusY = (info.find("<", statusX))
	status = info[statusX:statusY]

	#Genres
	str1 = info
	substr = "https://9anime.to/genre/"
	genreListNum = [i for i in range(len(str1)) if str1.startswith(substr, i)]
	i = 0
	genrelist = []
	while i != len(genreListNum):
		genreX = (genreListNum[i] + 24)
		genreY = (info.find('\"', genreX))
		genrelist.append(info[genreX:genreY].capitalize())
		i = i + 1

	genres = (', '.join(genrelist))


	#Score
	scoreX = (info2.find("Scores: ") + 14)
	scoreY = (info2.find("/", scoreX) - 1)
	votesX = (scoreY + 3)
	votesY = (info2.find("<", votesX))
	score = (f"{info2[scoreX:scoreY]} / 10 ({info2[votesX:votesY]} users)")


	#Duration
	timeX = (info2.find("Duration: ") + 16)
	timeY = (info2.find("<", timeX))
	duration = info2[timeX:timeY]


	#Cover Image
	coverImage = soup.select_one('img', itemprop="image")
	coverImage = coverImage['src']
	field1 = f"**Type**: {aniType}\n**Studio**: {studio}\n**Genres**: {genres}\n**Aliases**: {aliases}"
	field2 = f"**Date Aired**: {date}\n**Status**: {status}\n**Score**: {score}\n**Duration**: {duration}"
	coverPart = discord.Embed(title="", description="", color=discord.Color.blue())
	coverPart.set_image(url=coverImage)
	await ctx.send(embed=coverPart)
	embed = discord.Embed(title=animeName, description=description, color=discord.Color.blue())
	embed.add_field(name="----------------", value=field1, inline=True)
	embed.add_field(name="----------------", value=field2, inline=True)
	await ctx.send(embed=embed)


@client.command(aliases=["wiki"])
async def wikipedia(ctx, search, subtopic="naice"):
	try:
		search = search.replace("_", "+")


		searchUrl = f"https://en.wikipedia.org/w/index.php?search={search}&title=Special:Search&fulltext=1&ns0=1"

		rs = requests.get(searchUrl)

		soup1 = BeautifulSoup(rs.content, 'html.parser')

		results = soup1.select(".mw-search-result-heading a")
		    # rip it out

		result1 = results[0]['href']
		result1 = str(result1)


		url = f"https://www.wikipedia.org{result1}"

		r = requests.get(url)

		soup = BeautifulSoup(r.content, 'html.parser')

		

		name = soup.find("h1", {"class":"firstHeading"})
		name = str(name)
		name = name.replace("<h1 class=\"firstHeading\" id=\"firstHeading\">", "")
		name = name.replace("</h1>", "")

		cleanr = re.compile('<.*?>')
		cleantext1 = re.sub(cleanr, '', name)
		name = cleantext1
		try:
			try:
				try:
					image = soup.select(".infobox-full-data img")
					image = str((image[0])['src'])
				except:
					image = soup.select(".infobox-image img")
					image = str((image[0])['src'])
			except:
				image = soup.select(".thumb img")
				image = str((image[0])['src'])
		except:
			image = "//cdn.jsdelivr.net/npm/twemoji@11.0.1/2/svg/1f434.svg"

		try:
			for div in soup.find_all("div", {'class':'sidebar-list-content'}):
				div.decompose()
		except:
			pass

		try:
			for p in soup.find_all("p", {'class':'mw-empty-elt'}):
				p.decompose()
		except:
			pass

		texts = soup.select("#mw-content-text p")


		texts = [str(i) for i in texts]
		while "<None></None>" in texts:
			texts.remove("<None></None>")

		if subtopic == "naice":
			if len(str(texts[0])) < 400:
				text = str(texts[0]) + str(texts[1])
			else:
				text = str(texts[0])
		else:
			try:
				subtopic = int(subtopic)
				if subtopic >= len(texts):
					subtopic = len(texts)
			except:
				subtopic = 1
			text = str(texts[(subtopic)])




		text = text.replace("<a", "_<a href=")
		text = text.replace("</a>", "</a>_ ")
		

		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', text)
		text = cleantext

		
		await ctx.send(f"https:{image}")
		await ctx.send(f"**{name}**\n{text}"[:2000])
	except IndexError:
		await ctx.send("¯\\_(ツ)_/¯")

@client.command(aliases=["m"])
async def mat(ctx, x, y, typeOf="origin", write="r", file="plot", fileName="graph"):
	if typeOf == "origin":
		codePlus = "pt.axvline(x=0, c=\"black\")\npt.axhline(y=0, c=\"black\")"
	else:
		codePlus = ""

	code = "from os import system\nimport math\nfrom matplotlib import pyplot as pt\nimport numpy as np\ndef write(text):\n    system(f\"echo {text}\")\n\nx = " + x + "\ny = " + y + "\npt.plot(x, y)\n" + codePlus + "\npt.savefig(\"" + file + ".png\", dpi=600, bbox_inches=\"tight\")"
	code = code.replace('\n', '\\n')
	writeFunc = 0
	if write == "save":
		writeFunc = ">"
	elif write == "append":
		writeFunc = ">>"
	else:
		write = "r"
		writeFunc = ">"
	command = f"cd pythonFiles;printf \'{code}\' {writeFunc} {fileName}.py;python3 {fileName}.py"
	output = sp.getoutput(command)
	try:
		if len(output) > 2000:
			iterations = round((len(output) / 2000))
			await ctx.send(output[:2000])
			i = 0
			while i != iterations:
				if "p" in commandStatus:
						i = i + 1
						await ctx.send(output[(2000 * i):(2000 * (i + 1))])
				else:
					pass
		else:
			await ctx.send(output[:2000])
	except:
		pass

	await ctx.send(file=discord.File(f'pythonFiles/{file}.png'))

@client.command(aliases=["f"])
async def file(ctx, name):
	fileObject = ctx.message.attachments[0]
	await fileObject.save(fp=name)

@client.command(aliases=["p"])
async def python(ctx, linuxType, write, fileName, *, code):
	global commandStatus
	linuxlist = ['l', 'lt']
	code = "from os import system\ndef write(text):\n    system(f\"echo {text}\")\n\n" + code
	code = code.replace('\n', '\\n')
	writeFunc = 0
	if write == "save":
		writeFunc = ">"
	elif write == "append":
		writeFunc = ">>"
	else:
		write = "r"
		writeFunc = ">"
	command = f"cd pythonFiles;printf \'{code}\' {writeFunc} {fileName}.py;python3 {fileName}.py"
	if linuxType == 'l':
		start_time1 = time.time()
		output = sp.getoutput(command)
		finish_time1 = time.time() - start_time1
		try:
			start_time2 = time.time()
			if len(output) > 2000:
				iterations = round((len(output) / 2000))
				await ctx.send(output[:2000])
				i = 0
				while i != iterations:
					if "p" in commandStatus:
							i = i + 1
							await ctx.send(output[(2000 * i):(2000 * (i + 1))])
					else:
						pass
			else:
				await ctx.send(output[:2000])
		except:
			await ctx.send(":horse:")
		finish_time2 = time.time() - start_time2
		await ctx.send(f"Time of command execution: {(str(finish_time1))[:6]} seconds\nTime of output display: {(str(finish_time2))[:6]} seconds")
		await ctx.send(":horse:")

	elif linuxType == "lt":
		global lastCommand
		errOutput = ["", " "]
		if str(ctx.author.id):
			process = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8', shell=True)
			while "p" in commandStatus:
				output = process.stdout.readline()
				if output == '' and process.poll() is not None:
					break
				if output:
					if output.isspace() == False:
						await ctx.send(f"{output.strip()}")
					else:
						await ctx.send(f"_{output.strip()}")
			lastCommand = command
			await ctx.send(":horse:")
			rc = process.poll()
			#return rc	

	else:
		await ctx.send("Unidentified Command Type")

	if linuxType in linuxlist and write == "r":
			system(f"cd pythonFiles;rm {fileName}.py")

@client.command()
async def recc(ctx, startingPoint="random"):
	if startingPoint == "random":
		limit = str(random.randint(0, 2000))
	else:
		try:
			limit = int(startingPoint)
			limit = str(limit)
		except ValueError:
			limit = str(random.randint(0, 2000))

	r2 = requests.get(f"https://myanimelist.net/topanime.php?limit={limit}")

	soup2 = BeautifulSoup(r2.content, 'html.parser')

	names = soup2.select(".anime_ranking_h3")

	oneSelection = random.choice(names)
	oneSelection = str(oneSelection)
	

	oneX = (oneSelection.find("href=\"") + 6)
	oneY = (oneSelection.find("\"", (oneX)))
	url = oneSelection[oneX:oneY]


	r = requests.get(url)

	soup = BeautifulSoup(r.content, 'html.parser')

	name = str(soup.select_one(".title-name strong"))
	engName = str(soup.select_one(".title-english"))

	cleanr = re.compile('<.*?>')
	cleantext1 = re.sub(cleanr, '', name)
	name = cleantext1

	cleantext1 = re.sub(cleanr, '', engName)
	engName = cleantext1

	rank = str(soup.select_one(".ranked strong"))
	cleantext1 = re.sub(cleanr, '', rank)
	rank = cleantext1


	description = soup.select_one(".js-scrollfix-bottom-rel p", itemprop="description")
	description = str(description)
	description = description.replace("<p itemprop=\"description\">", "")
	description = description.replace("</p>", "")
	description = description.replace("<br/>", "")
	description = description.replace("<i>", "*")
	description = description.replace("</i>", "*")
	#I LEFT HERE (try detecting child of <a href=animename/pics>)
	table = soup.select_one(".borderClass")
	coverImage = table.select_one("img")
	coverImage = coverImage['data-src']

	embed = discord.Embed(color=discord.Colour.blue())
	embed.set_image(url=coverImage)
	await ctx.send(embed=embed)
	name = f"{name}\n**{engName}**"
	embed2 = discord.Embed(title=name, description=description, color=discord.Colour.blue())
	embed2.set_footer(text=f"Ranked {rank}")
	await ctx.send(embed=embed2)

@client.command()
async def cat(ctx):
	url = "https://www.randomkittengenerator.com/"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	cat = soup.select_one(".hot-random-image")
	cat = cat["src"]
	embed = discord.Embed(color=discord.Colour.red())
	embed.set_image(url=cat)
	await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
	await ctx.send(f'Neigh! {round(client.latency * 1000)}ms')

'''@client.command(aliases=['mpos', 'mp'])
async def mousepos(ctx, x, y):
	try:
		x = int(x)
		y = int(y)
		mouse.position = (x, y)
		await ctx.send('Done.')
	except ValueError:
		await ctx.send("Invalid Arguments.")'''

@client.command(aliases=['last'])
async def runLastCommandWithError(ctx):
	global lastCommand
	if str(ctx.author.id):
		output = sp.getoutput(lastCommand)
		try:
			await ctx.send(output)
			await ctx.send(":horse:")
		except:
			await ctx.send(":horse:")


@client.command(aliases=['l'])
async def linux(ctx, *, sysCommand):
	start_time1 = time.time()
	output = sp.getoutput(sysCommand)
	finish_time1 = time.time() - start_time1
	if str(ctx.author.id):
		start_time2 = time.time()
		try:
			if len(output) > 2000:
				iterations = round((len(output) / 2000))
				await ctx.send(output[:2000])
				i = 0
				while i != iterations:
					if "l" in commandStatus:
							i = i + 1
							await ctx.send(output[(2000 * i):(2000 * (i + 1))])
					else:
						pass
			else:
				await ctx.send(output[:2000])


		except:
			await ctx.send(":horse:")
		finish_time2 = time.time() - start_time2
		await ctx.send(f"Time of command execution: {(str(finish_time1))[:6]} seconds\nTime of output display: {(str(finish_time2))[:6]} seconds")
		await ctx.send(":horse:")




@client.command(aliases=['r'])
async def redditGet(ctx, subred, typeSub="top", num="random"):
	try:
		subr = await reddit.subreddit(subred, fetch=True)
		if num != "random":
			try:
				num = int(num)
				
			except:
				num = 0
			all_subs = []
			if typeSub == "top":
				top = subr.top(limit=(num + 2))
			elif typeSub == "hot":
				top = subr.hot(limit=(num + 2))
			elif typeSub == "new":
				top = subr.new(limit=(num + 2))
			else:
				top = subr.top(limit=(num + 2))

			async for submission in top:
				all_subs.append(submission)


			sub = all_subs[num]
		else:
			sub = await subr.random()
		name = sub.title
		url = sub.url



		if "youtu.be" in url:
			url = url.replace("youtu.be/", "youtube.com/watch?v=")
		elif "&feature=share" in url:
			url = url.replace("&feature=share", "")

		#em = discord.Embed(title=name, description="", color=discord.Color.blue())
		#em.set_image(url=url)
		if ctx.channel.nsfw and subr.over18:
			await ctx.send(f"**{name}**\n{url}")
		elif not subr.over18:
			await ctx.send(f"**{name}**\n{url}")
		else:
			await ctx.send("Not an Nsfw channel")
	except:
		await ctx.send("Non-existent Subreddit")


@client.command(aliases=["lt"])
async def linuxTime(ctx, *, sysCommand):
	global lastCommand
	errOutput = ["", " "]
	if str(ctx.author.id):
		
		process = sp.Popen(sysCommand, stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8', shell=True)
		while "lt" in commandStatus:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				if output.isspace() == False:
					await ctx.send(f"{output.strip()}")
				else:
					await ctx.send(f"_{output.strip()}")

			
		lastCommand = sysCommand
		await ctx.send(":horse:")
		rc = process.poll()
		return rc
		



@client.command(aliases=['dic', 'd'])
async def meaningofword(ctx, word):
	wordDecap = word.lower()
	wordMeaning = dictionary.meaning(wordDecap)
	speechPartInDict = list(wordMeaning.keys())
	speechPart = speechPartInDict[0]

	if len(wordMeaning) == 2:
		speechPart2 = speechPartInDict[1]
		await ctx.send(f"{word} **({speechPart})**: {wordMeaning[speechPart]}"[:2000])
		await ctx.send(f"{word} **({speechPart2})**: {wordMeaning[speechPart2]}"[:2000])

	elif len(wordMeaning) == 3:
		speechPart2 = speechPartInDict[1]
		speechPart3 = speechPartInDict[2]
		await ctx.send(f"{word} **({speechPart})**: {wordMeaning[speechPart]}"[:2000])
		await ctx.send(f"{word} **({speechPart2})**: {wordMeaning[speechPart2]}"[:2000])
		await ctx.send(f"{word} **({speechPart3})**: {wordMeaning[speechPart2]}"[:2000])

	elif len(wordMeaning) == 1:
		await ctx.send(f"{word} **({speechPart})**: {wordMeaning[speechPart]}"[:2000])
	else:
		await ctx.send(f"{word}: {wordMeaning}")

@client.command(aliases=['img', 'iSearch'])
async def imageSearch(ctx, search, num='r'):
	try:
		search = str(search)
		search = search.replace(" ", "+")
		channel_nsfw = ctx.channel.is_nsfw()
		url = f"https://search.aol.com/aol/image;?q={search}"
		if channel_nsfw:
			url = url + "&save=o"

		randomImg = requests.get(url)

		soup = BeautifulSoup(randomImg.content, 'html.parser')


		images = soup.select("img")
		if num == "r":
			if len(images) < 40:
				last = len(images)
			else:
				last = 40
			num = random.randint(1, last)
			if (num%2) == 0:
				num = num + 1
			
			source = (images[num])['src']
		else:
			try:
				num = int(num)
				if (num%2) == 0:
					num = num + 1
			except ValueError:
				num = 1
			source = (images[num])['src']
		source = str(source)
		source = source.replace("w=300&h=300", "w=800&h=800")
		await ctx.send(source)
	except:

		await ctx.send("Search went wrong")


@client.command(aliases=['vid'])
async def videosend(ctx, fileName):
	await ctx.send(file=discord.File(fileName))


@client.command()
async def bracket(ctx, *, members):
	memberlist = members.split(', ')
	order = []
	length = len(memberlist)
	for i in range(length):
		item = random.choice(memberlist)
		order.append(item)
		memberlist.remove(item)

	bracket = ""

	if len(order)%2 == 0:
		midround = int((len(order) - 4)/2)

		bracket = f"`{order[0]} vs {order[1]}`\n :arrow_down: \n"
		order.pop(0)
		order.pop(0)
		for i in range(midround):
			bracket = bracket + f"`?? vs {order[0]}`\n :arrow_down: \n"
			order.pop(0)
		bracket = bracket + " `Finals`\n :arrow_up: \n"
		for i in range(midround):
			bracket = bracket + f"`?? vs {order[0]}`\n :arrow_up: \n"
			order.pop(0)
		bracket = bracket + f"`{order[0]} vs {order[1]}`"

	else:
		midround = int((len(order) - 5)/2)
		bracket = f"`{order[0]} vs {order[1]}`\n :arrow_down: \n"
		order.pop(0)
		order.pop(0)
		for i in range(midround + 1):
			bracket = bracket + f"`?? vs {order[0]}`\n :arrow_down: \n"
			order.pop(0)
		bracket = bracket + " `Finals`\n :arrow_up: \n"
		for i in range(midround):
			bracket = bracket + f"`?? vs {order[0]}`\n :arrow_up: \n"
			order.pop(0)
		bracket = bracket + f"`{order[0]} vs {order[1]}`"

	await ctx.send(bracket)



@client.command(aliases=["j"])
async def join(ctx):
	if not ctx.message.author.voice:
		await ctx.send("You are not connected to a voice channel")
		return
	else:
		channel = ctx.message.author.voice.channel

	await channel.connect()

@client.command()
async def play(ctx, file):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		await ctx.send("Playing something right now.")
	else:
		voice.play(discord.FFmpegPCMAudio(file))

@client.command(aliases=["ps"])
async def playsound(ctx, search, num="1"):
	search = search.replace("_", "+")
	url = f"https://www.myinstants.com/search/?name={search}"
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	try:
		link = soup.select(".small-button")
		num = int(num)
		link = link[(num - 1)]
		link = str(link)
		link = link.replace("<div class=\"small-button\" onmousedown=\"play(\'", "")
		link = link.replace("\')\"></div>", "")
		link = "https://www.myinstants.com" + link
		system(f"wget -O {search} {link}")
		await ctx.invoke(client.get_command('play'), file=search)
	except:
		await ctx.send("Didnt find anything, Retard")



@client.command()
async def leave(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_connected():
		await voice.disconnect()
	else:
		await ctx.send("Not Connected")


@client.command()
async def pause(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		await ctx.send("Not Playing Anything")

@client.command()
async def resume(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		await ctx.send("Not Paused")

@client.command()
async def stopMusic(ctx):
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	voice.stop()



@client.command(aliases=['lo'])
async def linuxWithoutOutput(ctx, *, command):
	start_time1 = time.time()
	system(command)
	finish_time1 = time.time() - start_time1
	await ctx.send(f"Time of command execution: {finish_time1} seconds")
	await ctx.send(":horse:")

@client.command()
async def nh(ctx):
	doujin = Hentai(Utils.get_random_id())
	await ctx.send(f"**{doujin.title()}**")
	for i in doujin.image_urls:
		await ctx.send(i)


@client.command(aliases=['e'])
async def emoji(ctx, ej, am="1"):
	try:
		am = int(am)
		if am > 5:
			am = 5
	except:
		am = 1
	role = discord.utils.get(ctx.guild.roles, name="Horse")
	emoji = discord.utils.get(client.emojis, name=ej)
	try:
		tempWebHook = await ctx.channel.create_webhook(name=ctx.author.display_name)
		
		if role in ctx.author.roles:
			for i in range(am):
				await tempWebHook.send(emoji, avatar_url=ctx.author.avatar_url)
			await tempWebHook.delete()
		else:
			await tempWebHook.send(emoji, avatar_url=ctx.author.avatar_url)
			await tempWebHook.delete()
	except:
		if role in ctx.author.roles:
			for i in range(am):
				await ctx.send(emoji)
		else:
			await ctx.send(emoji)


@client.command(aliases=['8ball'])
async def _8Ball(ctx, *, question):
	responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes -- definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful.",
"Your mom.",
"Bruh",
"Why would you want to know that?",
"Bitch, I dont have time for this shit",
"Answer that yourself bitch"]
	await ctx.send(random.choice(responses))



client.run(sys.argv[1])
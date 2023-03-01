import discord
from discord.ext import commands

class HelpSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['parancsok'], invoke_without_command=True, pass_context=True)
    async def help(self, ctx):
        embed=discord.Embed(
            title='Parancsok',
            description=None,
            color=0x8a7c74
        )
        embed.set_thumbnail(
            url=str(self.bot.user.avatar_url)[:-15]
        )
        embed.set_footer(
            text='A parancsokról bővebb segítségért: !pb help <parancs neve>'
        )
        embed.add_field(
            name='FONTOS!',
            value='Ha egy parancs nevet kér vagy bármilyen bemenetet ami igényel szóközt, azt mindig kettő \" közé írd.'
                '\nPéldául: !pb teszt \"Ez egy teszt bemenet\"'
                '\n\nTovábbi parnacsok használata: `!pb tesztparancs` `továbbiparancs`',
            inline=False
        )
        embed.add_field(
            name='Elérhetőség/Visszajelzés',
            value='skydeszka.bots@gmail.com'
        )
        embed.add_field(
            name='A bot hivatalos Discord szervere',
            value='https://discord.gg/7r6Dsag8nF',
            inline=False
        )
        embed.add_field(
            name='Bot Információi',
            value='`invite`',
            inline=False
        )
        embed.add_field(
            name='Prefixum',
            value='Minden parancs elé a \"**!pb**\" prefixumot használd!',
            inline=False
        )
        embed.add_field(
            name='\n'
                '\n'
                '====================',
            value='====================',
            inline=False
        )
        embed.add_field(
            name='Általános parancsok',
            value='`help` '
                '`adatlap` '
                '`bolt` '
                '`kártya` '
                '`invite` '
                '`season` '
                '`code` '
                '`booster`',
            inline=False
        )
        embed.add_field(
            name='Bank parancsok',
            value='`egyenleg` '
                  '`fizet` '
                  '`kamat` '
        )
        embed.add_field(
            name='Munka parancsok',
            value='`munka` '
                  '`túlóra` '
                  '`lop` '
                  '`segély`',
            inline=False
        )
        embed.add_field(
            name='Kaszinó parancsok',
            value='`slotmachine` '
                  '`lotto` '
                  '`roulette` '
                  '`blackjack`',
            inline=False
        )
        embed.add_field(
            name='Fun parancsok',
            value='`gazdagság` '
                  '`rnjesus` '
                  '`lecsap` '
                  '`kifoszt` '
                  '`kereszt`'
        )
        if str(ctx.message.channel.type) != 'private':
            if ctx.author.guild_permissions.administrator:
                embed.add_field(
                    name='Admin parancsok',
                    value='`clear` '
                        '`kick` '
                        '`ban` '
                        '`mute` '
                          '`unmute` '
                        '`adminfizet` '
                        '`pcreset` '
                          '`rang` '
                          '`rang-info`',
                        inline=False
                )
            if ctx.author ==ctx.guild.owner:
                embed.add_field(
                    name='Szerver konfigurálása',
                    value='Ezeket a parancsokat adminisztrátor joggal is lehet használni.'
                        '\n`shop` '
                        '`ppreward` '
                        '`season (egyes funkciói)` '
                        '`channel` '
                        '`role` '
                        '`fixserver`',
                    inline=False
                )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['unmute'])
    async  def hunmute(self, ctx):
        embed = discord.Embed(
            title='Unmute - részletek',
            description='Vedd le a némítást egy tagról.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb unmute <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['rang-info', 'ranginfo'])
    async def hranginfo(self, ctx):
        embed = discord.Embed(
            title='Rang-információ - részletek',
            description='Nézd meg egy rang információit.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rang-info <@rang>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['blackjack'])
    async def hblackjack(self, ctx):
        embed = discord.Embed(
            title='BlackJack - részletek',
            description='Szerencse vagy tapasztalat? Próbáld meg',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb blackjack <tét>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )
        embed.add_field(
            name='Játékmenet',
            value='Miután elkezdted a játékot, a bot kiírja a te és az ellenfeled kártyáit.\n'
                  'A lényeg, hogy kevesebb, mint 21, de több mint az ellenfeled pontot gyűjts össze.\n'
                  'Miután látod a kártyáidat 3 opciód van, amit a chatbe kell simán írnod:\n'
                  '`hit` - felveszel mégegy kártyát\n'
                  '`double down` - megduplázod a téted, felveszel egy kártyát és vége a játéknak\n'
                  '`stand` - befejezed a játékot',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, aliases=['kamat'])
    async def hkamat(self, ctx):
        embed = discord.Embed(
            title='Kamat - részletek',
            description='Nézd meg az egyenleged a kamat számládon..',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kamat',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`nyit` '
                  '`berak` '
                  '`kivesz`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @hkamat.command(aliases=['kivesz'])
    async def hkivesz(self, ctx):
        embed = discord.Embed(
            title='Kamat - Kivesz - részletek',
            description='Vedd ki a kívánt összeget a számláról.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kamat kivesz <összeg>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @hkamat.command(aliases=['berak'])
    async def hberak(self, ctx):
        embed = discord.Embed(
            title='Kamat - Berak - részletek',
            description='Rakd be a kívánt mennyiséget a számládra.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kamat berak <összeg>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @hkamat.command(aliases=['nyit'])
    async def hnyit(self, ctx):
        embed = discord.Embed(
            title='Kamat - Nyit - részletek',
            description='Nyiss egy kamat számlát.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kamat nyit <kezdőösszeg>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, aliases=['rang'])
    async def hrang(self, ctx):
        embed = discord.Embed(
            title='Rang szerkesztés - részletek',
            description='Adj vagy vegyél el rangot tagoktól.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rang',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`ad` '
                  '`elvesz`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @hrang.command(aliases=['ad'])
    async def had(self, ctx):
        embed = discord.Embed(
            title='Rang szerkesztés - Ad - részletek',
            description='Adj rangot egy tagnak.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rang ad <@tag> <@rang> "indok"',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @hrang.command(aliases=['elvesz'])
    async def helvesz(self, ctx):
        embed = discord.Embed(
            title='Rang szerkesztés - Elvesz - részletek',
            description='Vegyél el rangot egy tagtól.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rang elvesz <@tag> <@rang> "indok"',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def pcreset(self, ctx):
        embed = discord.Embed(
            title='PlanCoin reset - részletek',
            description='Lenullázza minden tag egyenlegét.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb pcreset',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['booster'])
    async def boosts(self, ctx):
        embed = discord.Embed(
            title='Booster - részletek',
            description='Nézd meg a szerver támogatóit.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb booster',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['túlóra'])
    async def tulora(self, ctx):
        embed = discord.Embed(
            title='Túlóra - részletek',
            description='Dolgozz munkaidőn kívül egy kis bónuszért.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb túlóra',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['segély'])
    async def segely(self, ctx):
        embed = discord.Embed(
            title='Segély - részletek',
            description='Ha tartozásban vagy ugorj be a hivatalba.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb segély',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def code(self, ctx):
        embed = discord.Embed(
            title='Kódok - részletek',
            description='Aktiválj különleges kódokat',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb code <kód>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def kereszt(self, ctx):
        embed = discord.Embed(
            title='Kereszt - részletek',
            description='Tartsd távol a gonoszt és a cringe-t.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kereszt',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def lecsap(self, ctx):
        embed = discord.Embed(
            title='Lecsap - részletek',
            description='Mutasd meg ki az úr.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb lecsap <@áldozat>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def kifoszt(self, ctx):
        embed = discord.Embed(
            title='Kifoszt - részletek',
            description='Lopd meg. (nem történik egyenleg változás, csak humor céljából külddÖ',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kifoszt <@áldozat>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['gazdagság'])
    async def gazdagsag(self, ctx):
        embed = discord.Embed(
            title='Gazdagság - részletek',
            description='Mutasd meg, hogy mennyire gazdag vagy.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb gazdagság',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True)
    async def rnjesus(self, ctx):
        embed=discord.Embed(
            title='RNJesus - részletek',
            description='Minden RNG ura',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rnjesus',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value=
                '`gyerele` '
                '`segíts`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @rnjesus.command()
    async def gyerele(self, ctx):
        embed = discord.Embed(
            title='RNJesus - Gyere le - részletek',
            description='Minden RNG ura előhívása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb rnjesus gyerele',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @rnjesus.command(aliases=['segíts'])
    async def segits(self, ctx):
        embed = discord.Embed(
            title='RNJesus - Segíts - részletek',
            description='Az RNG ura eldönti a sorsod',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb segíts <igen-nem kérdés>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def adatlap(self, ctx):

        embed=discord.Embed(
            title='Adatlap - részletek',
            description='Kiírja a tag adatait.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value=
                '`szint`'
                ' `plankpass`'
                ' `egyenleg`'
                ' `booster`'
                ' `kartyak`'
                ' `toplista`'
                ' `rangok`'
                ' `kép`'
                ' `állapot`',
                inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command(aliases=['kép'])
    async def kep(self, ctx):
        embed = discord.Embed(
            title='Adatlap - Kép - részletek',
            description='Megmutatja a tag profilképét nagy méretben.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap kép <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def szint(ctx):
        embed=discord.Embed(
            title='Adatlap - Szint - részletek',
            description='Kiírja a tag szintjét és tapasztalat pontját.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap szint <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def rangok(self, ctx):
        embed=discord.Embed(
            title='Adatlap - Rang - részletek',
            description='Kiírja a tag rangjait a szerveren.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap rang <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
                inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command(aliases=['állapot', 'allapot', 'status'])
    async def hallapot(self, ctx):
        embed = discord.Embed(
            title='Adatlap - Állapot - részletek',
            description='Kiírja a tag állapotát.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap állapot <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def egyenleg(ctx):
        embed=discord.Embed(
            title='Adatlap - Egyenleg - részletek',
            description='Kiírja a tag egyenlegét.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap egyenleg <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
                inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def plankpass(ctx):
        embed=discord.Embed(
            title='Adatlap - PlankPass - részletek',
            description='Kiírja a tag PlankPass tierét, ha rendelkezik vele.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap plankpass <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
                inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def booster(self, ctx):
        embed = discord.Embed(
            title='Adatlap - Booster - részletek',
            description='Kiírja, hogy a tag Boostolja-e a szervert',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap booster <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command()
    async def toplista(self, ctx):
        embed = discord.Embed(
            title='Adatlap - Lotto - részletek',
            description='Kiírja, hogy a tag nemrég nyert-e FŐNYEREMÉNY-t',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap lotto <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @adatlap.command(aliases=['kártyák'])
    async def kartyak(self, ctx):
        embed = discord.Embed(
            title='Adatlap - Kartyák - részletek',
            description='Kiírja a tag Univerzális Kártyáit',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adatlap kártyák <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def bolt(self, ctx):
        embed=discord.Embed(
            title='Bolt - részletek',
            description='Vásárlás a boltból.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb bolt',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`vesz`'
                ' `plankpass`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @bolt.command()
    async def vesz(self, ctx):
        embed=discord.Embed(
            title='Bolt - vesz - részletek',
            description='A Bot bolt rendszerét hívja elő.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb bolt vesz <azonosító>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @bolt.command()
    async def plankpass(self, ctx):
        embed=discord.Embed(
            title='Bolt - PlankPass - részletek',
            description='PlankPass vásárlása, vagy ajándékozása.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb bolt plankpass <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, aliases=['kártya'], pass_context=True)
    async def kartya(ctx):
        embed=discord.Embed(
            title='Kártya - részletek',
            description='Kiírja a tag kártyáit.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kártya <@tag>',
            inline=False
        )
        if str(ctx.message.channel.type) != 'private':
            if ctx.author.guild_permissions.administrator:
                embed.add_field(
                    name='További funkciók',
                    value=
                        ' `remove`'
                        ' `add`',
                    inline=False
                )
        else:
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )


        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @kartya.command()
    async def remove(ctx):
        embed=discord.Embed(
            title='Kártya - remove - részletek',
            description='Törli a tag kártyáit',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kártya remove <@tag> <azonosító>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @kartya.command()
    async def add(ctx):
        embed=discord.Embed(
            title='Kártya - add - részletek',
            description='Hozzáad a tag kártyáihoz.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kártya add <@tag> \"<kártya név>\" \"<kártya leírás>\"',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def invite(ctx):
        embed=discord.Embed(
            title='Invite - részletek',
            description='Elküldi a Bot meghívó linkjét és leírja az alap információit.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb invite',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def season(self, ctx):
        embed=discord.Embed(
            title='Season - részletek',
            description='Kiírja a Season adatait',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb season',
            inline=False
        )
        if str(ctx.message.channel.type) != 'private':
            if ctx.author.guild_permissions.administrator:
                embed.add_field(
                    name='További funkciók',
                    value='`dátum`'
                        ' `név`'
                        ' `rang`'
                        ' `ár`'
                        ' `kezd`',
                    inline=False
                )
        else:
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @season.command(aliases=['dátum'])
    async def datum(self, ctx):
        embed=discord.Embed(
            title='Season - dátum- részletek',
            description='Itt lehet megadni a Season határidejét.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb season dátum <dátum> - ÉV-HÓNAP-NAP - 2024-05-12',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @season.command(aliases=['név'])
    async def nev(self, ctx):
            embed=discord.Embed(
                title='Season - név - részletek',
                description='Itt lehet megadni a Season nevét',
                color=0x8a7c74
            )
            embed.add_field(
                name='Előhívás',
                value='!pb season név \"<név>\"',
                inline=False
            )
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )

            await ctx.author.send(embed=embed)

            await ctx.message.add_reaction('📩')
            await ctx.message.add_reaction('<:s_:815621316014374922>')
            await ctx.message.add_reaction('<:e_:815621316374954054>')
            await ctx.message.add_reaction('<:n_:815621316018962462>')
            await ctx.message.add_reaction('<:t_:815621315688005684>')

    @season.command()
    async def rang(ctx):
            embed=discord.Embed(
                title='Season - rang - részletek',
                description='Itt lehet megadni a PlankPass rangját',
                color=0x8a7c74
            )
            embed.add_field(
                name='Előhívás',
                value='!pb season rang <@rang>',
                inline=False
            )
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )

            await ctx.author.send(embed=embed)

            await ctx.message.add_reaction('📩')
            await ctx.message.add_reaction('<:s_:815621316014374922>')
            await ctx.message.add_reaction('<:e_:815621316374954054>')
            await ctx.message.add_reaction('<:n_:815621316018962462>')
            await ctx.message.add_reaction('<:t_:815621315688005684>')

    @season.command(aliases=['ár'])
    async def ar(self, ctx):
            embed=discord.Embed(
                title='Season - ár - részletek',
                description='Itt lehet megadni a PlankPass árát.',
                color=0x8a7c74
            )
            embed.add_field(
                name='Előhívás',
                value='!pb season ár <ár>',
                inline=False
            )
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )

            await ctx.author.send(embed=embed)

            await ctx.message.add_reaction('📩')
            await ctx.message.add_reaction('<:s_:815621316014374922>')
            await ctx.message.add_reaction('<:e_:815621316374954054>')
            await ctx.message.add_reaction('<:n_:815621316018962462>')
            await ctx.message.add_reaction('<:t_:815621315688005684>')

    @season.command()
    async def kezd(self, ctx):
            embed=discord.Embed(
                title='Season - kezd - részletek',
                description='Ezzel lehet elindítani a Seasont',
                color=0x8a7c74
            )
            embed.add_field(
                name='Előhívás',
                value='!pb season kezd',
                inline=False
            )
            embed.add_field(
                name='További funkciók',
                value='Nincs',
                inline=False
            )

            await ctx.author.send(embed=embed)

            await reaction(ctx.message)

    @season.command(aliases=['leállít'])
    async def hleallit(self, ctx):
        embed = discord.Embed(
            title='Season - leállít - részletek',
            description='Ezzel lehet ideiglenesen megállítani',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb season leállít',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @season.command(aliases=['kikapcsol'])
    async def hkikapcsol(self, ctx):
        embed = discord.Embed(
            title='Season - leállít - részletek',
            description='Ezzel lehet kikapcsolni a Season-t.\n'
                        'Ezzel törlöd a tagok Tier szintjét és PlankPass hozzáférését.\n'
                        'Ez visszavonhatatlan.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb season kikapcsol',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def egyenleg(self, ctx):
        embed=discord.Embed(
            title='Egyenleg - részletek',
            description='Ezzel tudod megnézni az egyenleged.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb egyenleg',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def fizet(self, ctx):
        embed=discord.Embed(
            title='Fizet - részletek',
            description='Pénz utalása másoknak',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb fizet <összeg> <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def munka(self, ctx):
        embed=discord.Embed(
            title='Munka - részletek',
            description='A munkáért pénzt kapsz',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb munka',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command(aliases=['lopás'])
    async def lopas(self, ctx):
        embed=discord.Embed(
            title='Lopás - részletek',
            description='A lopás kockázatos, de kifizetődő',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb lopás',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group()
    async def lotto(self, ctx):
        embed=discord.Embed(
            title='Lotto - részletek',
            description='Mersz kockáztatni?',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb lotto <szelvények száma>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`toplista`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @lotto.command(aliases=['toplista'])
    async def toplist(self, ctx):
        embed = discord.Embed(
            title='Lotto - Toplista - részletek',
            description='Nézd meg azokat akik megnyerték a FŐNYEREMÉNY-t',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb lotto toplista',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def roulette(self, ctx):
        embed=discord.Embed(
            title='Roulette - részletek',
            description='Egy tipikus szerencsejáték',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb roulette <fogadás> <tét>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )
        embed.add_field(
            name='Fogadható',
            value='-számok'
                '\n-páros vagy even'
                '\n-páratlan vagy odd'
                '\n-piros vagy red'
                '\n-fekete vagy black'
                '\n-1/12'
                '\n-2/12'
                '\n-3/12',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def slotmachine(self, ctx):
        embed=discord.Embed(
            title='Slot Machine - részletek',
            description='Vajon megéri? Senki sem tudja',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb slotmachine',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def clear(self, ctx):
        embed=discord.Embed(
            title='Clear - részletek',
            description='Kitörli a megadott mennyiségű üzenetet.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb clear <mennyiség>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def kick(self, ctx):
        embed=discord.Embed(
            title='Kick - részletek',
            description='Kirúg egy tagod a szerverről.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb kick <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def ban(self, ctx):
        embed=discord.Embed(
            title='Ban - részletek',
            description='Kitilt egy tagod a szerverről.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ban <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def mute(self, ctx):
        embed=discord.Embed(
            title='Mute - részletek',
            description='Lenémít egy tagot a megadott ideig.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb mute <@tag> <idő>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def adminfizet(self, ctx):
        embed=discord.Embed(
            title='AdminFizet - részletek',
            description='Pénzt hoz létre a megadott személy egyenlegére.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb adminfizet <összeg> <@tag>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def shop(self, ctx):
        embed=discord.Embed(
            title='Shop - részletek',
            description='A Bolt konfigurálása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb shop',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`create`'
                ' `delete`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @shop.command()
    async def delete(self, ctx):
        embed=discord.Embed(
            title='Shop - Delete - részletek',
            description='Termék eltávolítása a boltból.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb shop delete <azonosító>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @shop.group(invoke_without_command=True, pass_context=True)
    async def create(self, ctx):
        embed=discord.Embed(
            title='Shop - Add - részletek',
            description='Termék hozzáadása a bolthoz.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb shop create',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`role`'
                ' `card`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @create.command()
    async def role(ctx):
        embed=discord.Embed(
            title='Shop - Add - Role - részletek',
            description='Rang hozzáadása a bolthoz.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb shop create role <@rang> <ár>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @create.command()
    async def card(self, ctx):
        embed=discord.Embed(
            title='Shop - Add - Card - részletek',
            description='Kártya hozzáadása a bolthoz.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb shop create card \"<kártya neve\" \"<kártya leírása>\" <ár>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def ppreward(self, ctx):
        embed=discord.Embed(
            title='PlankPass reward - részletek',
            description='Ezzel lehet állítani, a PlankPass rewardokat.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`add`'
                ' `remove`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @ppreward.command()
    async def remove(ctx):
        embed=discord.Embed(
            title='PlankPass reward - Remove - részletek',
            description='Tier reward törlése',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward remove <tier>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @ppreward.group(invoke_without_command=True, pass_context=True)
    async def add(self, ctx):
        embed=discord.Embed(
            title='PlankPass reward - Add - részletek',
            description='Ezzel lehet hozzáadni rewardot a PlankPasshez.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward add',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`penz`'
                ' `rang`'
                ' `kartya`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @add.command()
    async def penz(ctx):
        embed=discord.Embed(
            title='PlankPass reward - Add - Pénz - részletek',
            description='Pénz reward adása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward add penz <tier> <összeg>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @add.command()
    async def rang(self, ctx):
        embed=discord.Embed(
            title='PlankPass reward - Add - Rang - részletek',
            description='Rang reward adása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward add rang <tier> <@rang>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @add.command()
    async def kartya(self, ctx):
        embed=discord.Embed(
            title='PlankPass reward - Add - Kártya - részletek',
            description='Kártya reward adása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb ppreward add kartya <tier> \"<kártya neve>\" \"<kártya leírása>\"',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def channel(self, ctx):
        embed=discord.Embed(
            title='Szoba konfigurálás - részletek',
            description='A értesítő szobák konfigurálása.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb channel',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`welcome`'
                ' `szint`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)


    @channel.command()
    async def welcome(self, ctx):
        embed=discord.Embed(
            title='Szoba konfigurálás - Hírek - részletek',
            description='A híreket értesítő szobák konfigurálása.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb channel welcome <@szoba>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @channel.command()
    async def szint(self, ctx):
        embed=discord.Embed(
            title='Szoba konfigurálás - Szintlépés - részletek',
            description='A szintlépéseket értesítő szobák konfigurálása.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb channel szint <@szoba>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.group(invoke_without_command=True, pass_context=True)
    async def role(self, ctx):
        embed=discord.Embed(
            title='Rang konfigurálás - részletek',
            description='A Bot által adott rangok konfigurálása.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb role',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='`nema` `bot` `auto`',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @role.command(aliases=['nema', 'néma'])
    async def hnema(self, ctx):
        embed = discord.Embed(
            title='Rang konfigurálás - Néma - részletek',
            description='A némítás rangja.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb role nema <@rang>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @role.command(aliases=['bot'])
    async def hbot(self, ctx):
        embed = discord.Embed(
            title='Rang konfigurálás - Bot - részletek',
            description='Csatlakozáskor automatikusan ráhelyezi egy Botra a rangot.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb role bot <@rang>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @role.command(aliases=['auto'])
    async def hauto(self, ctx):
        embed = discord.Embed(
            title='Rang konfigurálás - részletek',
            description='Az újonnan csatlakozó tagoknak adott rang.',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb role auto <@rang>',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)

    @help.command()
    async def fixserver(self, ctx):
        embed = discord.Embed(
            title='Szerver javítás - részletek',
            description='A gyakori \"KeyError\" javítása',
            color=0x8a7c74
        )
        embed.add_field(
            name='Előhívás',
            value='!pb fixserver',
            inline=False
        )
        embed.add_field(
            name='További funkciók',
            value='Nincs',
            inline=False
        )

        await ctx.author.send(embed=embed)

        await reaction(ctx.message)


async def reaction(message):
    await message.add_reaction('📩')
    await message.add_reaction('<:s_:815621316014374922>')
    await message.add_reaction('<:e_:815621316374954054>')
    await message.add_reaction('<:n_:815621316018962462>')
    await message.add_reaction('<:t_:815621315688005684>')


def setup(bot):
    bot.add_cog(HelpSystem(bot))

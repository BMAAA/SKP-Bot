import csv
import datetime, time
import discord
import random
from discord.ext import commands

with open('variables.csv', encoding="windows-1251") as csvfile:
    var_t = {}
    if csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)
        n = 0
        for i in reader:
            var_t[i[0]] = i[1]
rr_n = int(var_t["rr_n"])
brokephone = var_t["brokephone"]
dice_1 = {
    'user_id': var_t["dice_id"],
    'score': int(var_t["dice_score"])
}
print(rr_n, brokephone, dice_1)
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.presences = True
intents.moderation = True
intents.bans = True
client = commands.Bot(command_prefix="$", intents=intents)

with open('statistics/messages.csv', encoding="utf8") as csvfile:
    t = []
    if csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)
        n = 0
        for i in reader:
            t.append({})
            for j in range(len(headers)):
                t[n][headers[j]] = i[j]
                if headers[j] not in ('username', 'date'):
                    if not t[n][headers[j]]:
                        t[n][headers[j]] = 0
                    else:
                        t[n][headers[j]] = int(i[j])
            n += 1


def statistics_messages(message):
    if message.channel.id in (943891340285079662, 1023638137982943242) or message.guild.id != 887981666805628939:
        F = 0
        for i in range(len(t)):
            if t[i]['username'] == message.author.name and t[i]['guild'] == message.guild.id and \
                    t[i]['date'] == datetime.datetime.now().strftime('%d/%m/%y'):
                t[i]["messages"] += 1
                F = 1
                break
        if not F:
            t.append({
                "username": message.author.name,
                "guild": message.guild.id,
                "date": datetime.datetime.now().strftime('%d/%m/%y'),
                "messages": 1
            })
        with open('statistics/messages.csv', 'w', newline='') as f:
            writer = csv.DictWriter(
                f, fieldnames=list(t[0].keys()), delimiter=',',
                quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for d in t:
                writer.writerow(d)


def save_variables():
    var = [
        {
            "name": "rr_n",
            "value": rr_n
        },
        {
            "name": "brokephone",
            "value": brokephone
        },
        {
            "name": "dice_id",
            "value": dice_1['user_id']
        },
        {
            "name": "dice_score",
            "value": dice_1['score']
        },
    ]
    with open('variables.csv', 'w', newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=list(var[0].keys()), delimiter=',',
            quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for d in var:
            writer.writerow(d)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global rr_n, brokephone, dice_1
    if message.author == client.user:
        return

    try:
        print(f"{datetime.datetime.now().strftime('%d/%m/%y')}: by {message.author}, '{message.content}'")
    except:
        print('Ашибка')
    statistics_messages(message)
    save_variables()

    await client.process_commands(message)


@client.command(name="test")
async def hello(ctx: discord.ext.commands.Context):
    await ctx.send('Hello!')
    print("+")


@client.command(name="ball")
async def ball(ctx):
    random.seed(int(time.mktime(datetime.datetime.now().timetuple())))
    v1 = random.randint(0, 2)
    lis = [
        [
            f"Да",
            f"Ага <:jopker:1208510015783309393>",
            f"Угу",
            f"Ты краснопопик <:face:1183766937499607040>"
        ],
        [
            f"Шар судьбы говорит... Да какая разница что он говорит?",
            f"Я занят, отстань",
            f"Урок по основам православной культуры. Учительница:\n— "
            f"И помните, дети! Те, кто будет учиться на «4» и «5», попадут в рай. "
            f"А те, кто будет учиться на «2» и «3», — в ад!\nВовочка с задней парты:\n— Мариванна,"
            f" а что, закончить школу живым нельзя?",
            f"Не знаю."
        ],
        [
            f"Да нет наверное",
            f"Когда рак на горе свистнет",
            f"Спроси у имени",
            f"Здесь должна была быть шутка про отчима но ее не будет <:sadjopker:1230585532103528488>",
            f"Ю ФАКИНГ СЛЕЙВ",
            f"Я подумаю"
        ]

    ]
    v2 = random.randint(0, len(lis[v1]) - 1)
    print(v1, v2)
    await ctx.send(lis[v1][v2])


@client.command(name="ruletka")
async def ruletka(ctx):
    global rr_n
    random.seed(int(time.mktime(datetime.datetime.now().timetuple())))
    value = random.randint(1, rr_n)
    if value == 1:
        try:
            await ctx.author.timeout(datetime.timedelta(minutes=1), reason=f"Проиграл в русской рулетке")
        except:
            pass
        await ctx.send(f"Ты проиграл в рулетке 🔫<:nespravedlivo:1183766894558322729>")
        rr_n = 6
    else:
        await ctx.send(f"Везунчик! Ты выиграл в рулетке <:spravedlivo:896323250009821205> {rr_n}")
        rr_n -= 1


@client.command(name="dice")
async def dice(ctx):
    global dice_1
    dice_2 = {
        'user_id': ctx.author.id,
        'score': random.randint(1, 6) + random.randint(1, 6)
    }
    await ctx.send(
        f"Вы кидаете кости! 🎲 \nВаш счёт: {dice_2['score']}\nСчёт <@{dice_1['user_id']}>: {dice_1['score']}\nВыигрывает <@{dice_1['user_id'] if dice_1['score'] > dice_2['score'] else dice_2['user_id']}>!")
    dice_1 = dice_2


@client.command(name="phone")
async def phone(ctx, *text):
    global brokephone
    text = " ".join(text)
    if text == 'current':
        await ctx.send(f"Текущий текст для расшифровки: `{'...'.join(list(brokephone))}`")
    elif text:
        F, n = 0, 0

        for i in text:
            if brokephone[n] == i:
                n += 1
            if n == len(brokephone):
                F = 1
                break
        if F:
            brokephone = text[::random.randint(1, len(text) // 2)]
            await ctx.message.delete()
            await ctx.send(f"<@{ctx.author.id}> расшифровал сообщение! <:pivo:1183770038767984640>")
            await ctx.send(f"Новое сообщение: `{'...'.join(list(brokephone))}`")
        else:
            await ctx.send(f"К сожалению, ваш текст не подходит. Продолжайте расшифровку.")
    else:
        await ctx.send(f"Напишите любой текст после команды, предложив вариант расшифровки сообщения.")
        await ctx.send(f"Просмотреть его можно по команде: `$phone current`")


@client.command(name="nextclass")
async def n_class(ctx):
    class_list = [
        [
            {
                "name": 'Завоеватель',
                "description": 'Этот могучий боец способен ловко отражать атаки со всех сторон одновременно и может'
                               ' в любой момент использовать огромные резервы силы, чтобы сразить своих врагов.'
            },
            {
                "name": 'Ассасин',
                "description": 'Беспощадный ассасин скользит по полю боя подобно тени, не спуская глаз со врага, '
                               'уничтожая важные цели в его тылу и оставляя за собой след из окровавленных трупов.'
            },
            {
                "name": 'Пирорыцарь',
                "description": 'Этот спаситель использует огонь у себя в крови и на клинке, чтобы от зла не осталось '
                               'ничего, кроме сажи и пепла. Он рассекает тьму клинком своей мудрости, чтобы вернуть'
                               ' миру свет.'
            },
            {
                "name": 'Дикоход',
                "description": 'Дикоход — стойкий воин и хозяин дикой природы, который без колебаний бросается в гущу'
                               ' битвы. Он может манипулировать энергией жизни, чтобы лечить ранения.'
            },
            {
                "name": 'Рыцарь ужаса',
                "description": 'Нечестивый символ войны и мрака, что своим гигантским мечом подчиняет отступников и '
                               'подпитывает кровь новой кровью, дабы повсеместно распространить свою власть.'
            }
        ],
        [
            {
                "name": 'Бастион',
                "description": 'Атаки лучников позволяют обнаружить всех врагов поблизости. Они не забывают и о защите,'
                               ' уничтожая любого, кто входит в их область поражения.'
            },
            {
                "name": 'Стрелок',
                "description": 'Свободные как ветер героические преступники могут без особых усилий пронзать копьями'
                               ' врагов на расстоянии в несколько миль и покрывать все небо стрелами во время слаженной'
                               ' атаки.'
            },
            {
                "name": 'Артиллерист',
                "description": 'Безбашенный смельчак-бомбардир, чьи снаряды наносят немыслимый урон с разрушительной'
                               ' эффективностью, уничтожая укрепления и сопротивление врага.'
            },
            {
                "name": 'Дальнеход',
                "description": 'Дальнеход — ловкий снайпер, который чувствует себя в лесу как дома. Он изнуряет своих'
                               ' жертв мощными ядами, прежде чем нанести смертельный удар.'
            },
            {
                "name": 'Тёмный стрелок',
                "description": 'Искусный и опытный воитель, преодолевающий самые опасные участки фронтов с изящной '
                               'легкостью, отбирая у врагов их последнее прибежище межпланетными бомбардировками и '
                               'поражая сердца недругов стрелами, рожденными в недрах самой пустоты.'
            }
        ],
        [
            {
                "name": 'Хранитель бурь',
                "description": 'Непреклонные, как ледники, хранители бурь замораживают и разбивают противников на'
                               ' осколки. Они очищают мир от мусора, хладнокровно атакуя врагов с помощью копий и щитов.'
            },
            {
                "name": 'Клинок бурь',
                "description": 'Клинок бурь, обладающий неистовой мощью штурмовик, может поражать врагов подобно молнии'
                               ' и разрывать вражеский строй одним взмахом своих электрических клинков.'
            },
            {
                "name": 'Элементалист',
                "description": 'Повелитель стихий, эрудированный мудрец, который может с помощью трехцветной магии'
                               ' нести погибель и творить чудеса, чтобы поставить на колени целые легионы.'
            },
            {
                "name": 'Штормшаман',
                "description": 'Штормшаман — духовный наставник и хранитель веры предков. Он может призывать'
                               ' первобытных элементов и уничтожать врагов с помощью сокрушительных стихий.'
            },
            {
                "name": 'Астральный маг',
                "description": 'Ученый-мистик, который бросает вызов научным сообществам практическим применением '
                               'своей выдающейся теории инверсии стихий, а также упорным поиском предметов, связанных '
                               'с пустотой и ее проклятыми силами.'
            }
        ],
        [
            {
                "name": 'Хранитель душ',
                "description": 'Хранитель душ, командир, пользующийся общим доверием. Он яростно защищает призванных'
                               ' приспешников, создавая нерушимую связь, способную бросить вызов самой судьбе.'
            },
            {
                "name": 'Шиноби',
                "description": 'Шиноби, непостижимый и неуловимый враг, способный использовать уловки, чтобы оградить'
                               ' себя от урона, и создавать иллюзии, чтобы пополнять свои ряды в бою.'
            },
            {
                "name": 'Еретик',
                "description": 'Еретик, апостол, возродившийся из пепла. Ему служат адские приспешники, '
                               'жаждущие сеять хаос по его приказу. Он управляет древним драконом, способным'
                               ' сжечь саму реальность.'
            },
            {
                "name": 'Друид',
                "description": 'Друид — олицетворение неукротимой природы. Он может призвать верных зверей-спутников'
                               ' и превращаться в огромного медведя с несравненной мускулатурой,'
                               ' чтобы сокрушать врагов.'
            },
            {
                "name": 'Некромант',
                "description": 'Проводник между жизнью и смертью, который пытается обрести некое подобие бессмертия. '
                               'Он использует негасимую сущность покойного, чтобы заманить души в бесконечный танец '
                               'контроля и лжи.'
            }
        ]
    ]
    class_emojis = [["🗡", "🏹", ":snowflake:", "🔮"], ["🛡", ":crossed_swords:", "🔥", "🧪", "🌌"]]
    x, y = random.randint(0, 3), random.randint(0, 4)
    print(x, y)
    await ctx.send(
        f"Вашим следующим классом будет **{class_list[x][y]['name']}** {class_emojis[0][x]}×{class_emojis[1][y]}\n"
        f"> {class_list[x][y]['description']}")


@client.command()
async def report(author, command, member, reason):
    channel = client.get_channel(1189277237288116294)
    await channel.send(
        f"<@{author.id}> использовал команду `{command}` по отношению к участнику **<@{member.id}>** по причине:\n"
        f"> {reason}")


@client.command(name="voteban")
@commands.has_permissions(kick_members=True)
async def v_ban(ctx, member: discord.Member = None, *, reason=None):
    try:
        await member.timeout(datetime.timedelta(days=7), reason=reason)
        await report(ctx.author, "$voteban", member, reason)
        await ctx.send(
            f"Отправлен запрос на блокировку участника {member} в <#1189277237288116294>. На время рассмотрения"
            f" запроса он отправлен в таймаут")
    except:
        await ctx.send(f"Случилась какая-то ошибка. Попробуйте еще раз или обратитесь к старшему по званию.")


@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    try:
        await member.ban(reason=reason)
        await report(ctx.author, "$ban", member, reason)
        await ctx.send(f"Участник <@{member}> был успешно забанен.")
    except:
        await ctx.send(f"Случилась какая-то ошибка. Попробуйте еще раз или обратитесь к старшему по званию.")


@client.command(name="mute")
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member = None, minutes: int = 0, hours: int = 0, days: int = 0, *, reason=None):
    try:
        await member.timeout(datetime.timedelta(days=days, hours=hours, minutes=minutes), reason=reason)
        await report(ctx.author, "$mute", member, reason)
        await ctx.send(f"Участник <@{member.id}> был успешно отправлен в таймаут.")
    except:
        await ctx.send(f"Случилась какая-то ошибка. Попробуйте еще раз или обратитесь к старшему по званию.")


@client.command(name="unmute")
@commands.has_permissions(moderate_members=True)
async def unmute(ctx, member: discord.Member = None, *, reason=None):
    try:
        await member.edit(timed_out_until=None)
        await report(ctx.author, "$unmute", member, reason)
        await ctx.send(f"Участник <@{member.id}> был успешно возвращен из таймаута.")
    except:
        await ctx.send(f"Случилась какая-то ошибка. Попробуйте еще раз или обратитесь к старшему по званию.")


token = open('token.txt', 'r').read()
client.run(token)

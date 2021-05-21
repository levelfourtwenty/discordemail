from email.message import EmailMessage
import email
import discord
from smtplib import SMTP_SSL, SMTP
from imaplib import IMAP4_SSL, IMAP4
from discord.ext import commands

bot = commands.Bot(command_prefix='+', help_command=None)
m = IMAP4_SSL(port='993', host='imap.example.com')
s = SMTP_SSL(host='smtp.example.com', port=465)
fromaddr = "email@email.com"
@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Help", description="Shows bot commands.", color=0xFF5733)
    embed.add_field(name="+sendmail", value="Sends mail to specified address, syntax is +sendmail \"addresses you want to send to\", \"<Subject>\", \"<Message body>\". You can specify multiple recipients by using a \", \".", inline=False)
    embed.add_field(name="+getmail", value="Gets specifed amount of messages, up to 5 latest. ", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def sendmail(ctx, toaddrs, subject, body):
        s.login(fromaddr, 'PASSWORD HERE')
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['To'] = toaddrs.split(", ")
        msg['From'] = fromaddr
        s.set_debuglevel(2)
        s.send_message(msg)
        s.quit()
        embed=discord.Embed(title="Message details", color=0xFF5733)
        embed.add_field(name="Recipients:", value=toaddrs, inline=False)
        embed.add_field(name="From:", value=fromaddr, inline=False)
        embed.add_field(name="Subject:", value=subject, inline=False)
        embed.add_field(name="Message Body:", value=body, inline=False)
        await ctx.channel.send(embed=embed)



@bot.command()
async def getmail(ctx):
        N = 4
        m.login("EMAIL HERE", "PASSWORD HERE")
        status, messages = m.select('"[Gmail]/All Mail"')
        messages = int(messages[0])
        for i in range(messages, messages-N, -1):
                res, msg = m.fetch(str(1), "(RFC822)")

        for response in msg:
                if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                                subject.decpde(encoding)
                        if isinstance(From, bytes):
                                From = From.decode(encoding)
                        if msg.is_multipart():
                                for part in msg.walk():
                                        content_type = part.get_content_type()
                                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                                body = part.get_payload(decode=True).decode()
                        except:
                                pass


                        if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(body)
                        else:
                                pass
                else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                                print(body)
                        else:
                                pass
        m.close()
        m.logout()
        embed=discord.Embed(title="Message", color=0xFF5733)
        embed.add_field(name="From:", value=From)
        embed.add_field(name="Subject:", value=subject)
        embed.add_field(name="Body:", value=body)
        ctx.channel.send(embed=embed)


bot.run('TOKEN HERE')

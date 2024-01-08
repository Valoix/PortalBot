import discord
import responses
from discord.ext import commands
from discord.utils import get
import secret
import ticks
import os
from moviepy.editor import *
import random
import asyncio


async def send_message(message, user_message):
    try:
        response = responses.handle_response(message, user_message)
        if response:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():

    # Intents
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    # Turns on successfully
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")

    # Read Reactions
    @client.event
    async def on_raw_reaction_add(payload):
        message_id_found = False
        reaction_amount_to_pin = 10
        pin_channel_id = 1192784040634351757
        if payload.emoji.name == "📌":
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            if reaction and reaction.count == reaction_amount_to_pin:
                with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\pinnerino_message_ids.txt", "r") as file:
                    for id in file.readlines():
                        if str(message.id) == id[0:-1]:
                            # ID is found in DB
                            message_id_found = True
                            break
                    file.close()
                
                if message_id_found == False:
                    with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\pinnerino_message_ids.txt", "a") as file:
                        file.write(f"{message.id}\n")
                    file.close()
                    attachments = message.attachments
                    channel = client.get_channel(pin_channel_id)
                    pin_embed = discord.Embed(title=str(message.author).capitalize(), description=str(message.content), color=0xFF0000)
                    if attachments:
                        attachments_filename = str(message.attachments).split("'")[1]
                        # Pin Contains MP4
                        if attachments_filename.endswith(".mp4"):
                            await message.attachments[0].save("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\pinnerino.mp4")        
                            await channel.send(embed=pin_embed)
                            await channel.send(file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\pinnerino.mp4"))
                        
                        # Pin Contains IMAGE
                        else:
                            await message.attachments[0].save("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\pinnerino.jpg")        
                            await channel.send(embed=pin_embed)
                            await channel.send(file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\pinnerino.jpg"))
                        await channel.send(responses.generate_message_link(message.guild.id, message.channel.id, message.id))
                    else:
                        # Pin Contains Tenor GIF
                        if "https://tenor.com/view/" in message.content:
                            pin_embed = discord.Embed(title=str(message.author).capitalize(), description="SENT GIF", color=0xFF0000)
                            await channel.send(embed=pin_embed)
                            await channel.send(message.content)
                            await channel.send(responses.generate_message_link(message.guild.id, message.channel.id, message.id))
                        elif ".gif" in message.content:
                            pin_embed = discord.Embed(title=str(message.author).capitalize(), description="SENT GIF", color=0xFF0000)
                            await channel.send(embed=pin_embed)
                            await channel.send(message.content)
                            await channel.send(responses.generate_message_link(message.guild.id, message.channel.id, message.id))

                        # Pin has NO GIF AND NO ATTACHMENT
                        else:
                            await channel.send(embed=pin_embed)
                            await channel.send(responses.generate_message_link(message.guild.id, message.channel.id, message.id))

    # Reads Messages
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Check if text contains dox
        if responses.text_dox_blox(user_message):
            print("Dox Detected")
            await message.author.ban(reason="Potential Dox Detected")
            await message.delete()
        
        # Check if username contains dox
        if responses.name_dox_blox(username):
            print("Dox Detected")
            await message.author.ban(reason="Potential Dox Detected")
            await message.delete()

        # Emergency Exit
        if user_message == "emergencyexit++":
            big_boss_roles = ["Community contributor", "SRC verifier", "Moderation Team", "Admin"]
            for role in message.author.roles:
                    # Moderator Only
                    #if str(role) == "Moderation Team":
                    
                    # Contributor and above
                    if str(role) in big_boss_roles:
                        await message.channel.send("Shutting Down...")
                        exit()



        # Help Manual

        # Convert Ticks into Time
        if user_message[0:11] == "tick2time++" or user_message[0:12] == "ticks2time++":
            convert_contents = user_message.split()
            print(convert_contents)
            try:
                for letter in convert_contents[1]:
                    if letter == "@":
                        int("fuck")
                try:
                    await message.channel.send(ticks.tick_to_time(convert_contents[1]))
                except:
                    await message.channel.send(f'Your ticks "{convert_contents[1]}" was not a valid tick count, please try again!')
            except Exception as e:
                print(e)
                await message.channel.send("i no no wanna :(")
        
        # Convert Time into Ticks
        if user_message[0:11] == "time2tick++" or user_message[0:12] == "time2ticks++":
            convert_contents = user_message.split()
            print(convert_contents)
            try:
                for letter in convert_contents[1]:
                    if letter == "@":
                        int("fuck")
                try:
                    await message.channel.send(ticks.time_to_tick(convert_contents[1]))
                except:
                    await message.channel.send(f'Your time "{convert_contents[1]}" was not a valid time, please try again!')
            except Exception as e:
                print(e)
                await message.channel.send("i no no wanna :(")
        
        try:
            try:
                attachments = message.attachments

                # Get Attachment Name
                attachments_filename = str(message.attachments).split("'")[1]

                if attachments_filename.endswith(".mkv"):
                    try:
                        await message.channel.send("Converting to MP4...")
                        # Downloading the MKV File
                        print("Downloading Video...")
                        await message.attachments[0].save("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\input_video.mkv")
                        print("Downloaded")

                        # Converting MKV -> MP4
                        print("Converting to MP4")
                        # Converts MKV => Raw MP4 (not web optimized)
                        os.rename("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\input_video.mkv", "C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4")
                        # Compresses to according to original file size
                        clip = VideoFileClip("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4")
                        print(str(os.path.getsize("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4")) + "bytes")
                        if os.path.getsize("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4") > 30000000:
                            print("Converting to 240p")
                            resized_clip = clip.fx(vfx.resize,width=427,height=240)
                        elif os.path.getsize("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4") > 20000000:
                            print("Converting to 480p")
                            resized_clip = clip.fx(vfx.resize,width=854,height=480)
                        else:
                            print("Converting to 720p")
                            resized_clip = clip.fx(vfx.resize,width=1280,height=720)
                        resized_clip.write_videofile("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\resized_output_video.mp4")
                        clip.close()
                        print("Converted Successfully")
                        # Send back to Channel
                        await message.channel.send("Converted Successfully!", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\resized_output_video.mp4"))
                        # Remove left overs
                        os.remove("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4")
                        os.remove("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\resized_output_video.mp4")
                    except:
                        await message.channel.send("Something went wrong!!! :((")
                        try:
                            os.remove("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\input_video.mkv")
                            os.remove("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\output_video.mp4")
                            os.remove("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\resized_output_video.mp4")
                        except:
                            pass

                # Download Attachment
                await message.attachments[0].save("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\image.jpg")
                print(f"{username}: '{user_message}' [{channel}] with ({attachments})")

                # Check if image attachment contains dox
                if responses.image_dox_blox():
                    print("Dox Detected")
                    await message.author.ban(reason="Potential Dox Detected")
                    await message.delete()
            except:
                pass
            
            # WR Posting
            # message.channel.id (int) = the moderation channel of choice
            if user_message[0:4] == "wr++":

                # Splits the command and parameters into an array
                wr_message = user_message.split(" ")
                try:
                    for letter in user_message:
                        if letter == "@":
                            int("fuck")

                    # wr++ help command
                    if wr_message[1] == "help":
                            await message.channel.send("""```wr++ manual :)

wr++ help - Displays the help menu (duh)

wr++ search name <username> - Search WR archive for runs by a certain user.
wr++ search category <inb, noslal, noslau, oob, gless> - Search WR archive for all WRs in a category.
wr++ search year <YYYY> - Search WR archive for runs done in that year.

*for wr++ archive moderation tools, please contact Valoix or someone else who knows how to use it!*```""")

                    # wr++ search command

                    if wr_message[1] == "search":
                        # for name
                        wr_search_output_1 = ""
                        wr_search_output_2 = ""
                        if wr_message[2] == "name":
                            await message.channel.send(f"Seaching for name {wr_message[3]}...")
                            with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\wr_archive.txt", "r") as file:
                                for line in file.readlines():
                                    if line.split()[0].lower() == wr_message[3].lower():
                                        if len(wr_search_output_1) < 1700:
                                            wr_search_output_1 += f"{responses.process_wr_output(line)}"
                                        else:
                                            wr_search_output_2 += f"{responses.process_wr_output(line)}"
                                if wr_search_output_1 == "":
                                    await message.channel.send("Oops! Something went wrong. Please contact Valoix or someone who knows how to use the command for more information :)")
                                else:
                                    await message.author.send(f"**WR ARCHIVE SEARCH FOR '{wr_message[3]}'**\n{wr_search_output_1}")
                                    if wr_search_output_2 != "":
                                        await message.author.send(f"\n{wr_search_output_2}")
                                    await message.channel.send("Finished! Found WRs will be sent to your DMs :)")
                                file.close()
                        # for category
                        if wr_message[2] == "category":
                            search_category = ""
                            await message.channel.send(f"Seaching for category {wr_message[3]}...")
                            with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\wr_archive.txt", "r") as file:
                                # Category Translation
                                if wr_message[3] == "glitchless" or wr_message[3] == "gless" or wr_category[3] == "g":
                                    search_category = "g"
                                elif wr_message[3] == "noslal" or wr_message[3] == "nl":
                                    search_category = "nl"
                                elif wr_message[3] == "noslau" or wr_message[3] == "nu":
                                    search_category = "nu"
                                elif wr_message[3] == "inbounds" or wr_message[3] == "inb" or wr_message[3] == "i":
                                    search_category = "i"
                                elif wr_message[3] == "oob" or wr_message[3] == "o":
                                    search_category = "o"
                                for line in file.readlines():
                                    if line.split()[1].lower() == search_category.lower():
                                        if len(wr_search_output_1) < 1700:
                                            wr_search_output_1 += f"\n{responses.process_wr_output(line)}"
                                        else:
                                            wr_search_output_2 += f"{responses.process_wr_output(line)} \n"
                                if wr_search_output_1 == "":
                                    await message.channel.send("Oops! Something went wrong. Please contact Valoix or someone who knows how to use the command for more information :)")
                                else:
                                    await message.author.send(f"**WR ARCHIVE SEARCH FOR '{wr_message[3]}'**\n{wr_search_output_1}")
                                    if wr_search_output_2 != "":
                                        await message.author.send(f"{wr_search_output_2}")
                                    await message.channel.send("Finished! Found WRs will be sent to your DMs :)")
                                file.close()
                        # for year
                        if wr_message[2] == "year":
                            await message.channel.send(f"Seaching for year {wr_message[3]}...")
                            with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\wr_archive.txt", "r") as file:
                                for line in file.readlines():
                                    if line.split()[3][-4:] == wr_message[3]:
                                        if len(wr_search_output_1) < 1700:
                                            wr_search_output_1 += f"\n{responses.process_wr_output(line)}"
                                        else:
                                            wr_search_output_2 += f"{responses.process_wr_output(line)} \n"
                                if wr_search_output_1 == "":
                                    await message.channel.send("Oops! Something went wrong. Please contact Valoix or someone who knows how to use the command for more information :)")
                                else:
                                    await message.author.send(f"**WR ARCHIVE SEARCH FOR '{wr_message[3]}'**\n{wr_search_output_1}")
                                    if wr_search_output_2 != "":
                                        await message.author.send(f"{wr_search_output_2}")
                                    await message.channel.send("Finished! Found WRs will be sent to your DMs :)")
                                file.close()
                except Exception as e:
                    print(e)
                    await message.channel.send("i no no wanna :(")


                # Get wr-posting channel id (int)
                wr_channel_id = 1174320230386901023

                # wr_message = ["wr++", "<name>", "<category>", "<time>", "<date (DD/MM/YYYY)>" "<message link>"]

                # CATEGORY:
                # Glitchless - g, gless, glitchless
                # NoSLA Legacy - nl, noslal
                # NoSLA Unrestricted - nu, noslau
                # Inbounds - i, inb, inbounds
                # Out of Bounds - o, oob

                wr_name = str(wr_message[1])
                wr_category = str(wr_message[2])
                wr_time = str(wr_message[3])
                wr_date = str(wr_message[4])
                wr_message_link = str(wr_message[5])

                big_boss_roles = ["Community contributor", "SRC verifier", "Moderation Team", "Admin"]

                for role in message.author.roles:
                    # Moderator Only
                    #if str(role) == "Moderation Team":
                    
                    # Contributor and above
                    if str(role) in big_boss_roles:
                        try:
                            # Try to Download WR Image
                            try:
                                await message.attachments[0].save("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg")
                            except:
                                int("force error lol")
                            if wr_category == "glitchless" or wr_category == "g" or wr_category == "gless":
                                channel = client.get_channel(wr_channel_id)
                                await channel.send(f"[{wr_date}] {wr_name.capitalize()} just got a World Record Glitchless run in {wr_time}! Congratulations :tada: {wr_message_link}", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg"))
                            elif wr_category == "noslal" or wr_category == "nl":
                                channel = client.get_channel(wr_channel_id)
                                await channel.send(f"[{wr_date}] {wr_name.capitalize()} just got a World Record NoSLA Legacy run in {wr_time}! Congratulations :tada: {wr_message_link}", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg"))
                            elif wr_category == "noslau" or wr_category == "nu":
                                channel = client.get_channel(wr_channel_id)
                                await channel.send(f"[{wr_date}] {wr_name.capitalize()} just got a World Record NoSLA Unrestricted run in {wr_time}! Congratulations :tada: {wr_message_link}", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg"))
                            elif wr_category == "inbounds" or wr_category == "i" or wr_category == "inb":
                                channel = client.get_channel(wr_channel_id)
                                await channel.send(f"[{wr_date}] {wr_name.capitalize()} just got a World Record Inbounds run in {wr_time}! Congratulations :tada: {wr_message_link}", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg"))
                            elif wr_category == "oob" or wr_category == "o":
                                channel = client.get_channel(wr_channel_id)
                                await channel.send(f"[{wr_date}] {wr_name.capitalize()} just got a World Record Out of Bounds run in {wr_time}! Congratulations :tada: {wr_message_link}", file=discord.File("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\downloads\\wr.jpg"))
                            responses.wr_db_add(wr_category, wr_time, wr_name, wr_date, wr_message_link)
                            break
                        except:
                            channel = str(message.channel)
                            await message.channel.send("Oops! Something went wrong :(. Please contact developer for more information!")
                            break
                        
            
            # Break if everything false
            else:
                int("fuck")
        except:
            print(f"{username}: '{user_message}' [{channel}]") 

        await send_message(message, user_message)


    client.run(secret.get_token())
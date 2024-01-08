from PIL import Image
import pytesseract
import cv2
import secret
import random


big_boss_roles = ["Community contributor", "SRC verifier", "Moderation Team", "Admin"]

def handle_response(user_data, message):
    if message == "cube++":
        for role in user_data.author.roles:
            if str(role) in big_boss_roles:
                with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\cube_count.txt", "r") as read_cube_count:
                    cube_count = int(read_cube_count.read())
                with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\cube_count.txt", "w") as write_cube_count:
                    write_cube_count.write(str(cube_count+1))
                    return f"So many cubes! I've now seen {str(cube_count+1)} cubes!"
    
    if message == "cube--":
        for role in user_data.author.roles:
            if str(role) in big_boss_roles:
                with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\cube_count.txt", "r") as read_cube_count:
                    cube_count = int(read_cube_count.read())
                with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\cube_count.txt", "w") as write_cube_count:
                    write_cube_count.write(str(cube_count-1))
                    return f"I was mistaken, cube rescinded. I've now seen only {str(cube_count-1)} cubes!"

    if message == "admin test":
        return "testing testing 123"
    

    # If message does not meet above conditions
    else:
        return False


def image_dox_blox():
    pass
    # REMOVED FOR SECURITY PURPOSES
    
def text_dox_blox(message):
    pass
    # REMOVED FOR SECURITY PURPOSES
        
def name_dox_blox(username):
    pass
    # REMOVED FOR SECURITY PURPOSES

def wr_db_add(wr_category, wr_time, wr_name, wr_date, wr_message_link):
    print("Begin Writing to WR DB")
    # CATEGORY:
                # Glitchless - g, gless, glitchless
                # NoSLA Legacy - nl, noslal
                # NoSLA Unrestricted - nu, noslau
                # Inbounds - i, inb, inbounds
                # Out of Bounds - o, oob

    # Category Translation
    if wr_category == "glitchless" or wr_category == "gless":
        wr_category = "g"
    
    elif wr_category == "noslal":
        wr_category = "nl"

    elif wr_category == "noslau":
        wr_category = "nu"

    elif wr_category == "inbounds" or wr_category == "inb":
        wr_category = "i"

    elif wr_category == "oob":
        wr_category = "o"
    print("Translated")

    with open("C:\\Users\\Valoix\\Documents\\Programming Projects\\python\\PortalBot\\wr_archive.txt", "a") as file:
        file.write(f"{wr_name} {wr_category} {wr_time} {wr_date} {wr_message_link}\n")
        print("Write Success")
    file.close()

def process_wr_output(raw_wr_search):
    #line_words = ["name", "category", "time", "date", "message link"]

    line_words = str(raw_wr_search).split(" ")

    wr_name = str(line_words[0]).lower()
    wr_category = str(line_words[1]).lower()
    wr_time = str(line_words[2])
    wr_date = str(line_words[3])
    wr_message_link = str(line_words[4])

    # Category Processing
    if wr_category == "g":
        wr_category = "Glitchless"
    elif wr_category == "nl":
        wr_category = "NoSLA Legacy"
    elif wr_category == "nu":
        wr_category = "NoSLA Unrestricted"
    elif wr_category == "i":
        wr_category = "Inbounds"
    elif wr_category == "o":
        wr_category = "Out of Bounds"

    return f"[{wr_date}] {wr_name.capitalize()} {wr_category} {wr_time} {wr_message_link}"

def generate_message_link(server_id, channel_id, message_id):
    return f"https://discord.com/channels/{server_id}/{channel_id}/{message_id}"

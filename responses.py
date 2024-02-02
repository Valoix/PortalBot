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
                with open("./cube_count.txt", "r") as read_cube_count:
                    cube_count = int(read_cube_count.read())
                with open("./cube_count.txt", "w") as write_cube_count:
                    write_cube_count.write(str(cube_count+1))
                    return f"So many cubes! I've now seen {str(cube_count+1)} cubes!"
    
    if message == "cube--":
        for role in user_data.author.roles:
            if str(role) in big_boss_roles:
                with open("./cube_count.txt", "r") as read_cube_count:
                    cube_count = int(read_cube_count.read())
                with open("./cube_count.txt", "w") as write_cube_count:
                    write_cube_count.write(str(cube_count-1))
                    return f"I was mistaken, cube rescinded. I've now seen only {str(cube_count-1)} cubes!"

    if message == "admin test":
        return "testing testing 123"
    

    # If message does not meet above conditions
    else:
        return False


def image_dox_blox():
    myconfig = r"--psm 11 --osm 3"
    text = pytesseract.image_to_string(Image.open("./downloads/image.jpg"))
    print(text)
    for term in secret.get_dox_terms():
        if term in text:
            return True, text
        else:
            return False, text
    
def text_dox_blox(message):
    for term in secret.get_dox_terms():
        if term in message:
            return True
        else:
            return False
        
def name_dox_blox(username):
    for term in secret.get_dox_terms():
        if term in username:
            return True
        else:
            return False

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

    with open("./wr_archive.txt", "a") as file:
        file.write(f"{wr_name} {wr_category} {wr_time} {wr_date} {wr_message_link}\n")
        print("Write Success")
    file.close()

def process_wr_category(category):
    # Category Handling
    categories = {
    "g": "Glitchless",
    "nl": "NoSLA Legacy",
    "nu": "NoSLA Unrestricted",
    "i": "Inbounds", 
    "o": "Out of Bounds"
    }

    return categories.get(category)

def process_wr_output(raw_wr_search):
    #line_words = ["name", "category", "time", "date", "message link"]

    line_words = str(raw_wr_search).split(" ")

    # Parses line_words
    wr_name = str(line_words[0]).lower()
    wr_category = process_wr_category(line_words[1].lower())
    wr_time = str(line_words[2])
    wr_date = str(line_words[3])
    wr_message_link = str(line_words[4])

    return f"[{wr_date}] {wr_name.capitalize()} {wr_category} {wr_time} {wr_message_link}"

def generate_message_link(server_id, channel_id, message_id):
    return f"https://discord.com/channels/{server_id}/{channel_id}/{message_id}"

def print_colour(colour, text):

    def message_red(text):
        return "\033[31m{}\033[0m".format(text)

    def message_green(text):
        return "\033[32m{}\033[0m".format(text)

    def message_blue(text):
        return "\033[34m{}\033[0m".format(text)
    
    colour_functions = {
        "R": message_red,
        "G": message_green,
        "B": message_blue,
    }
    return colour_functions.get(colour)(text)

def print_error(code):
    error_codes_dict = {
        "000": "Error 000: Unclassified Error",
        "201": "Error 201: ESC sequence found in message.",
        "301": "Error 301: Dox Detected in message.",
        "302": "Error 302: Dox Detected in name.",
        "303": "Error 303: Dox Detected in image.",
        "304": "Error 304: Ping Detected in message.",
    }
    return print_colour("R", error_codes_dict.get(code))

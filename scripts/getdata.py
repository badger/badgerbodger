""" MIT License

Copyright (c) 2022 Krishna Prajapati - @KrisPrajapati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. """

import urllib.request
import requests
from lxml import etree
from io import StringIO
import os
import datetime
import qrcode
import shutil
from lib import convert
import argparse

first_name = ""
last_name = ""
username = ""

# Parse HTML into DOM and fetch name & username
def parse_profile_data(html):
    global username
    parser = etree.HTMLParser()
    dom_root = etree.parse(StringIO(html.decode("unicode_escape")), parser)
    name_nodes = dom_root.xpath("//span[@itemprop='name']")
    username_nodes = dom_root.xpath("//span[@itemprop='additionalName']")

    if len(name_nodes) == 0 or len(username_nodes) == 0:
        print("An error occured")
        quit()

    name = name_nodes[0].text.strip() if args.name is None else args.name
    username = username_nodes[0].text.strip()

    names = name.split(" ")
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ""

    print(f"Welcome, {name}!")
    print(f"@{username}")
    print("\nCreating Badge")
    badge_filename = f"generated/badge.txt"
    os.makedirs(os.path.dirname(badge_filename), exist_ok=True)
    with open(badge_filename, "w") as badge_file:
        badge_file.write(f"UNIVERSE 2023\n{first_name}\n{last_name}\n@{username}")
        badge_file.close()


# Date format for contribution page
def dateformat(dateStr):
    date_components = dateStr.split("-")
    date = datetime.datetime(int(date_components[0]), int(date_components[1]), int(date_components[2]))
    return date.strftime("%-d %b %Y")
    
# Parse and fetch contribution graph data
def parse_contributions_data(html): 
    parser = etree.HTMLParser()
    dom_root = etree.parse(StringIO(html.decode("unicode_escape")), parser)

    #Fetch each rect element inside the svg
    
    rect_nodes = dom_root.xpath("//svg[@class='js-calendar-graph-svg']//rect")

    #Offset as latest week may be partial
    latest_week = dom_root.xpath("//svg[@class='js-calendar-graph-svg']/g/g[last()]//rect")
    week_position_offset = 7 - len(latest_week)


    # Graph has 369 days
    # however we can display only 182 days per page (i.e. 364 days)
    # so ignore the earliest 5 days

    # Writing latest 6 months to page 1
    with open(f"generated/contribution_page_1.txt", "w") as contributions_file:
        total = 0
        graph_data = ""
        start_date = rect_nodes[187+week_position_offset].xpath("string(@data-date)")
        end_date = rect_nodes[len(rect_nodes)-1].xpath("string(@data-date)")
        for i in range(187+week_position_offset,len(rect_nodes)):
            contributions = 0
            if rect_nodes[i].xpath("string(@data-count)") != "":
                contributions = int(rect_nodes[i].xpath("string(@data-count)"))
            total += contributions
            data_level = rect_nodes[i].xpath("string(@data-level)")
            graph_data+=f"\n{data_level}"
        
        contributions_file.write(f"{total} contributions between\n{dateformat(start_date)} - {dateformat(end_date)}")
        contributions_file.write(graph_data)
        contributions_file.close()


    # Writing earlier 6 months to page 2
    with open(f"generated/contribution_page_2.txt", "w") as contributions_file:
        total = 0
        graph_data = ""
        start_date = rect_nodes[4+week_position_offset].xpath("string(@data-date)")
        end_date = rect_nodes[186+week_position_offset].xpath("string(@data-date)")
        
        for i in range(4+week_position_offset,186+week_position_offset):
            contributions = 0
            if rect_nodes[i].xpath("string(@data-count)") != "":
                contributions = int(rect_nodes[i].xpath("string(@data-count)"))
            total += contributions
            data_level = rect_nodes[i].xpath("string(@data-level)")
            graph_data+=f"\n{data_level}"
        contributions_file.write(f"{total} contributions between\n{dateformat(start_date)} - {dateformat(end_date)}")
        contributions_file.write(graph_data)
        contributions_file.close()

# Generate QR code
def generate_qr_code():
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=3, border=3,)
    qr.add_data(f"https://github.com/{username}")
    png = qr.make_image()
    pngfilename = f"generated/gh_qrcode.png"
    png.save(pngfilename)
    convert.convert(pngfilename)
    os.remove(pngfilename)

#---------------------------
# MAIN PROGRAM ENTRY POINT
#---------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--handle', type=str, required=False)
parser.add_argument('--name', type=str, required=False)
args = parser.parse_args()

entered_username = input("\nEnter your GitHub username: ") if args.handle is None else args.handle
print("\nFetching Profile...\n")

profile_request = requests.get(f"http://github.com/{entered_username}")


if profile_request.status_code == 200:
    profile_html = profile_request.content
    parse_profile_data(profile_html)
    generate_qr_code()

elif profile_request.status_code == 404:
    print("Profile not found")
    quit()
else: 
    print("Error fetching profile")
    quit()


print("\nFetching Contribution Graph...")
contributions_request = requests.get(f"http://github.com/users/{entered_username}/contributions")


if contributions_request.status_code == 200:
    print("\nProcessing Contribution Graph...")
    contributions_html = contributions_request.content
    parse_contributions_data(contributions_html)

else: 
    print("Error fetching contribution graph")
    quit()

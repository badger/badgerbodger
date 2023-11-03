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
import argparse


# Date format for contribution page
def dateformat(dateStr):
    date_components = dateStr.split("-")
    date = datetime.datetime(int(date_components[0]), int(date_components[1]), int(date_components[2]))
    return date.strftime("%-d %b %Y")
    
# Parse and fetch contribution graph data
def parse_contributions_data(html): 
    parser = etree.HTMLParser()
    dom_root = etree.parse(StringIO(html.decode("unicode_escape")), parser)
    
    # Writing latest 6 months to page 1 (Week 26 to 52)
    write_contribution_file(filename="contribution_page_1.txt", start_week=26, end_week=52, dom_root=dom_root)
   
    # Writing earlier 6 months to page 2 (Week 0 to 25)
    write_contribution_file(filename="contribution_page_2.txt", start_week=0, end_week=25, dom_root=dom_root)

def write_contribution_file(filename, start_week, end_week, dom_root):
    with open(f"generated/{filename}", "w") as contributions_file:
        graph_data = ""
        contributions = 0
        start_date = first_day_of_week(dom_root,start_week)
        end_date = last_day_of_week(dom_root,end_week)

        for week in range(start_week,end_week+1):
            contributions+=contribution_count_for_week(dom_root,week)
            graph_data+=graph_levels_for_week(dom_root,week)
        
        contributions_file.write(f"{contributions} contributions between\n{dateformat(start_date)} - {dateformat(end_date)}")
        contributions_file.write(graph_data)
        contributions_file.close()

def graph_levels_for_week(dom,week):
    nodes = dom.xpath(f'//table[@class="ContributionCalendar-grid js-calendar-graph-table"]//td[@data-ix="{week}"]')
    data = ""
    for i in range(0,len(nodes)):
        data+=f"\n{nodes[i].xpath('string(@data-level)')}"
    return data

def contribution_count_for_week(dom, week):
    count = 0
    nodes = dom.xpath(f'//table[@class="ContributionCalendar-grid js-calendar-graph-table"]//td[@data-ix="{week}"]//text()')
    for i in range(0,len(nodes)):
        num = [int(s) for s in nodes[i].split() if s.isdigit()]
        count+=sum(num)
    return count

def first_day_of_week(dom,week):
    return dom.xpath(f'string((//table[@class="ContributionCalendar-grid js-calendar-graph-table"]//td[@data-ix="{week}"])[1]/@data-date)')

def last_day_of_week(dom,week):
    return dom.xpath(f'string((//table[@class="ContributionCalendar-grid js-calendar-graph-table"]//td[@data-ix="{week}"])[last()]/@data-date)')


def fetch_contribution_graph(handle):
    print("\nFetching Contribution Graph...")
    contributions_request = requests.get(f"http://github.com/users/{handle}/contributions")


    if contributions_request.status_code == 200:
        print("\nProcessing Contribution Graph...")
        contributions_html = contributions_request.content
        parse_contributions_data(contributions_html)

    else: 
        print("Error fetching contribution graph")
        quit()

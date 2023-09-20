import time
import badger2040
import badger_os

CONTRIBUTION_GRAPH_PAGE = 0 #page 0 = latest 6 months; page 1 = previous 6 months

class ContributionPage(object):
    # Each contribution page contains title, subtitle and graph data
 def __init__(self, title, subtitle, contribution_data):
    self.title = title
    self.subtitle = subtitle
    self.contribution_data = contribution_data

#Drawing contribution graph
def draw_contribution_graph(display):
    #Clearing the display
    display.pen(15)
    display.clear()
    
    display.pen(0) # Black
    display.thickness(2)
    display.font("sans")
    
    page_data = contribution_pages[CONTRIBUTION_GRAPH_PAGE]
    
    # Drawing title text
    display.text(page_data.title, 8,16,0.6)
    # Drawing subtitle text
    display.text(page_data.subtitle, 8,32,0.5)
    
    # Drawing graph
    
    contributions_of_day = page_data.contribution_data
    
    # 26 weeks (6 months)
    for week in range(26):
        
        # 7 days each week
        for day_of_week in range(7):
            
            # Calculating position of each cell
            x = 8 + (week * 11)
            y = 50 + (day_of_week * 11)
            index = (week*7)+day_of_week
            
            
            # Cell value can be 0-5;
            # 0 being no contributions, color with lightest pen (15)
            # 5 being highest contributions, color with darkest pen (0) 
            display.pen(15 - ((contributions_of_day[index]+1) * 3))
            display.rectangle(x, y, 9, 9)


# Open the contributions data files corresponding to the pages
contribution_files = ["contribution_page_1.txt","contribution_page_2.txt"]
contribution_pages = []

# Load file data
for filename in contribution_files:
    try:
        file = open(filename, "r")
    except OSError:
        # If file does not exist, create a default file
        try:
            # Import the specific module needed and create file
            if filename == "contribution_page_1.txt":
                import contribution_page_1
                with open(filename, "wb") as f:
                    f.write(contribution_page_1.data())
                    f.flush()
                    time.sleep(0.1)
                del contribution_page_1
                file = open(filename, "r")
            elif filename == "contribution_page_2.txt":
                import contribution_page_2
                with open(filename, "wb") as f:
                    f.write(contribution_page_2.data())
                    f.flush()
                    time.sleep(0.1)
                del contribution_page_2
                file = open(filename, "r")
        except ImportError:
            pass
    page_title = file.readline()
    page_subtitle = file.readline()
    contribution_data = []
    
    # Loading 182 days (26 weeks / 6 months)
    for x in range(182):
        # Read each line for each day's value
        contribution_of_day_str = file.readline()
        # If day's data does not exist, it may be partial week, set the value to -1
        contribution_of_day = int(contribution_of_day_str) if len(contribution_of_day_str)>0 else -1
        # Append the day's data 
        contribution_data.append(contribution_of_day)
        
    # Append the page data
    contribution_pages.append(ContributionPage(page_title, page_subtitle, contribution_data))

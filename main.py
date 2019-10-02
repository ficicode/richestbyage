# THIS PROGRAM WILL ANALYZE DATA FROM THE RICHEST PEOPLE IN THE WORLD
# FOR EACH AGE FROM 21 TO 100 INCLUSIVE
# DATA: https://www.businessinsider.com/richest-person-every-age-2018-8
# Anthony Magnafici 09.26.19



from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pycountry as pc
import numpy as np

# grab website
page = requests.get("https://www.businessinsider.com/richest-person-every-age-2018-8")

# create BeautifulSoup object from page contents with HTML parser
soup = BeautifulSoup(page.content, "html.parser")

# grab each slide (div class = "slide-layout clearfix") as a ResultSet
slides = soup.find_all(class_ = "slide-layout clearfix")





# THE FOLLOWING BLOCK OF CODE GRABS THE FULL TITLE FROM <div class = "slide-title-text">
# AND PARSES THE INTEGER (AGE) AND STRING (FULL NAME) FROM THE FULL TITLE STRING

# grab all full titles from the slides ResultSet
full_titles = []
for i in range(0, 80) :
    full_titles.append(slides[i].find(class_ = "slide-title-text").string)

# parse age (int) from full_titles list
ages = []
for i in range(0, 80) :
    ages.append(int(re.search(r"\d+", full_titles[i]).group()))
    
# THE FOLLOWING BLOCKS OF CODE WILL PARSE THE FULL NAME AS A STRING FROM THE FULL
# TITLE STRING

# this first loop will find the first space after the colon, indicating the beginning
# of the string we want to extract, containing the full name
string_begin = []
for i in range(0, 80) :
    string_begin.append(full_titles[i].find(" ")) # append index as integer for start

# this loop will parse the string using curr_start, storing in full_name list
full_name = []
for i in range(0, 80) :
    curr_start = string_begin[i] + 1 # start the substring one index past the space
    full_titles_string = str(full_titles[i]) # grabs full title one at a time
    full_name.append(full_titles_string[curr_start : len(full_titles_string)])
    # appends string starting from curr_start to the end of the string







# THE FOLLOWING BLOCKS OF CODE WILL GRAB THE FOUR <p> TAGS WITHIN EACH SLIDE. THESE
# WILL BE USED LATER TO GRAB INFORMATION ABOUT NET WORTH, COUNTRY, SOURCE OF WEALTH,
# AND POSITION.

# grabbing all four <p> tags from the slides ResultSet
p_tags = []
for i in range(0, 80) :
    p_tags.append(slides[i].find_all("p")) # append all four <p> tags to p_tags





# THE FOLLOWING BLOCKS OF CODE WILL PARSE THE NET WORTH FROM THE <p> TAG WITHIN
# THE SLIDE. WE NEED TO FIND THE INTEGER OR FLOAT WITHIN THE STRING, THEN DETERMINE
# WHETHER IT IS MILLION OR BILLION BY PARSING THE STRING. AFTER THESE TWO PARSES,
# WE NEED TO POPULATE A LIST WITH A SINGLE INTEGER VALUE FOR NET WORTH

# grabbing the Net Worth full string from the p_tags list
net_worth_full = []
for i in range(0, 80) :
    net_worth_full.append(str(p_tags[i][0])) # append first <p> tag to net_worth_full

# grabbing the net worth and converting to a float with two decimal places
net_worth_float = []
for i in range(0, 80) :
    index_begin = net_worth_full[i].find("$") + 1 # begin at dollar sign
    index_end = net_worth_full[i].find(" ", index_begin) # end at space after value
    net_value = (net_worth_full[i][index_begin : index_end]) # get value as string
    float_value = "%.2f" % float(net_value) # convert substring into float w/ 2 decimals
    net_worth_float.append(float_value) # append the float to net_worth_float


# checking for presense of billion or million within net_worth_full to create a
# list of Boolean values which are useful for formatting an integer value
is_million = []
for i in range(0, 80) :
    is_million.append("million" in net_worth_full[i])


# using net_worth_float and is_million to create net_worth_int, which will contain
# net worth values as an integer
net_worth_int = []
for i in range(0, 80) :
    if is_million[i] == True :
        multiply_mil = float(net_worth_float[i]) * 1000000.00
        if "999999" in str(multiply_mil) : # this will handle any lossy conversions
               multiply_mil += 1
        net_worth_int.append(int(multiply_mil))
    else :
        multiply_bil = float(net_worth_float[i]) * 1000000000.00
        if "999999" in str(multiply_bil) : # this will handle any lossy conversions
               multiply_bil += 1
        net_worth_int.append(int(multiply_bil))





# THE FOLLOWING CODE BLOCKS WILL PARSE THE COUNTRY FROM THE <p> TAG WITHIN THE SLIDE

# grab the full country tag from p_tags and store as a string
country_full = []
x = 0
for i in range(0, 80) :
    country_full.append((p_tags[i][1]).getText()) # append second <p> tag to net_worth_full

# a rough grab of the country
countries_untrim = []
end_string = len(str(country_full[i].find)) - 4
beginning_string = country_full[i].find("</strong>") + 10
x = 0
for i in range(0, 80) :
    countries_untrim.append(country_full[i][beginning_string:])

# cleaning up countries_untrim and storing in countries
countries = []

for i in range(0, 80) :
    countries.append(countries_untrim[i].replace("</p>", ""))






# THE FOLLOWING CODE WILL PARSE THE SOURCE OF WEALTH FROM THE <p> TAG WITHIN THE SLIDE

# parsing the full text from the <p> tag
wealth_full = []

for i in range(0, 80) :
    wealth_full.append((p_tags[i][2]).getText())

# cleaning up the data in wealth_full to only store the source of wealth
source_of_wealth = []

trim_len = len("source of wealth: ") # this is the string we want to remove

for i in range(0, 80) :
    source_of_wealth.append(wealth_full[i][trim_len : ])


    



# THE FOLLOWING CODE WILL PARSE THE POSITION FROM THE <p> TAG WITHIN THE SLIDE

# appending the full position string from the final <p> tag to position_full
position_full = []
for i in range(0, 80) :
    position_full.append((p_tags[i][3]).getText())

# cleaning up the data in position_full to only store the position without the
# name of the company where applicable
position_untrim = []
position = []

trim_len = len("Position:")

# trimming "Position:" from string
for i in range(0, 80) :
    position_untrim.append(position_full[i][trim_len : ]) 
    # if a comma isn't found
    if position_untrim[i].find(",") == -1 :
        # if the string begins with a space, append without first char
        if position_untrim[i].startswith(" ") :
            position.append(position_untrim[i][1 :])
        # else append the full string
        else :
            position.append(position_untrim[i])
    # if a comma is found
    else :
        # store the index of the comma found
        comma_len = position_untrim[i].index(",")
        # if the string begins with a space, append without first char
        if position_untrim[i].startswith(" ") :
            position.append(position_untrim[i][1 : comma_len])
        # else append the full string
        else :
            position.append(position_untrim[i][: comma_len])



    



# THE FOLLOWING CODE BLOCK WILL CONSTRUCT A PANDAS DATAFRAME FROM OUR LISTS OF DATA
data = pd.DataFrame({"Age" : ages,
                     "Name" : full_name,
                     "Net Worth" : net_worth_int,
                     "Country" : countries,
                     "Source of Wealth" : source_of_wealth,
                     "Position" : position})

# convert and save the data DataFrame as as CSV file locally
data.to_csv("Richest by Age - Scrape CSV.csv", index = False)





# PLOTTING VARIOUS DATA FROM THE data PANDAS DATAFRAME


# these imports will be used throughout the following code blocks
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch



# DISPLAY COUNTRY (X AXIS) AND NUMBER OF PEOPLE FROM COUNTRY (Y AXIS) AS A BAR
# Only displaying countries with more than 1 richest person
unique_country = data["Country"].unique()
unique_count = []

for i in range(0, len(unique_country)) : # construct list 0's with length 24
    unique_count.append(0)

for i in range(0, 80) : # comparing all 80 people
    for y in range(0, 25) : # with the 24 unique countries
        if data["Country"][i] == unique_country[y] : # if country name is found
            unique_count[y] = int(unique_count[y]) + 1 # increment count by 1
            break # break if country is found to avoid unneeded searches

unique = pd.DataFrame({"Country" : unique_country,
                       "Number of Richest" : unique_count})

unique_two = unique[unique["Number of Richest"] > 2]

plt.bar(unique_two["Country"], unique_two["Number of Richest"], width = 0.7)

x_labels = list(unique_two["Country"])
plt.xticks(rotation = 25)

plt.xlabel("Country")
plt.ylabel("Number of Richest")
plt.title("Number of Richest People Per Age in Each Country (n > 2)")
# enable grid for visibility
plt.grid(True)
# getting the figure manager and setting the window to open in full screen
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()





# DISPLAY AGE GROUPS AND THEIR COMBINED WEALTH AS A PIE CHART
# Groups will be 21-30, 31-40, 41-50, etc.
# establish age groups list
age_groups = ["21-30", "31-40", "41-50", "51-60",
              "61-70", "71-80", "81-90", "91-100"]
net_combined = [0, 0, 0, 0,
                0, 0, 0 ,0] # create list with predetermined size

for i in range(0, 8) : # for 8 groups of 10
    for y in range(0, 10) : # for 10 values in each group
        net_combined[i] += data["Net Worth"][79 - (10*i) - y] / 10000000
        # add previous list value to found value, divide by 100000 to avoid int64

total_net = sum(net_combined)

# format the combined net worths from net_combined for readability
net_form = []
for i in range(0, len(net_combined)) :
    toInt = int(net_combined[i])
    if toInt < 10000 :
        toString = str(net_combined[i])
        formatted = str(toString[0:2] + "." + toString[2:4] + "B")
        net_form.append(formatted)
    else :
        toString = str(net_combined[i])
        formatted = str(toString[0:3] + "." + toString[3:5] + "B")
        net_form.append(formatted)

# construct a pandas DataFrame
combined_net = ({"Age Group" : age_groups,
                 "Combined Net Worth" : net_combined,
                 "Formatted Net" : net_form})

plt.pie(x = combined_net["Combined Net Worth"], labels = combined_net["Formatted Net"], autopct = "%1.1f%%")
plt.legend(labels = combined_net["Age Group"], title = "Age Groups", loc = "upper left")
plt.title("Richest Combined Age Groups")
# getting the figure manager and setting the window to open in full screen
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()





# DISPLAY AGE (X AXIS) AND NET WORTH AS BILLIONS (Y AXIS) AS A SCATTER PLOT
# construct scatter plot using the data DataFrame

# create boolean list to determine net worths larger than 80 billion
rich_bool = data["Net Worth"] / 1000000000 > 80

# find the index of each True value, indicating >80B net worth
rich_index = [i for i, x in enumerate(rich_bool) if x]

# using rich_index, append Ages of people who have >80B net worth
rich_age = []
for i in rich_index :
    rich_age.append(data["Age"][i])

# using rich_index, append Names of people who have >80B net worth
rich_name = []
for i in rich_index :
    rich_name.append(data["Name"][i])

# using rich_index, append Net Worth of people who have >80B net worth
rich_net = []
for i in rich_index :
    rich_net.append(data["Net Worth"][i] / 1000000000)

# construct richest DataFrame which stores Name and Net Worth of people
# whose net worth is >80B
richest = pd.DataFrame({"Name" : rich_name,
                        "Net Worth" : rich_net,
                        "Age" : rich_age})

# sort richest DataFrame by the Net Worth column, descending inplace
richest.sort_values("Net Worth", ascending = False, inplace = True)
# reset the index values for the DataFrame inplace
richest.reset_index(drop = True, inplace = True)

# append constructed Name and Net Worth strings to legend_labels
legend_labels = []
for i in range(0, len(list(richest["Net Worth"]))) :
    legend_labels.append(richest["Name"][i] + " (" + str(richest["Age"][i]) + "): " + str(richest["Net Worth"][i]) + "B")

# creating individual proxy artists for legend using legend_labels
first_color = "red"
second_color = "blue"
third_color = "cyan"
fourth_color = "purple"
first_richest = mpatch.Patch(color = first_color, label = legend_labels[0])
second_richest = mpatch.Patch(color = second_color, label = legend_labels[1])
third_richest = mpatch.Patch(color = third_color, label = legend_labels[2])
fourth_richest = mpatch.Patch(color = fourth_color, label = legend_labels[3])

# color each point on the scatter plot that is >80B
# create color_list to plot each point individually
color_list = [first_color, second_color, third_color, fourth_color, "green"]

# import math for square root
import math

# set scale for each point on the scatter plot
scale = []
for i in range(len(data["Net Worth"])) :
    # assign the value found divided by one billion to num
    num = data["Net Worth"][i] / 1000000000
    # append the square root of num * 80 to scale list
    scale.append(math.sqrt(num*80))
    
# for each value in data["Net Worth"] column
for i in range(0, 80) :
    num = data["Net Worth"][i] / 1000000000
    net_list = list(richest["Net Worth"])
    
    # if the person is one of the richest, plot using their color in color_list
    # this will be nested in a try-except to handle ValueError
    try :
        plt.scatter(data["Age"][i], num, s = scale[i], c = color_list[net_list.index(num)], edgecolors = "black")
    # plot using the default color in color_list at last index after ValueError
    except :
        plt.scatter(data["Age"][i], num, s = scale[i], c = color_list[-1], edgecolors = "black")

# set scatter plot title and labels
plt.xlabel("Age")
plt.ylabel("Net Worth")
plt.title("Richest People by Age")

# create legend using the four proxy artists as handles
plt.legend(handles = [first_richest, second_richest,
                      third_richest, fourth_richest], loc = "upper right", title = "Richest")
# getting the figure manager and setting the window to open in full screen
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()




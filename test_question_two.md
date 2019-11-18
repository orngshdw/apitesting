# Question Two
This file lists the test cases for Question two:
Write all the test cases you can think of to validate the following screen

*Note: hovering over the bars will show a tooltip*  

# Test cases  
## Dropdowns & options  
1. "Unit" & "All days" dropdowns can be changed, applied changes persist on refesh/relog and Volumes chart updates correctly
  * Date ranges to cover are: past to present, past to future, future dates only, and a single date.
2. Left and right arrow next to the All days can be changed. 
2. Filters panel on right can be shown and hidden  
3. Filters dropdowns can be individiually changed from 0 selected to an x amount selected & the Volumes chart updates after every filter change  
4. Filters can be reset  

## Chart Properties  
1. Axis for Volumes & Date are within expected range and are at the correct interval  
2. Summary values on top of the stacked bar chart (daily average scheduled/completed appts & total scheduled/completed volume) show expected numbers and labels. Numbers should be present and correct as chart updates.  
3. Maximum number of stack bars per date equals the count of ranges in the legend (plus schedule & completed)
4. Legend colors at bottom are expected 
5. Legend colors matches and same as what is seen for each stacked bar chart  
6. Tooltip should appear when hovering over a bar for a date and disappear when user is not hovering over a bar 


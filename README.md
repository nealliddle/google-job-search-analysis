# Google Job Search Analysis

### Purpose:
This script crawls Google's job search functionality. The data is then exported as a .CSV file.  

### Use:
In order to do your own search just change the url based on your own search and run the script.

*Eg.  
https://www.google.com/search?q=data+scientist+USA&oq=data+sc&aqs=chrome.0.69i59l2j0i433i457j69i59j69i57j69i61l2j69i60.1954j1j1&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwioy4DD3I_uAhVWhlwKHXWZDPAQutcGKAB6BAgFEAQ&sxsrf=ALeKk01QJ1N0hCq5E4yNdSVpAocamk9jcA:1610225255727#htivrt=jobs&htidocid=eaEAKiT_pHnjJGlAAAAAAA%3D%3D&fpstate=tldetail*

Once complete the data will be placed in a .CSV file in the same folder as the script.

### Common Issues:
* Running this script too often will lead to a 429 request status. This means you've ran it too often. Wait and run again later. This is more of an issue when coding than actually using as one has to run it quite often.  
* When opening file in Excel, use Data > From Text/CSV > File Origin = 605001: Unicode(UTF-8)



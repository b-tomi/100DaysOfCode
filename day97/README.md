# Day 97 - Professional Portfolio Project - Python Automation
## Assignment: Custom Automation
Automate some aspect of your life using Python.
## Assignment instructions
You've learnt about automation with Python and Selenium. It's your turn to get creative and automate some aspect of your life using what you have learnt.

This could be an aspect of your job, your schoolwork, your home, your chores. Think about your week and everything that you do on a regular basis, when do you feel like a robot? Which jobs do you find tedious and boring? Can it be automated?

Here are some stories for inspiration:  
Automate an email to your boss to ask for a raise every 3 months. =)  
Automate your lights so they switch on when your phone is within the radius of your house.  
Automatically organise the files in your downloads folder based on file type.  
Automate your gym class bookings.  
Automate your library book renewals.  
[Automate your job.](https://www.reddit.com/r/learnpython/comments/boywle/what_work_activity_have_you_automated/)  
[Automate your home chores.](https://www.reddit.com/r/Python/comments/9lp1mn/so_what_have_you_automated_at_home/)

Personally, I had a job in a hospital where I had to arrange all the doctors' shifts in my department (normal day, long day, night shift). It would depend on when they wanted to take annual leave/vacation and the staffing requirements. It started out in an Excel spreadsheet, by the time I was done with it, it was fully automated with Python and doctors were able to view a live version of the rota to see when they can take time off. The code took an evening to write and it saves me 3 hours per week. (More time to watch Netflix and eat ice cream).

Once you're done with the assignment, let us know what you automated in your life and maybe it will inspire another student!

---
### Notes:
This is a fairly short script that I wrote to simplify the management of language learning podcast episodes.

Automates the following actions for several podcasts:
* Looks at the local drive and finds the number of the most recent episode
* Retrieves a list of newer episodes from the relevant RSS feed
* Downloads all the newer episodes to the local drive
* Authenticates with Google Drive using OAuth2.0 (utilizing [PyDrive](https://pypi.org/project/PyDrive/))
* Uploads all the newer episodes to the appropriate Google Drive folder...

...which then I can conveniently access from my mobile devices and listen to the episodes using my preferred audiobook player.

---

*Make sure to update config.py and replace the two JSON files with your own from the Google API Console.*

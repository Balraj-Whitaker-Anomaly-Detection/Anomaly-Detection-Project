# Team Anomaly Detection Project
## About Project:
### Description:
In this project a teammate and I will be answering questions presented in an email from our boss concerning codeup curriculum traffic.

### Project Goal:
The goal of this project is to answer the questions in the email and return a email with the answers, the requested slide, and the link to this github repo.

### Email from Boss:
Hello,

I have some questions for you that I need to be answered before the Board meeting on Monday evening. I need to be able to speak to the following questions. I also need a single slide that I can incorporate into my existing presentation (Google Slides) that summarizes the most important points. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.

Which lesson appears to attract the most traffic consistently across cohorts (per program)?
Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
What topics are grads continuing to reference after graduation and into their jobs (for each program)?
Which lessons are least accessed?
Anything else I should be aware of?
Thank you,


### Additional Info:
Data was acquired from Codeup's SQL database and additional contextual info was gathered from alumni.codeup.com.

The Board meeting on Monday evening that the slide will be presented in is to discuss the general state of things and update the stakeholders (What’s the direction we are going in, and is it a good one?).

## Data Dictionary 
A list of the variables in the dataframe and their meaning. 

| Variable       | Description                         |
| -------------- | ----------------------------------- |
|     path          | endpoint |
|user_id| user id (unique per student/staff|
|cohort_id|id unique to each class|
|program_id|1: php, 2: java, 3: data_science, 4: front_end|
|ip|ip address|
|name|name of cohort (class)|
|slack|slack group name (should be same as name)|
|start_date|date started cohort|
|end_date|date graduated|
|created_at|date log created|
|updated_at|date log edited|
|program|php, java, and front end belong to Web Dev and data_science belongs to data science|
|staff|True = staff, False = not staff|
|days_after_grad|number of days after graduation|
|module_1|first half of path|
|module_2|second half of path|
|is _active|1 = yes, 2 = no|

## Plan 
Joann will answer 1,2,3,7
Chloe will answer 4,5,6,8

After answering questions, create slide and email response. 

## Deliverables 
- Email response
- Slide for board meeting
- GitHub repo
- README.md

## Conclusion (Email Replies):
1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
The Javascript -i lesson appears to attract the most traffic across all cohorts.

2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
Bayes had the most frequent access to the curriculum of all data science cohorts. It looks like SQL an classification modules are the most popular among all data science cohorts. The Classification module in the curriculum was accessed significantly more by Darden than any other cohort.

3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
User ID 278 only accessed the curriculum 3 times while active in the program and was in the Voyageurs cohort for Java between 5-29-2018 and 10-11-2018
User ID 832 only accessed the curriculum 2 times while active in the program and was in the Jupiter cohort for Java between 9/21/2020 and 3/30/2021
User ID 679 only accessed the curriculum 1 time while active in the program and was in the Darden cohort for Data Science between 7/13/2020 - 1/12/2021
Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
I did find suspicious activity. I looked at which IPs looked at the most lessons in a day, and I saw that on 2019-03-03 user 341 (using IP address 204.44.112.76), looked at 156 pages in 6 seconds. This person is from the Zion Web Dev cohort. Each page appears to have been accessed only once on that day. This activity is indicative of web scraping. This user appears to have only done this once, and currently interacts with the curriculum in a normal manor.

4. Another suspicious user is user_id 88 from the Glacier cohort. They have the most activity of all users and are not a staff member. Their activity seems to be persistant since their cohort in 2015, with significant spikes in activity every few months. There is more than one IP associated with this user.

Other user ids with significant amounts of activity are: 146, 80, 18, and 291. Some or all of these may be staff, so more exploration is needed to determine if these users are suspicious or not.

Summary:

Supicious IP from 2019: 204.44.112.76 Current supicious user: user id 88 Potential supicious user ids that require additional time to explore: 146, 80, 18, and 291

5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
I see evidence that users from one program could not access lessons in another program between 2019-04-13 and 2019-08-15.

A Web Dev student (user_id: 220) from the Wrangell cohort accessed the data-science curriculum on 2019-04-13 but another Web Dev staff member (user_id: 410) didn't access the data science curriculum until 2019-08-15.

This doesn't appear to have happened before since Codeup didn't have a Data Science program in 2018. That's why there isn't activity for Data Science in that year. The first cohort started in January 2019. There's a notable spike on a day at the end of 2020 that is worth looking into as well as what looks like March 2021.

Summary: The ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) appears to have been down between the dates 2019-04-13 and 2019-08-15, but not before or after.

6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?

Top 5 Lessons Accessed by Web Dev Alumni:

javascript-i
spring
html-css
java-iii
java-ii

Top 5 Lessons Accessed by Data Science Alumni:

sql/mysql-overview
classification/overview
anomaly-detection/overview
fundamentals/intro-to-data-science
1-fundamentals/1.1-intro-to-science

7. Which lessons are least accessed?
Several pages are only accessed once. It's difficult to tell if its an actual lesson, or a page that was not intended for student use.

8. Anything else I should be aware of?
Current Data Science students are accessing the same lessons as alumni. The only difference is that the alumni are accessing anomaly detection and not regression.

Current Web Dev students are accessing the same lessons as alumni. The only difference is that the alumni are accessing spring and not toc.

Summary: Codeup is mostly focusing on the subjects that alumni need to revisit the most. Codeup curriculum appears to be focused in the right direction.


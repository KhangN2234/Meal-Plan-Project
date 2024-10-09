# MyMealPrep
![Example screenshot](burger.webp)

## Table of Contents
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)


## General Information
- Created by Joseph Bond, Lucas Garcia, Mark Nardone, Khang Ngo, Sean Kuge
- This is a web app centered around making meal prepping easy. A lot of us face the issue of wanting to meal prep but being scared off due to its difficulty. This app aims to solve that and enable people looking to improve their health, fitness, and finances while improving their quality of life.

## Technologies Used
- Flask 3.0.3
- Edamam Recipe Search API v2


## Features
List the ready features here:
- Welcome Page
	-  Users can get a full overview of the app and its features from a comfortable welcome page.
	-  Story: Welcome Page
- Account Creation System
	-  You can make an account that is able to store your username and password.
	-  Story: Account Creation
- Recipe Search Page
	-  Can't seem to find that recipe you saw earlier? Just search for it and you'll be there in no time! 
	-  Story: Recipe Search Page
- Dynamic Recipe Scaling System
	-  If a user doesn't have the specified quantity of ingredients, they can scale the entire recipe proportionally to whatever amount of ingredients they have.
	-  Story: Recipe Scaling
- Save Your Favorite Meals
	-  Love the meal your looking at? Save it for later.
	-  Users will have the ability to flag meals as "saved for later"
	-  Story: Saving Favorite Meals


## Sprint 1 (September 23rd - October 4th)
Contribution:

Khang Ngo: Made the Welcome Page for the user, along with the navigation bar. Along with refactoring all the routes from app.py to routes.py.
- Jira Task CP-14: Create a mockup of the Project
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-14 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/1cb6394311ceb6aea5b7e7d9e8b6ccef4de2ad72
- Jira Task CP-5: Create the Welcome Page Route in Flask (Backend)
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-5 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/pull-requests/2 
- Jira Task CP-3: Implement HTML Welcome Page
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-3 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/b72bd5395967b032358ce9d2300dfd91fc8f9d64 
- Jira Task CP-15: Implement CSS Welcome Page
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-15 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/3f5544d185b976c37f4cde7c113ec04167fa4c6f 
- Jira Task CP-4: Make the UI look better
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-4
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/pull-requests/10
- Jira Task CP-77: Add some animation to UI
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-77  
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/f6aafc0b30ebfe1b139d6201b2a2dd7055794f0a 

Joseph Bond: created the function for scaling down specific ingredients for recipes. 
- Jira Task CP-74: Conduct further research of HTML and Python
	-Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-74
	-bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-74-cunduct-further-research-of-html-a
-Jira Task CP-30 Design UI for Ingredient Adjustment
	-Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-30
	-bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/feature%2FCP-30-design-ui-for-ingredient-adjustmen
-Jira Task CP-32 Develop Basic Algorithm for Scaling Recipes
	-Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-32
	-bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-32-develop-basic-algorithm-for-scalin
-Jira Task CP-73 Integrate Recipe Scaling with the core functionality of app
	-Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-73
	-bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-73-integrate-recipe-scaling-with-the-
-Jira Task CP-35 Unit Testing for scaling algorithm (To-Do)

Mark Nardone: Made and designed the Signup.html that allows users to create an account. Along with that made a profile.html with profile basic profile features. Also worked on the app.py
- Jira Task CP-54: Account Creation UI
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-54
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/commits/ea5a613a516a74184f48799ef6ebbffc63667cec
- Jira Task CP-55: Profile Creation
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-55
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/7



## Next Steps
- Khang: Make an option for user to select a type of diet for their preferred meal.
- Joseph: Add a feature that tracks the calorie intake for user based on recipes made.
- Mark: Tie the account creation to the profile and make a log in feature.






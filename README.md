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
	- Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-74
	- bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-74-cunduct-further-research-of-html-a
- Jira Task CP-30 Design UI for Ingredient Adjustment
	- Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-30
	- bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/feature%2FCP-30-design-ui-for-ingredient-adjustmen
- Jira Task CP-32 Develop Basic Algorithm for Scaling Recipes
	- Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-32
	- bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-32-develop-basic-algorithm-for-scalin
- Jira Task CP-73 Integrate Recipe Scaling with the core functionality of app
	- Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-73
	- bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/commits/branch/CP-73-integrate-recipe-scaling-with-the-
- Jira Task CP-35 Unit Testing for scaling algorithm (To-Do)

Mark Nardone: Made and designed the Signup.html that allows users to create an account. Along with that made a profile.html with profile basic profile features. Also worked on the app.py
- Jira Task CP-54: Account Creation UI
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-54
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/commits/ea5a613a516a74184f48799ef6ebbffc63667cec
- Jira Task CP-55: Profile Creation
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-55
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/7

Lucas Garcia: Designed and implemented search.html page. Set up project's api integration.
- Jira Task CP-76: Configure search result data displayed
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-76
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/feature/CP-76-configure-search-result-data-displ
- Jira Task CP-75: Link search page to rest of app
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-75
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/CP-75-link-search-page-to-rest-of-app
- Jira Task CP-39: Link search page to rest of app
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-39
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/feature/CP-39-create-search-page-route-in-flask
- Jira Task CP-42: Design Page Layout
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-42
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/CP-42-design-page-layout
- Jira Task CP-40: Create Result Filtering Interface
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-40
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/feature/CP-40-create-result-filtering-interface
- Jira Task CP-41: Write Unit Tests For Page
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-41
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/CP-41-write-unit-tests-for-page
- Jira Task CP-38: Implement CSS / HTML For Search Page
	-  Jira: https://cs3398-europa1-f24.atlassian.net/browse/CP-38
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/branch/CP-38-implement-css---html-for-search-pa

## Next Steps
- Khang: Make an option for user to select a type of diet for their preferred meal.
- Joseph: Add a feature that tracks the calorie intake for user based on recipes made.
- Mark: Tie the account creation to the profile and make a log in feature.
- Lucas: Expand on search page to add shopping list functionality



## Sprint 2 (October 14th - November 4th)
Contribution:

Khang Ngo: Made the Calendar Page for the user.
- Jira Task Scrum-95: Make the UI more appealing
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-95
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/27 
- Jira Task Scrum-83: Refactor Routes
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-83  
	-  Bitbucket:https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-83-refactor-the-routes.py (NO PULL REQUEST NEEDED, MERGED TO MY OWN CODE)
- Jira Task Scrum-81: Implement multiple recipes
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-81 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-81-display-multiple-recipes (NO PULL REQUEST NEEDED, MERGED TO MY OWN CODE)
- Jira Task Scrum-78: Functional CSS and HTML
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-78
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-78-functional-css-and-html (NO PULL REQUEST NEEDED, MERGED TO MY OWN CODE)
- Jira Task Scrum-79: Save Recipes
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-79 
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-79-save-recipes (NO PULL REQUEST NEEDED, MERGED TO MY OWN CODE)
- Jira Task Scrum-102: Display recipes from account
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-102  
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-102-display-the-recipes-from-accou (NO PULL REQUEST NEEDED, MERGED TO MY OWN CODE)
- Jira Task Scrum-82: Make a diet system in Search
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-82 
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/15  

Joseph Bond: Made the Calorie tracking page.
- Jira Task SCRUM-35: Unit Testing for Scaling Algorithm
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-35
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-35-unit-testing-for-scaling-algori/
- Jira Task SCRUM-97: Implement User Input box for logging meal calories
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-97
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-97-implement-user-input-form-for-l/
- Jira Task SCRUM-96: create Logic for tracking meals and their calories
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-96
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-96-create-database-model-for-track/
- Jira Task SCRUM-100: create daily calorie goal entry option:(TO-DO)
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-100
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-100-create-daily-calorie-goal-entr/
- Jira Task SCRUM-98: Create Daily Calorie Summary Logic:(TO-DO)
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-98
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-98-create-daily-calorie-summary-lo/
- Jira Task SCRUM-101: implement logic to give calorie intake recomendations based on daily calorie goal(To-DO)
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-101
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-101-implement-logic-to-give-calori/
- Jira Task SCRUM-99: write unit tests for calorie tracker logic:(TO-DO)
	- Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-99
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/src/SCRUM-99-write-unit-tests-form-calorie-t/

Mark Nardone: Make a profile creation and edit system
-Jira Task SCRUM-86: Firebase Integration
	- Jira https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-86
	- Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/pull-requests/18
	
-Jira Task SCRUM-84: Login and Out Feature
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-84
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/pull-requests/21

- Jira Task SCRUM-88: Customizable Profile
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-88
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/meal-project/pull-requests/30
	
- Jira Task SCRUM-87: Add comment functionality
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-85
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/feature/SCRUM-85-add-comment-functionality

Lucas Garcia: Set up functional ingredient shopping page with pdf export. Added spellcheck to search feature.
- Jira Task SCRUM-53: Design shopping list layout
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-53
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-53-design-shopping-list-layout
- Jira Task SCRUM-51: Create Saved Recipe Ingredient Addition / Consolidation
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-51
	-  Bitbucket: https://bitbucket.org/%7B%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/feature/SCRUM-51-create-saved-recipe-ingredient-
- Jira Task SCRUM-52: Implement HTML / CSS for Shopping List Page
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-52
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-52-implement-html---css-for-shoppi
- Jira Task SCRUM-90: Create interface with search page to 'add to shopping list'
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-90
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/feature/SCRUM-90-create-interface-with-search-pa
- Jira Task SCRUM-89: Create function exporting shopping list as pdf
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-89
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D
- Jira Task SCRUM-93: Add spellcheck functionality
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-93
	-  Bitbucket: https://bitbucket.org/%7B%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-93-add-spellcheck-functionality

## Next Steps
- Khang: Add more functionality to the Calendar System like a delete, help overhaul and update UI elements, and add proper months and year rather than just one week.
- Joseph: add daily calorie goal feature to calories page. begin working on food prep reminders feature, adjust UI for scaling algorithm and calorie tracker.
- Mark: Add a home page and add more profile options to its page.
- Lucas: Continue to work on getting web hosting working. Start work on social media aspects of app. (Comments, likes, further profile features)




## Sprint 3 (November 11th - December 2)
Contribution:

Khang Ngo: Made the Calendar Page for the user.
- Jira Task Scrum-107: Sign In/Sign Up UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-107
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/33
- Jira Task Scrum-110: Recipe Search UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-110  
	-  Bitbucket:https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/37

- Jira Task Scrum-109: Recipe Scaling UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-109 
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/51

- Jira Task Scrum-112: Nav Bar
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-112
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/56

- Jira Task Scrum-111: Cart UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-111 
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/47

- Jira Task Scrum-108: Calendar UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-102  
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/44

- Jira Task Scrum-131: Restore Tracker UI
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-82 
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/39

- Jira Task Scrum-132: Share button
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-82 
	-  Bitbucket: https://bitbucket.org/%7B14accbf2-0e99-4271-b4d3-4fe97e4971c1%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/pull-requests/58 
	

Lucas Garcia: Made the social page, profile page, and implemented social functionality.
- Jira Task Scrum-116: Design profile page layout
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-116
	-  Bitbucket: https://bitbucket.org/%7B%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-116-design-profile-page-layout
	
- Jira Task Scrum-117:Implement posts submission system
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-117
	-  Bitbucket: I think this branch got deleted by my accidental clicking of the checkbox udring the pull request. The pull request still exists.

- Jira Task Scrum-120: Implement friends system
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-120
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/feature/SCRUM-120-implement-friends-system

- Jira Task Scrum-118: Implement post displaying from database system
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-118
	-  Bitbucket: https://bitbucket.org/cs3398-europa-f24/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-118-implement-post-displaying-from

- Jira Task Scrum-119:Implement bio changes as posts
	-  Jira: https://cs3398-europa-fall24.atlassian.net/browse/SCRUM-119
	-  Bitbucket: https://bitbucket.org/%7B%7D/%7B315ae11b-9fcd-47ba-9242-cfc4f4b9d261%7D/branch/SCRUM-119-implement-bio-changes-as-posts




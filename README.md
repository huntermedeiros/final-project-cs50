# CS:50 Final Basic Social Media App
#### Video Demo:  https://www.youtube.com/watch?v=2QjU0_UcH_U
#### Description:
  This is my final project for CS:50. It is basic web based social media app using Flask. 
#### Reasons:
  The reason I chose to make this application as my final project for CS:50 was so that I could learn a bit more about front end development and working with html, css, and javascript. It also has allowed me to explore more into Flask and learn about git and how to use it efficiently.
#### Features:
  This application allows users to register for an account and use that account to make posts for other users of the app. Each user is able to follow other users in order to see their posts on their homepage as well as they can look for other users and posts by using the search bar at the top of the page.
#### Files:
  To start here are the explanations for what each one of the files does in the project.
##### Templates:
- layout.html
  - This is the file that layouts most of the html that the user will see.
  - It contains html for...
    - The navigation bar at the top of the page.
      - This navigation bar holds the search bar, the sign in, register, and signout buttons as well as the menu button which extends the side navigation bar.
    - The side navigation bar that allows users to view their homepage, profile, friends, and name of the users profile as well as the button to make a post.
      - The options for profile and friends will not show up if the user is not signed in.
      - The side bar will be expanded to show the names of each button if the menu button in the nav bar is pressed.
    - The popup for signing in and registering
      - These are opened though the use of javascript which is activated by clicking the register or sign in button if the user is not already signed in.
      - The sign in prompts the user for their username and password which is checked through the flask application.
- index.html
  - This file has the html for homepage of the user
  - It will not show any posts if the user is not signed in
  - It will show user post from people they are following and will tell the user to follow more people if there are no posts.
  - The posts that are displayed are linked to each user that has posted them.
  - The posts are also ordered by the time that they were posted
- users.html
  - This is the file that contains the html for every user on the app
  - It links to /user/<username>
    - If user tries to enter a name that is not there, it will flash the user a message that tells them that this user does not exist.
  - It has two main parts
    - The profile's information
      - This shows the name of the profile, the profile username, and the following/follower count.
      - This also shows an unfollow or follow button based on wether or not the current user is following them
        - If it is the users own account it will not show anything.
    - The profile's posts
      - It shows the users username and name as well as date it was posted.
      - And the text the user has posted.
- friends.html
  - Shows the current user a list of all of the users they are following including those users how many people they are following and the amount of followers they have.
- post.html
  - This is where the user can type anything they want to post
- search.html
  - This is shown after the user has entered something into the search bar at the top of the page.
  - Takes information from the database to find any users or posts that contain the same words that the user entered.

##### Static:
- scripts.js
  - This holds all of the javascript for the layout.
  - It handles the ability to open and close the side nav bar as well as opening the register and sign in prompts.
- styles.css
  - Handles all css for app.
##### App:
- This is the flask app that handles all backend functionality of the application.
- Most of it is explained in the file.
#### Features That I Would Have Liked to Add:
Due me having personal matters I need to attend to, I was not able to add all the features I wanted. Here is a list of features I wanted to add.
- Ability for users to change their username, name, and password.
- Allow users to delete their own posts.
- Allow for users to like eachothers posts
- Limit the search to three to five users and allow the user to look at more through a different page
- Profile Pictures for users
- Allow users to post photos

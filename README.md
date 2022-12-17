# CS:50 Final Basic Social Media App
#### Video Demo:  <URL HERE>
#### Description:
  This is my final project for CS:50. It is basic web based social media app using Flask. 
#### Reasons:
  The reason I chose to make this application as my final project for CS:50 was so that I could learn a bit more about front end development and working with html, css, and javascript. It also has allowed me to explore more into Flask
#### Features:
  This application allows users to register for an account and use that account to make posts for other users of the app. Each user is able to follow other users in order to see their posts on their homepage as well as they can look for other users and posts by using the search bar at the top of the page.
#### Files:
  To start here are the explanations for what each one of the files does in the project.
##### Templates:
- Layout.html
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
  - It has two main parts
    - The profile's information
      - This shows the name of the profile, the profile username, and the following/follower count.
      - This also shows an unfollow or follow button based on wether or not the current user is following them
    - The profile's post
  

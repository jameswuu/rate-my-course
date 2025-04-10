# Rate My Course 

## Video Demo: https://youtu.be/WOTDMLNOFU8
## Introduction
CS50x has introduced me to the exciting world of programming. After 10 weeks of intensive content, I’ve transitioned from not knowing how to write code to optimizing programming concepts. Before taking this class, I spent a considerable amount of time researching online courses, exploring videos and websites to find the right fit. This experience inspired me to create a webpage called “Rate My Course.” The primary purpose of this site is to allow users to review courses they have taken. Users' reviews serve as valuable guidance for those who are still undecided about which course to pursue. By reading these reviews, potential students can make more informed decisions about their educational journey.

## Implementation and Design
The webpage I created utilizes a Flask template and is structured into five main categories:
1. Nav Bar
2. Index
3. Review
3. About
5. Account.

Below, I’ll explain the functionality of each component.

## Nav Bar (layout.html)
The Navigation Bar is present on every page and serves to direct users to their desired locations, including the Index Page, Review Page, About Page, and Account Page, as well as a Login/Logout button. For example, if users want to view the "About" page, they can easily click on the link to be directed there. To keep track of reviews and user information, account registration is required. If a user is not logged in, they will have access only to the Index Page, About Page, and Login Page. The Review and Account pages are restricted to logged-in users. Additionally, I added a nice touch to the navigation bar: instead of simply displaying "Account," it dynamically shows the current username.

## Index Page (index.html)
This page displays all user reviews. It is divided into two sections. The top section summarizes reviews in a visually appealing format, showcasing three main features: the average score of the CS50 class out of five, the total number of reviewers, and a table displaying scores. The design was inspired by popular course rating website, rate my prof, but with my own twist. For instance, instead of a black-and-white palette, I incorporated the CS50 duck’s signature yellow to make the site unique. I also conducted research on converting backend SQL data into a table using JavaScript. The lower section of the page lists all user reviews in a clear, boxy layout, utilizing a backend database that stores user ratings displayed using a loop. I intentionally omitted usernames from the review boxes to maintain anonymity, allowing students to express their thoughts freely.

## Review Page (review.html)
This page allows users to submit their ratings to the backend server. I implemented a *form* that collects data on the year of completion, duration of the course, workload, usefulness, quality, and a personal comment. For the year and duration fields, I used the *select* function to provide predetermined options, preventing unexpected input. The workload, usefulness, and quality categories feature a star rating system, where users can rate their class from one to five stars. This system, built with JavaScript and CSS, tracks user ratings and animates the stars. A *textarea* enables users to enter additional comments. If any fields are left blank, an error message will be displayed upon submission.

## About Page (about.html)
This page outlines the purpose of the website. I employed CSS styling to enhance the visual appeal, using display: flex to create a balanced layout. The page is divided into three sections: “About This Page,” “What is DUCK,” and “How Does DUCK Work?” Users can click on “About” to learn more.

## Account Page (account.html)
The Account page displays the current user’s username and allows them to add their school information. Most importantly, this page enables users to change their passwords. To do so, they must enter their current password. If the entered password is incorrect or the new password does not match the confirmation, an error message will appear. Conversely, if the password is successfully changed, a success message will be displayed.

## SQL Database (project.db)
This project utilizes a database with two tables: users and reviews. The users table tracks usernames, passwords, and personal information, while the reviews table maintains records of user reviews. The reviews table is linked to the users table using a foreign key (user_id) that references the id in the users table.

## app.py
The success of this project is attributed to various libraries from CS50 and other resources, including cs50, datetime, bleach, flask, flask_session, werkzeug.security, and helpers.
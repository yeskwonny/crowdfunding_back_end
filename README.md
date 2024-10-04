
# Crowdfunding Back End

MakeCine

## Planning:

### Concept/Name

This is a platform for independent movie directors.
They can introduce their films and receive funding from the public.

### Intended Audience/User Stories

- Movie directors or staff
- Movie fans who loves independent movies
- Investors

### Front End Pages/Functionality

- Homepage
  1. nav bar
  - Sign up/ login button on the nav bar.
  - Create projects button.
  2. Landing page
  - Display all projects.
  - button for project detail.
  - Progress bar goal of pledges and how much pledges has been made so far.
- Project detail
  - Show the onwer of project.
  - Show details of project such as content, title...
  - funding deadline.
  - Progress bar goal of pledges and how much pledges has been made so far.
  - History of the pledges.
  - Button for donate.
  - Button for updating (only owner)
- Error handling page
  - Login is required
  - Unauthorized such as not project owner or admin
  - Bad request such as missing field.

### API Spec
| URL                    | HTTP METHOD | PURPOSE                 | REQUEST BODY   | SUCCESS RESPONSE CODE | Autnetication/Authorisation                         | 
|------------------------|-------------|-------------------------|----------------|-----------------------|-----------------------------------------------------| 
| /projects/             | GET         | Display all projects    | N/A            | 200                   | N/A                                                 | 
| /projects/:id          | GET         | Return a project by id  | N/A            | 200                   | N/A                                                 | 
| /projects?is_open=True | GET         | Return projects is open | N/A            | 200                   | N/A                                                 | 
| /projects/             | POST        | Create a new projects   | Project object | 201                   | Login required                                      | 
| /projects/:id          | PUT         | Update the prject       | Project object | 200                   | Login required /Must be the project owner or admin  | 
| /projects/:id          | DELETE      | Delete the project      |                | 200                   | Login required /Must be the project owner or admin  | 
|                        |             |                         |                |                       |                                                     | 
| /pledges/              | GET         | Return all pledges      | N/A            | 200                   | N/A                                                 | 
| /pledges/:id           | GET         | Return a pledge by id   | N/A            | 200                   | N/A                                                 | 
| /pledges/              | POST        | Create a pledge         | Pledges object | 201                   | Login required                                      | 
| /pledges/:id           | PUT         | Update a pledge         | Pledges object | 200                   | Login required /Must be the project owner or admin  | 
| /pledges/:id           | DELETE      | Delete the pledge by id | N/A            | 200                   | Login required /Must be the project owner or admin  | 
|                        |             |                         |                |                       |                                                     | 
| /users/                | GET         | Returns all users       | N/A            | 200                   | Login required /Must be the admin                   | 
| /users/                | POST        | Sign up                 | User object    | 201                   | N/A                                                 | 
| /users/login           | POST        | Login                   | User object    | 200                   | N/A                                                 | 
| /users/:id             | PUT         | Update the user by id   | User object    | 200                   | Login required /Must be the project owner or admin  | 
| /users/:id             | DELETE      | Delete the user by id   | N/A            | 200                   | Login required /Must be the project owner or admin  | 
### DB Schema

![]( {{ ./relative/path/to/your/schema/image.png }} )

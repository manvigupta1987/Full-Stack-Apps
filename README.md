# Full-Stack-Developer Projects

### Project 1: Booking Site Fy-yur

Aim of the project was to build a full-stack Web App with Flask and Boostrap which enables
Venues & Artists to list themselves and arrange Shows together.

Used tech stack:
- `SQLAlchemy` as ORM library of choice
- `PostgreSQL` as database
- `Python3` and `Flask` for server language and framework
- `Flask-Migrate` for creating and running schema migrations
- Frontend: HTML, CSS, and Javascript with Bootstrap 3 (mainly provided by Udacity Team)

Applied concepts:
- How to use Git Bash & Github as version control tool
- Configure local database and connect it to a web application
- Create Model Schemas with columns and relationships (1:1, 1:n and N:N)
- Use SQLAlchemy ORM with PostgreSQL to query, insert, edit & delete Data
- Use WTForms to encapsulate input forms in separate file & to allow for custom validations
- Use Bootstrap as a simple to use Front End Library and Ajax to fetch flask routes
- Create SQL-like Queries, but without any SQL syntax, only using SQLAlchemy ORM
- How to clearly structure a larger web application in different files & folders

[View Project](https://github.com/manvigupta1987/Full-Stack-Projects/tree/master/fyyur).

### Project 2: Trivia API

Using 'Flask' and 'React', created a Full-Stack App to manage questions
for different categories & develop an API to power the Quiz Gameplay.

Used tech stack:
- React Components as frontend (provided by Udacity Team)
- Python3 and Flask for server language and API development
- `cors` to handle access to the API
- `unittest` for automated testing of APIs
- `curl` to get responses from API
- `README.md` to document project setup & API endpoints

Applied concepts:
- using best-practice `PEP8-style` to design and structure code
- `test-driven-development (TDD)` to rapidly create highly tested & maintainable endpoints.
- directly test and make response to any endpoint out there with `curl`.
- implement `errorhandler` to format & design appropriate error messages to client
- becoming aware of the importance of extensive project documentation & testing.

[View Project](https://github.com/manvigupta1987/Full-Stack-Projects/tree/master/trivia-app).

### Project 3: Coffee Shop (Security & Authorization)

Using 'Flask' and 'Auth0', created a Full-Stack App to let Users
login to Site & make actions according to their Role & Permission Sets.

Used tech stack:
- `Python3` & `Flask` for server language and API development 
- `SQLAlchemy` as ORM / `Sqlite` as database
- `Ionic` to serve and build the frontend (provided by Udacity Team)
- `Auth0` as external Authorization Service & permission creation
- `jose` JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTs.
- `postman` to automatize endpoint testing & verification of correct Authorization behaviour.

[View Project](https://github.com/manvigupta1987/Full-Stack-Projects/tree/master/coffee-shop-app).

### Project 4: Server Deployment, Containerization and Testing

Deployed a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

(Application has been teared down after successful review to avoid incurring additional costs)

[View Project]().

Used tech stack:
- `Docker` for app containerization & image creation to ensure environment consistency across development and production server
- `AWS EKS` & `Kubernetes` as container orchestration service to allow for horizontal scaling
- `aswscli` to interact with AWS Cloud Services
- `ekscli` for EKS cluster creation
- `kubectl` to interact with kubernetes cluster & pods
- `CodePipeline` for Continuous Delivery (CD) & to watch Github Repo for changes
- `CodeBuild` for Continuous Integration (CI), together with `pytest` for automated testing before deployment


### Project 5: Capstone

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.
It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentication with `Auth0` (see `auth.py`)
5. Deployment on `Heroku` (see `setup.sh`)

[View Project]().


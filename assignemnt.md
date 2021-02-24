# Data Engineering & Analyst Assignment

## Background:

The role of data analyst & engineer is to support by helping stakeholders get the data they need in order to make better decisions. As such, "practical" and "done" is more important than "perfect", but the validity of decisons depends on obtaining good quality, timely correct data.

This assignment is intended to see how you would approach an every-day data problems. We expect that it should take approximately three hours to complete.

Your work will be assessed on a number of criteria:

* Does it work as required? We will follow any instructions you have provided and attempt to re-run your project.
* How do we know the code will execute as intended in production?
* How easy is it for other developers to contribute to the project?

Please create a public github repo and share the link. Include any file or component which is needed to re-run the assignment such as scripts and instructions. Please do not include any database internal files. Feel free to restructure the repo to suit your needs.

## Assignment:

You are introduced to a software-as-a-service company (SaaS) called ABC Enterprises. The leadership is flying blind and urgently needs an analysis of the help of the company. They currently lack any KPIs. Put on your superhero suit and open your favorite IDE.

You task will be to:
 - Generate a fake dataset representing the company's database and store it in a local PostgreSQL database.
 - Report 3 relevant KPIs of business health.
 - Explain how you would go about understanding the problem and arrive at a solution.

### Spin up the PostgreSQL database

Make sure Docker is installed and run:

``` bash
./start.sh
```

The credentials for the database can be found in the `docker-compose.yml` file.

### Generating the data

Rules:
 - Let's assume the company has existed for 12 months, they acquired all their customers on month 1 and they will not gain any more customers in the following 12 months.
 - All customers (referred to as companies) have monthly subscriptions.
 - Create 500 companies, each with a unique `company_id` .
 - Each company is a company_size="small" with a probability of 0. 7 and "large" with a probability of 0. 3.
 - Monthly subscriptions for small and large companies are $19 and $99 respectively.
 - Each small company has the number of sessions in a month equal to 5, plus or minus a uniform random integer between 0 & 5.
 - Each large company has the number of sessions in a month equal to 10, plus or minus a uniform random integer between 0 & 10.
 - Give each session a random `created_at` timestamp within that month.
 - If a company has 0 sessions in a month, they have churned that month and will not come back (i. e. have no future sessions).

Create a python package in `main/assignment` to generate this data and store it into the PostgeSQL database. This package should also create an appropriate database schema. Use the `build.sh` script to install it in a virtual environment in the projects root directory.

### Reporting KPIs

Finally, we want to inform ABC Enterprises of the overall health of their business.

Enable your python package to query for 3 relevant KPIs using SQL and simply print them. You should be able to motivate your choice of KPIs.

## Task Summary

 - Use the docker-compose file in this project to spin up a new postgres database.
 - Use any necessary Python libraries.
 - Create an appropriate database schema - please provide a way for us to recreate this schema.
 - Write a Python script that generates fake data and stores it as tables in the local database.
 - Write a Python script that will use SQL to query and print 3 relevant KPIs.
 - Add any necessary tests.
 - Provided some instructions which will allow us to repeat everything you have done. Put this in another markdown file.
 - Create a public github repo and share the link.

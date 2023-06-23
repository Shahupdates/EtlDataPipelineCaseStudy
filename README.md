# EtlDataPipelineCaseStudy
Backend/Data Eng - Case Study


Technical Case Study: ETL Pipeline Development and Optimization

Objective: The purpose of this technical exercise is to evaluate your skills in designing, developing, optimizing and troubleshooting a big data ETL (Extract, Transform, Load) pipeline. You will use a combination of SQL, Python, DBT and a big data technology of your choice (Hadoop, Spark, etc.).


Background: Our company collects blockchain transaction data from various digital platforms, which needs to be processed and analyzed to support business decisions.

Your task is to develop a scalable ETL pipeline that extracts data from Solana Blockchain nodes, transforms it based on specific business rules, and loads the transformed data into PostgreSQL.

Part 1: ETL Pipeline Development (3-4 Hours)
Extract: Write a script in Python to extract data from Solana Blockchain.
Transform: Develop a transformation function based on the following business rules:
Rule 1: Only extract data from Magic Eden contracts.
Rule 2: Filter out any records that are older than two years.
Your script should be able to get a contract address as a variable so it could be used for other contract addresses too.


Load: Write a script to load the transformed data into PostgreSQL.

For each function in the contract you should create a new table.

You are free to use different tables, ideally you should have a raw data table and aggregated tables like daily active users, daily transaction volume etc.

Part 2: Optimization and Troubleshooting (1 Hour)
Based on your understanding of big data technologies and databases, identify potential performance bottlenecks in your ETL pipeline and propose solutions to optimize it. Discuss how to stream the data from blockchain and update the database with real-time data.
Assume that the ETL pipeline failed during the transformation stage. Discuss how you would troubleshoot this issue.

Part 3: Collaboration and Documentation (1 Hour)
Prepare a short document explaining how your ETL pipeline works, any decisions you made, and instructions on how to run it. This document should be written with both technical and non-technical colleagues in mind.
Describe how you would collaborate with data science and business teams to understand their data needs and how your ETL pipeline could be adjusted to meet these needs.
Deliverables
The source code of your ETL pipeline.
A document explaining your ETL pipeline, any decisions you made, instructions on how to run it, and your collaboration strategy with the data science and business teams.
An explanation of how you identified and proposed to optimize performance bottlenecks.
A troubleshooting guide for the pipeline.

Your evaluation will be based on the quality of your code, the scalability of your ETL pipeline, your ability to optimize and troubleshoot, your ability to communicate technical concepts, and your collaboration strategy.


Part 4 (optional): (3-4 Hours)

Using the database you have created, create a dashboard which has insights from the data like daily active users, daily volume, counts of transactions etc. However, this dashboard should be real-time, you need to update data on the dashboard when there is a new transaction written.


You are free to use Retool for your dashboard needs. It is a no-code dashboard platform, so you do not need to write frontend

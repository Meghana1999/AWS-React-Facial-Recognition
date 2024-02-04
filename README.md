# About the Project

## Overview

This project focuses on implementing an AI-based employee authentication system using facial recognition. The system comprises two primary flows: Registration Flow and Authentication Flow. In the Registration Flow, employee images are uploaded to S3 buckets, triggering a Lambda function that registers the employee by indexing the image through AWS Rekognition. The employee's details are then stored in DynamoDB. The Authentication Flow involves capturing images at the entrance, uploading them to S3, and utilizing AWS Rekognition to verify if the individual is an employee.

## Architecture Diagram

![Architecture Diagram](https://github.com/Meghana1999/AWS-React-Facial-Recognition/blob/main/AWS-React-Faciaol-Recognition-Architecture.jpg)

## Project Description

In the context of a company and its daily office activities, this project addresses the need for secure employee authentication using facial recognition technology. The Registration Flow initiates by capturing employee pictures, uploading them to designated S3 buckets. This triggers a Lambda function, referred to as the Registration Lambda, which performs indexing using AWS Rekognition. The resulting unique key, known as the Rekognition ID, is stored alongside employee information in DynamoDB.

The Authentication Flow comes into play when individuals enter the company premises. Images of entrants are captured, uploaded to S3, and processed by AWS Rekognition to determine if the person is a registered employee. The React.js frontend communicates with the API Gateway, which triggers Lambda functions for image processing.

# Technologies Used

The implementation of this project involves the use of various technologies to achieve seamless integration and efficient functioning. Below is a list of key technologies employed:

- **AWS (Amazon Web Services):**
  - **S3 (Simple Storage Service):** Used for storing employee and visitor images.
  - **Lambda:** Leveraged for serverless computing, particularly in the Registration and Authentication flows.
  - **Rekognition:** Utilized for facial recognition tasks, indexing images, and searching faces.
  - **DynamoDB:** Chosen as the **NoSQL database** for storing employee information.

- **React.js:**
  - Implemented for developing the frontend user interface, allowing user interaction with the system.

- **API Gateway:**
  - Used to create **RESTful APIs**, facilitating communication between the frontend and Lambda functions.

- **IAM (Identity and Access Management):**
  - Configured to manage access permissions and roles for **Lambda functions, API Gateway, and S3 buckets**.

- **GitHub:**
  - Employed for **version control** and collaborative development.

These technologies collectively enable the seamless execution of the Registration and Authentication flows, ensuring a reliable and secure employee authentication system.

# Output Demo

## Successful Authentication

![Successful Authentication](https://github.com/Meghana1999/AWS-React-Facial-Recognition/blob/main/Successful%20Authentication%20Screenshot.png)

## Failed Authentication (Not an Employee)

![Failed Authentication](https://github.com/Meghana1999/AWS-React-Facial-Recognition/blob/main/Failed%20Authentication%20Screenshot.png)

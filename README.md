# AWS Automation and Deployment Project

## Overview
This repository contains code and configuration files for automating the deployment of AWS resources and serverless functions. The project focuses on leveraging Python, AWS Lambda, and supporting AWS services to streamline the provisioning and management of cloud infrastructure.

## Project Components
The main components of this project are:

1. **deploy_lambda.py**: This Python script handles the deployment of an AWS Lambda function. It includes functions for packaging the Lambda code, creating or updating the Lambda function, and managing the associated resources.

2. **lambda_function.py**: This file contains the source code for the AWS Lambda function itself. The Lambda function can be used to perform various tasks, such as data processing, API integration, or event-driven logic.

3. **layer.py**: This script is responsible for creating and deploying an AWS Lambda layer. Lambda layers allow you to package dependencies and libraries that can be shared across multiple Lambda functions.

4. **main.py**: The main entry point of the project, this script orchestrates the deployment of the Lambda function and layer.

5. **Supporting Files**:
   - `.gitattributes`: Specifies how Git should handle certain file types.

## Deployment Workflow
The deployment workflow for this project is as follows:

1. The `main.py` script is executed, which orchestrates the deployment process.
2. The `deploy_lambda.py` script is called to handle the deployment of the Lambda function.
   - The Lambda function code is packaged into a ZIP file.
   - The Lambda function is created or updated in the AWS environment.
3. The `layer.py` script is called to deploy the Lambda layer.
   - The layer code is packaged into a ZIP file.
   - The Lambda layer is created or updated in the AWS environment.

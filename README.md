# Newsletter_site
A simple newsletter subscription webpage project.

![serverless_newsletter_architecture drawio (1)](https://github.com/user-attachments/assets/a3cf419b-99f2-438d-94c0-555e95d4dcc0)

# Features
User subscription management
Email automation with AWS SES
Serverless backend using AWS Lambda and API Gateway
Data storage with DynamoDB
Secure access control with IAM
Static asset storage in S3

# Architecture
API Gateway - Handles incoming HTTP requests.
Lambda Functions - Processes user subscriptions and email sending.
DynamoDB - Stores subscriber details.
SES (Simple Email Service) - Sends newsletters to subscribers.
S3 - Stores static assets or email templates.
IAM - Manages secure access control for AWS services.

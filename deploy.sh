#!/bin/bash

# Install AWS CLI and EB CLI if not already installed
# pip install awscli awsebcli

# Configure AWS credentials
# aws configure

# Initialize EB CLI
eb init -p python-3.9 fashion-ai-app --region us-east-1

# Create the environment
eb create fashion-ai-env --instance-type t2.micro --single

# Deploy the application
eb deploy

# Open the application in browser
eb open 
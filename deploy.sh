#!/bin/bash

# Install AWS CLI and EB CLI if not already installed
pip install awscli awsebcli

# Configure AWS credentials
aws configure

# Initialize EB CLI
eb init -p python-3.9 fashion-ai-app --region us-east-1

# Create the environment
eb create fashion-ai-env --instance-type t2.micro --single

# Deploy the application
eb deploy

# Open the application in browser
eb open

# Make the deploy script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh

# Set environment variables
aws elasticbeanstalk update-environment --environment-name fashion-ai-env --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=SECRET_KEY,Value=your-secure-secret-key
aws elasticbeanstalk update-environment --environment-name fashion-ai-env --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=FLASK_DEBUG,Value=False
aws elasticbeanstalk update-environment --environment-name fashion-ai-env --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=STYLE_MODEL_PATH,Value=/var/app/current/models/style_model.h5
aws elasticbeanstalk update-environment --environment-name fashion-ai-env --option-settings Namespace=aws:elasticbeanstalk:application:environment,OptionName=VIRTUAL_TRYON_MODEL_PATH,Value=/var/app/current/models/virtual_tryon.h5 
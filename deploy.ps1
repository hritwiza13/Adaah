# Error handling
$ErrorActionPreference = "Stop"

# Function to check if a command exists
function Test-Command {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { if (Get-Command $command) { return $true } }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check and install required packages
Write-Host "Checking and installing required packages..."
if (-not (Test-Command aws)) {
    Write-Host "Installing AWS CLI..."
    pip install awscli
}
if (-not (Test-Command eb)) {
    Write-Host "Installing EB CLI..."
    pip install awsebcli
}

# Check if AWS is configured
$awsConfig = "$env:USERPROFILE\.aws\credentials"
if (-not (Test-Path $awsConfig)) {
    Write-Host "AWS credentials not found. Please configure AWS..."
    aws configure
}

# Initialize EB CLI if not already initialized
if (-not (Test-Path ".elasticbeanstalk")) {
    Write-Host "Initializing Elastic Beanstalk application..."
    eb init -p python-3.9 fashion-ai-app --region us-east-1
}

# Create environment if it doesn't exist
$envExists = eb status fashion-ai-env 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating Elastic Beanstalk environment..."
    eb create fashion-ai-env --instance-type t2.micro --single
}

# Deploy the application
Write-Host "Deploying application..."
eb deploy

# Set environment variables
Write-Host "Setting environment variables..."
$secretKey = [System.Guid]::NewGuid().ToString()
eb setenv SECRET_KEY="$secretKey" `
          FLASK_DEBUG="False" `
          STYLE_MODEL_PATH="/var/app/current/models/style_model.h5" `
          VIRTUAL_TRYON_MODEL_PATH="/var/app/current/models/virtual_tryon.h5"

# Open the application
Write-Host "Opening application in browser..."
eb open

Write-Host "Deployment completed successfully!" 
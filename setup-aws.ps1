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

Write-Host "AWS Setup Helper" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host ""

# Check if AWS CLI is installed
if (-not (Test-Command aws)) {
    Write-Host "Installing AWS CLI..." -ForegroundColor Yellow
    pip install awscli
}

# Create AWS credentials directory if it doesn't exist
$awsDir = "$env:USERPROFILE\.aws"
if (-not (Test-Path $awsDir)) {
    New-Item -ItemType Directory -Path $awsDir | Out-Null
}

# Guide user through AWS setup
Write-Host "To set up AWS credentials, you need to:" -ForegroundColor Cyan
Write-Host "1. Create an AWS account at https://aws.amazon.com" -ForegroundColor White
Write-Host "2. Create an IAM user with Elastic Beanstalk permissions" -ForegroundColor White
Write-Host "3. Get your Access Key ID and Secret Access Key" -ForegroundColor White
Write-Host ""

$proceed = Read-Host "Have you created an AWS account and IAM user? (y/n)"
if ($proceed -ne "y") {
    Write-Host "Please create an AWS account and IAM user first." -ForegroundColor Red
    Write-Host "Visit https://aws.amazon.com to get started." -ForegroundColor Red
    exit
}

# Configure AWS credentials
Write-Host "`nPlease enter your AWS credentials:" -ForegroundColor Cyan
aws configure

# Test AWS configuration
Write-Host "`nTesting AWS configuration..." -ForegroundColor Yellow
try {
    aws sts get-caller-identity
    Write-Host "AWS configuration successful!" -ForegroundColor Green
} catch {
    Write-Host "AWS configuration failed. Please check your credentials." -ForegroundColor Red
    exit
}

Write-Host "`nAWS setup completed successfully!" -ForegroundColor Green
Write-Host "You can now run deploy.ps1 to deploy your application." -ForegroundColor Green 
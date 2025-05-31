# Error handling
$ErrorActionPreference = "Stop"

Write-Host "Adaah App Setup Helper" -ForegroundColor Green
Write-Host "=====================" -ForegroundColor Green
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { if (Get-Command $command) { return $true } }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check if git is installed
if (-not (Test-Command git)) {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/downloads" -ForegroundColor Red
    exit
}

# Get GitHub credentials
Write-Host "Please enter your GitHub credentials:" -ForegroundColor Cyan
$githubUsername = Read-Host "GitHub Username"
$githubEmail = Read-Host "GitHub Email"

# Configure Git
Write-Host "`nConfiguring Git..." -ForegroundColor Yellow
git config --global user.name $githubUsername
git config --global user.email $githubEmail

# Initialize repository if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Update: Added ML features and deployment configuration"

# Set up remote for Adaah repository
$repoUrl = "https://github.com/hritwiza13/Adaah.git"

# Add remote if it doesn't exist
$remoteExists = git remote -v | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "`nAdding remote repository..." -ForegroundColor Yellow
    git remote add origin $repoUrl
}

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin master

# Create Render account
Write-Host "`nNow, let's set up Render deployment:" -ForegroundColor Cyan
Write-Host "1. Go to https://render.com" -ForegroundColor White
Write-Host "2. Sign up for a free account" -ForegroundColor White
Write-Host "3. Connect your GitHub account" -ForegroundColor White

$proceed = Read-Host "`nHave you created a Render account? (y/n)"
if ($proceed -ne "y") {
    Write-Host "Please create a Render account first." -ForegroundColor Red
    exit
}

# Deploy to Render
Write-Host "`nDeploying to Render..." -ForegroundColor Yellow
Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
Write-Host "2. Click 'New +' and select 'Web Service'" -ForegroundColor White
Write-Host "3. Connect your repository: $repoUrl" -ForegroundColor White
Write-Host "4. Use these settings:" -ForegroundColor White
Write-Host "   - Name: adaah-app" -ForegroundColor White
Write-Host "   - Environment: Python" -ForegroundColor White
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "   - Start Command: gunicorn app:app" -ForegroundColor White
Write-Host "5. Click 'Create Web Service'" -ForegroundColor White

Write-Host "`nSetup completed!" -ForegroundColor Green
Write-Host "Your GitHub repository: $repoUrl" -ForegroundColor Green
Write-Host "Your Render app will be available at: https://adaah-app.onrender.com" -ForegroundColor Green 
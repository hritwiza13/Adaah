# Error handling
$ErrorActionPreference = "Stop"

Write-Host "GitHub Push Helper" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host ""

# Check if git is installed
if (-not (Test-Command git)) {
    Write-Host "Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/downloads" -ForegroundColor Red
    exit
}

# Check if repository is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Fashion AI application with ML features"

# Get GitHub repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/fashion-ai-app.git)"

# Add remote if it doesn't exist
$remoteExists = git remote -v | Select-String "origin"
if (-not $remoteExists) {
    Write-Host "Adding remote repository..." -ForegroundColor Yellow
    git remote add origin $repoUrl
}

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin master

Write-Host "`nSuccessfully pushed to GitHub!" -ForegroundColor Green
Write-Host "Your repository is available at: $repoUrl" -ForegroundColor Green 
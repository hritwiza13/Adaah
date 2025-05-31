# Error handling
$ErrorActionPreference = "Stop"

Write-Host "Render Deployment Helper" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
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
    git add .
    git commit -m "Initial commit"
}

# Guide user through Render setup
Write-Host "To deploy to Render, you need to:" -ForegroundColor Cyan
Write-Host "1. Create a Render account at https://render.com" -ForegroundColor White
Write-Host "2. Connect your GitHub repository" -ForegroundColor White
Write-Host "3. Create a new Web Service" -ForegroundColor White
Write-Host ""

$proceed = Read-Host "Have you created a Render account? (y/n)"
if ($proceed -ne "y") {
    Write-Host "Please create a Render account first." -ForegroundColor Red
    Write-Host "Visit https://render.com to get started." -ForegroundColor Red
    exit
}

# Check if remote exists
$renderRemote = git remote -v | Select-String "render"
if (-not $renderRemote) {
    Write-Host "`nPlease follow these steps:" -ForegroundColor Cyan
    Write-Host "1. Go to https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. Click 'New +' and select 'Web Service'" -ForegroundColor White
    Write-Host "3. Connect your repository" -ForegroundColor White
    Write-Host "4. Use these settings:" -ForegroundColor White
    Write-Host "   - Name: fashion-ai-app" -ForegroundColor White
    Write-Host "   - Environment: Python" -ForegroundColor White
    Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "   - Start Command: gunicorn app:app" -ForegroundColor White
    Write-Host "5. Click 'Create Web Service'" -ForegroundColor White
} else {
    Write-Host "`nDeploying to Render..." -ForegroundColor Yellow
    git push render master
}

Write-Host "`nDeployment setup completed!" -ForegroundColor Green
Write-Host "Your app will be available at: https://fashion-ai-app.onrender.com" -ForegroundColor Green

# Push to GitHub
Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
git remote add origin https://github.com/YOUR_USERNAME/fashion-ai-app.git
git push -u origin master 
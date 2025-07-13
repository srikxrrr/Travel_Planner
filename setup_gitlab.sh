#!/bin/bash

# 🦊 GitLab Setup Script for Travel Planner
# This script helps you add the Travel Planner project to GitLab

echo "🦊 GitLab Setup Script for Travel Planner"
echo "=========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if git is available
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed. Please install Git first.${NC}"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a Git repository. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Current repository status:${NC}"
echo "Repository: $(git remote get-url origin 2>/dev/null || echo 'No origin remote found')"
echo "Current branch: $(git branch --show-current)"
echo "Working directory: $(pwd)"
echo

# Get user input
echo -e "${YELLOW}🔑 GitLab Configuration${NC}"
echo "Please provide your GitLab details:"
echo

read -p "GitLab username: " GITLAB_USERNAME
read -p "GitLab repository name (default: travel-planner): " GITLAB_REPO
read -p "Authentication method (token/ssh): " AUTH_METHOD

# Set default repo name if not provided
GITLAB_REPO=${GITLAB_REPO:-travel-planner}

# Validate inputs
if [[ -z "$GITLAB_USERNAME" ]]; then
    echo -e "${RED}❌ GitLab username is required${NC}"
    exit 1
fi

if [[ "$AUTH_METHOD" != "token" && "$AUTH_METHOD" != "ssh" ]]; then
    echo -e "${RED}❌ Authentication method must be 'token' or 'ssh'${NC}"
    exit 1
fi

# Setup based on authentication method
if [[ "$AUTH_METHOD" == "token" ]]; then
    echo
    echo -e "${YELLOW}🔐 Token Authentication Setup${NC}"
    echo "1. Go to GitLab → Settings → Access Tokens"
    echo "2. Create a token with 'api', 'read_repository', 'write_repository' scopes"
    echo "3. Copy the token and paste it below"
    echo
    read -s -p "GitLab Personal Access Token: " GITLAB_TOKEN
    echo
    
    if [[ -z "$GITLAB_TOKEN" ]]; then
        echo -e "${RED}❌ GitLab token is required${NC}"
        exit 1
    fi
    
    GITLAB_URL="https://oauth2:${GITLAB_TOKEN}@gitlab.com/${GITLAB_USERNAME}/${GITLAB_REPO}.git"
else
    echo
    echo -e "${YELLOW}🔑 SSH Authentication Setup${NC}"
    echo "Make sure you have:"
    echo "1. Generated SSH key: ssh-keygen -t rsa -b 4096 -C 'your_email@example.com'"
    echo "2. Added public key to GitLab → Settings → SSH Keys"
    echo
    read -p "Press Enter to continue when SSH is set up..."
    
    GITLAB_URL="git@gitlab.com:${GITLAB_USERNAME}/${GITLAB_REPO}.git"
fi

# Check if GitLab remote already exists
if git remote | grep -q "^gitlab$"; then
    echo -e "${YELLOW}⚠️  GitLab remote already exists. Removing and re-adding...${NC}"
    git remote remove gitlab
fi

# Add GitLab remote
echo -e "${BLUE}🔗 Adding GitLab remote...${NC}"
if git remote add gitlab "$GITLAB_URL"; then
    echo -e "${GREEN}✅ GitLab remote added successfully${NC}"
else
    echo -e "${RED}❌ Failed to add GitLab remote${NC}"
    exit 1
fi

# Show all remotes
echo -e "${BLUE}📡 Current remotes:${NC}"
git remote -v

# Test connection
echo -e "${BLUE}🔍 Testing GitLab connection...${NC}"
if git ls-remote gitlab > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connection to GitLab successful${NC}"
else
    echo -e "${RED}❌ Failed to connect to GitLab. Please check your credentials.${NC}"
    exit 1
fi

# Ask about pushing branches
echo
echo -e "${YELLOW}📤 Ready to push to GitLab${NC}"
echo "Available branches:"
git branch -a
echo

read -p "Push main branch? (y/n): " PUSH_MAIN
read -p "Push current feature branch? (y/n): " PUSH_FEATURE

# Push branches
if [[ "$PUSH_MAIN" == "y" || "$PUSH_MAIN" == "Y" ]]; then
    echo -e "${BLUE}📤 Pushing main branch...${NC}"
    if git push gitlab main; then
        echo -e "${GREEN}✅ Main branch pushed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Main branch push failed (might not exist or need force push)${NC}"
    fi
fi

if [[ "$PUSH_FEATURE" == "y" || "$PUSH_FEATURE" == "Y" ]]; then
    CURRENT_BRANCH=$(git branch --show-current)
    echo -e "${BLUE}📤 Pushing current branch: $CURRENT_BRANCH${NC}"
    if git push gitlab "$CURRENT_BRANCH"; then
        echo -e "${GREEN}✅ Feature branch pushed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Feature branch push failed${NC}"
    fi
fi

# Final summary
echo
echo -e "${GREEN}🎉 GitLab Setup Complete!${NC}"
echo "Repository URL: https://gitlab.com/${GITLAB_USERNAME}/${GITLAB_REPO}"
echo "GitLab remote: $(git remote get-url gitlab)"
echo
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Visit your GitLab repository: https://gitlab.com/${GITLAB_USERNAME}/${GITLAB_REPO}"
echo "2. Configure project settings (visibility, descriptions, etc.)"
echo "3. Set up CI/CD pipelines if needed"
echo "4. Add collaborators if working in a team"
echo
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo "• Push to GitLab: git push gitlab <branch-name>"
echo "• Pull from GitLab: git pull gitlab <branch-name>"
echo "• Check remotes: git remote -v"
echo "• View GitLab branches: git branch -r | grep gitlab"
echo

echo -e "${GREEN}✅ Setup completed successfully!${NC}"
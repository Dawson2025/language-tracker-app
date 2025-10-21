# Firebase Setup Guide

Complete guide to setting up Firebase for Lang Trak following Google's best practices.

## Overview

This project implements Google's recommended Firebase architecture:
- **Local emulators** for unit testing only (fast, free, isolated)
- **Real Firebase projects** for development, staging, and production

## Prerequisites

### Required Software
- **WSL Ubuntu** (mandatory for shell scripts)
- **Node.js** 16+ 
- **Firebase CLI**: `npm install -g firebase-tools`
- **Google Cloud CLI** (recommended): [Install Guide](https://cloud.google.com/sdk/docs/install)

### Required Permissions
- Google account with access to `lang-trak-*` Firebase projects
- Service account keys properly configured
- IAM roles: Firebase Admin, Firestore User, Cloud Functions Developer

## Firebase Projects

| Environment | Project ID | Purpose | URL |
|-------------|------------|---------|-----|
| **Test** | Local emulator | Unit tests only | `http://127.0.0.1:4002` |
| **Development** | `lang-trak-dev` | Daily development | `https://lang-trak-dev.web.app` |
| **Staging** | `lang-trak-staging` | Pre-production testing | `https://lang-trak-staging.web.app` |
| **Production** | `lang-trak-prod` | Live application | `https://lang-trak-prod.web.app` |

## Initial Setup

### 1. Authenticate with Firebase

```bash
# Login to Firebase (opens browser)
firebase login

# Verify authentication
firebase projects:list

# Should see all lang-trak projects
```

### 2. Authenticate with Google Cloud (Optional but Recommended)

```bash
# Login to Google Cloud
gcloud auth login

# Set default project (choose one)
gcloud config set project lang-trak-dev
```

### 3. Verify Project Access

```bash
# Test each environment
firebase use lang-trak-dev && firebase projects:list --filter="lang-trak-dev"
firebase use lang-trak-staging && firebase projects:list --filter="lang-trak-staging"  
firebase use lang-trak-prod && firebase projects:list --filter="lang-trak-prod"
```

## Environment Scripts

All environment scripts are located in `scripts/` directory and **must be run in WSL**.

### Development Environment

```bash
# Setup development environment
bash scripts/setup-dev-env.sh
```

**What it does:**
- Sets `PROJECT_ID=lang-trak-dev`
- Sets `FIREBASE_ENV=development`
- Switches Firebase CLI to development project
- Sets Google Cloud project to development

### Unit Testing Environment  

```bash
# Setup test environment (emulator only)
bash scripts/setup-test-env.sh
```

**What it does:**
- Sets `NODE_ENV=test`
- Sets `FIREBASE_ENV=test`
- Sets `USE_FIREBASE_EMULATOR=true`
- Configures emulator host variables
- **Does NOT switch Firebase projects** (uses emulators)

### Staging Environment

```bash
# Setup staging environment
bash scripts/setup-staging-env.sh
```

**What it does:**
- Sets `PROJECT_ID=lang-trak-staging`
- Sets `FIREBASE_ENV=staging`
- Switches Firebase CLI to staging project
- Sets Google Cloud project to staging

### Production Environment

```bash
# Setup production environment (includes safety warnings)
bash scripts/setup-prod-env.sh
```

**What it does:**
- Shows safety warnings
- Sets `PROJECT_ID=lang-trak-prod`
- Sets `FIREBASE_ENV=production`
- Switches Firebase CLI to production project
- Sets Google Cloud project to production

## Firebase Emulator Setup

### Configuration

Emulator settings in `firebase.json`:

```json path=/home/dawson/code/lang-trak-in-progress/firebase.json start=null
{
  "emulators": {
    "firestore": {
      "port": 8088,
      "host": "127.0.0.1"
    },
    "auth": {
      "port": 9099,
      "host": "127.0.0.1"
    },
    "ui": {
      "enabled": true,
      "port": 4002,
      "host": "127.0.0.1"
    }
  }
}
```

### Starting Emulators

```bash
# Setup test environment first
bash scripts/setup-test-env.sh

# Start specific emulators
firebase emulators:start --only firestore,auth

# Or start all emulators with UI
firebase emulators:start --only firestore,auth,ui

# Using NPM scripts
npm run emulator:start    # Start emulators
npm run emulator:ui       # Start with UI
```

### Emulator URLs

- **Firestore Emulator:** `http://127.0.0.1:8088`
- **Auth Emulator:** `http://127.0.0.1:9099`  
- **Emulator UI:** `http://127.0.0.1:4002`

## NPM Scripts Integration

The `package.json` includes scripts that work with WSL:

```json path=/home/dawson/code/lang-trak-in-progress/package.json start=null
{
  "scripts": {
    "firebase:dev": "wsl -e bash -c 'cd /home/dawson/code/lang-trak-in-progress && bash scripts/setup-dev-env.sh'",
    "firebase:test": "wsl -e bash -c 'cd /home/dawson/code/lang-trak-in-progress && bash scripts/setup-test-env.sh'",
    "firebase:staging": "wsl -e bash -c 'cd /home/dawson/code/lang-trak-in-progress && bash scripts/setup-staging-env.sh'",
    "firebase:prod": "wsl -e bash -c 'cd /home/dawson/code/lang-trak-in-progress && bash scripts/setup-prod-env.sh'",
    "emulator:start": "firebase emulators:start --only firestore,auth",
    "emulator:ui": "firebase emulators:start --only firestore,auth,ui"
  }
}
```

## Security Rules

### Firestore Rules

Located in `firestore.rules`:

```javascript path=/home/dawson/code/lang-trak-in-progress/firestore.rules start=null
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Add your security rules here
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Deploying Rules

```bash
# Development
bash scripts/setup-dev-env.sh
firebase deploy --only firestore:rules

# Staging  
bash scripts/setup-staging-env.sh
firebase deploy --only firestore:rules

# Production
bash scripts/setup-prod-env.sh
firebase deploy --only firestore:rules
```

## Development Workflow

### Daily Development

```bash
# 1. Setup development environment
bash scripts/setup-dev-env.sh

# 2. Start Next.js development server
npm run dev

# 3. Develop your features
# ... make changes ...

# 4. Run unit tests with emulators
bash scripts/setup-test-env.sh
npm run emulator:start  # In separate terminal
npm test
```

### Deployment Workflow

```bash
# 1. Test locally with emulator
bash scripts/setup-test-env.sh
npm run emulator:start
npm test

# 2. Deploy to staging
bash scripts/setup-staging-env.sh
firebase deploy

# 3. Test staging environment
# ... manual testing ...

# 4. Deploy to production
bash scripts/setup-prod-env.sh
firebase deploy  # Includes safety confirmations
```

## Troubleshooting

### Common Issues

#### 1. Scripts Won't Execute
**Symptoms:** "Command not found", "Permission denied"

**Causes:**
- Running from Windows PowerShell instead of WSL
- Scripts not executable
- Windows line endings (CRLF)

**Solutions:**
```bash
# Always run in WSL
wsl

# Make scripts executable
chmod +x scripts/*.sh

# Scripts already have Unix line endings (LF)
```

#### 2. Firebase CLI Errors
**Symptoms:** "Project not found", "Authentication required"

**Solutions:**
```bash
# Re-authenticate
firebase login

# List accessible projects
firebase projects:list

# Check current project
firebase use
```

#### 3. Emulator Issues
**Symptoms:** Port conflicts, "EADDRINUSE", emulator won't start

**Solutions:**
```bash
# Kill existing processes
lsof -i :8088  # Check Firestore emulator port
lsof -i :9099  # Check Auth emulator port
lsof -i :4002  # Check UI port

# Kill specific process
kill -9 <PID>

# Or stop all Firebase processes
pkill -f firebase
```

#### 4. Environment Variable Issues
**Symptoms:** Wrong project selected, environment mismatch

**Solutions:**
```bash
# Check current environment
echo $PROJECT_ID
echo $FIREBASE_ENV
firebase use

# Re-run setup script
bash scripts/setup-dev-env.sh
```

#### 5. NPM Script Issues
**Symptoms:** Scripts fail when run from Windows

**Solutions:**
```bash
# Run directly in WSL instead of npm scripts
wsl
cd /home/dawson/code/lang-trak-in-progress
bash scripts/setup-dev-env.sh
```

### Advanced Troubleshooting

#### Check Service Account Permissions
```bash
# List service accounts
gcloud iam service-accounts list

# Check IAM bindings
gcloud projects get-iam-policy lang-trak-dev
```

#### Verify Firebase Configuration
```bash
# Check firebase.json
cat firebase.json

# Check .firebaserc
cat .firebaserc

# Test Firebase CLI connection
firebase projects:list
firebase use --add
```

#### Network Connectivity Issues
```bash
# Test Firebase connectivity
curl https://firebase.googleapis.com/

# Test emulator connectivity
curl http://127.0.0.1:8088
curl http://127.0.0.1:9099
```

## Environment Variables Reference

### Development Environment
```bash
PROJECT_ID="lang-trak-dev"
FIREBASE_ENV="development"
# Firebase CLI project: lang-trak-dev
# Google Cloud project: lang-trak-dev
```

### Test Environment (Emulator)
```bash
NODE_ENV="test"
FIREBASE_ENV="test"
USE_FIREBASE_EMULATOR="true"
FIRESTORE_EMULATOR_HOST="127.0.0.1:8088"
FIREBASE_AUTH_EMULATOR_HOST="127.0.0.1:9099"
# Firebase CLI project: unchanged (uses emulator)
```

### Staging Environment
```bash
PROJECT_ID="lang-trak-staging"
FIREBASE_ENV="staging"
# Firebase CLI project: lang-trak-staging
# Google Cloud project: lang-trak-staging
```

### Production Environment
```bash
PROJECT_ID="lang-trak-prod"
FIREBASE_ENV="production"
# Firebase CLI project: lang-trak-prod
# Google Cloud project: lang-trak-prod
```

## Best Practices

1. **Always use WSL** for Firebase commands and scripts
2. **Use emulators for unit tests only** - never for development
3. **Test in staging** before production deployments
4. **Verify environment** before running commands: `echo $PROJECT_ID`
5. **Keep environments isolated** - never mix data between environments
6. **Use safety confirmations** for production deployments
7. **Monitor logs** after deployments: `firebase functions:log`

## Getting Help

- **Operational Status:** [docs/OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md)
- **Production Readiness:** [docs/PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)
- **Firebase Documentation:** https://firebase.google.com/docs
- **Firebase CLI Reference:** https://firebase.google.com/docs/cli

---

**Need immediate help?** Check [OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md) for current system status and known issues.
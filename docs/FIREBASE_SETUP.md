---
resource_id: "711304fe-e6cb-4bbf-b31f-45bb1e918703"
---
# Firebase Setup Guide

Complete guide to setting up Firebase for Lang Trak following Google's best practices.

<!-- section_id: "d5b98c7b-1a35-4a0c-88cd-041cdbdef982" -->
## Overview

This project implements Google's recommended Firebase architecture:
- **Local emulators** for unit testing only (fast, free, isolated)
- **Real Firebase projects** for development, staging, and production

<!-- section_id: "9d1aaa8f-e765-4f1a-b60a-b6790f1a8e54" -->
## Prerequisites

<!-- section_id: "a8f4d55e-c219-4c6b-a765-9b03073daee9" -->
### Required Software
- **WSL Ubuntu** (mandatory for shell scripts)
- **Node.js** 16+ 
- **Firebase CLI**: `npm install -g firebase-tools`
- **Google Cloud CLI** (recommended): [Install Guide](https://cloud.google.com/sdk/docs/install)

<!-- section_id: "f661b99b-bfe4-4d55-911b-d7346552248a" -->
### Required Permissions
- Google account with access to `lang-trak-*` Firebase projects
- Service account keys properly configured
- IAM roles: Firebase Admin, Firestore User, Cloud Functions Developer

<!-- section_id: "0d901ab3-83c1-4d3a-b69b-f8d87169db1b" -->
## Firebase Projects

| Environment | Project ID | Purpose | URL |
|-------------|------------|---------|-----|
| **Test** | Local emulator | Unit tests only | `http://127.0.0.1:4002` |
| **Development** | `lang-trak-dev` | Daily development | `https://lang-trak-dev.web.app` |
| **Staging** | `lang-trak-staging` | Pre-production testing | `https://lang-trak-staging.web.app` |
| **Production** | `lang-trak-prod` | Live application | `https://lang-trak-prod.web.app` |

<!-- section_id: "bb8ad27f-0e03-4ab6-a060-77b3422f7e40" -->
## Initial Setup

<!-- section_id: "8d5e9330-7fb6-4be7-84cd-7ba3c08f7d3f" -->
### 1. Authenticate with Firebase

```bash
# Login to Firebase (opens browser)
firebase login

# Verify authentication
firebase projects:list

# Should see all lang-trak projects
```

<!-- section_id: "8bd1f511-cdc0-4172-97de-10803e3bbf25" -->
### 2. Authenticate with Google Cloud (Optional but Recommended)

```bash
# Login to Google Cloud
gcloud auth login

# Set default project (choose one)
gcloud config set project lang-trak-dev
```

<!-- section_id: "6776c598-dced-4736-abbd-3a4089fb4233" -->
### 3. Verify Project Access

```bash
# Test each environment
firebase use lang-trak-dev && firebase projects:list --filter="lang-trak-dev"
firebase use lang-trak-staging && firebase projects:list --filter="lang-trak-staging"  
firebase use lang-trak-prod && firebase projects:list --filter="lang-trak-prod"
```

<!-- section_id: "d1cfb099-dba2-4aa9-a95a-273dded3e22f" -->
## Environment Scripts

All environment scripts are located in `scripts/` directory and **must be run in WSL**.

<!-- section_id: "709d01ac-c108-449f-b4bd-4442c59dd0e3" -->
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

<!-- section_id: "00458616-0cc1-421b-aee8-2895da2e90d2" -->
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

<!-- section_id: "91f1ce68-b008-4885-8047-d96afc6da137" -->
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

<!-- section_id: "512ad691-03e1-4211-802f-7558e54d9ad9" -->
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

<!-- section_id: "053a4262-9b26-4a81-80d1-6e71f4d4c899" -->
## Firebase Emulator Setup

<!-- section_id: "543a4952-81ca-40b6-ae9f-0025b48c0ddd" -->
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

<!-- section_id: "df417d48-a355-4f97-8adb-00bdfc2b3797" -->
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

<!-- section_id: "311ca741-ea7f-4b82-970a-9495f67edea0" -->
### Emulator URLs

- **Firestore Emulator:** `http://127.0.0.1:8088`
- **Auth Emulator:** `http://127.0.0.1:9099`  
- **Emulator UI:** `http://127.0.0.1:4002`

<!-- section_id: "7c0e3463-4a8a-4ac4-aaec-59d350628a86" -->
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

<!-- section_id: "a6f14b16-a57c-4e0f-bd1e-e668aaaf2f58" -->
## Security Rules

<!-- section_id: "3d201e0b-dd9d-4d36-b1b3-79c4e8b5f8c7" -->
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

<!-- section_id: "24cf3167-cf0c-48db-a056-4a9954542b8a" -->
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

<!-- section_id: "612001ae-8864-4390-b931-71eb2b141240" -->
## Development Workflow

<!-- section_id: "481db4bd-f84e-499d-9e06-94be8b7a3595" -->
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

<!-- section_id: "8fd4494e-586e-45fa-bd4a-7c423c254888" -->
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

<!-- section_id: "91f452df-ae4c-4108-98a6-d24a1325ff09" -->
## Troubleshooting

<!-- section_id: "c87c61cd-73cc-4e94-976a-93f9db1e8b7d" -->
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

<!-- section_id: "94400a5c-f8b9-486d-8d68-b6b3d6f18225" -->
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

<!-- section_id: "cf4782d9-2135-468c-a2fc-85cc84477d11" -->
## Environment Variables Reference

<!-- section_id: "6088bb4d-a082-4088-8388-f9c94b4c29cd" -->
### Development Environment
```bash
PROJECT_ID="lang-trak-dev"
FIREBASE_ENV="development"
# Firebase CLI project: lang-trak-dev
# Google Cloud project: lang-trak-dev
```

<!-- section_id: "43d0a996-7953-4d74-94fb-708958c93ab2" -->
### Test Environment (Emulator)
```bash
NODE_ENV="test"
FIREBASE_ENV="test"
USE_FIREBASE_EMULATOR="true"
FIRESTORE_EMULATOR_HOST="127.0.0.1:8088"
FIREBASE_AUTH_EMULATOR_HOST="127.0.0.1:9099"
# Firebase CLI project: unchanged (uses emulator)
```

<!-- section_id: "65cc8e87-d38a-4f2a-bede-20451f7d051b" -->
### Staging Environment
```bash
PROJECT_ID="lang-trak-staging"
FIREBASE_ENV="staging"
# Firebase CLI project: lang-trak-staging
# Google Cloud project: lang-trak-staging
```

<!-- section_id: "a903c3b9-58a5-41b5-ba3b-1cb780a8a696" -->
### Production Environment
```bash
PROJECT_ID="lang-trak-prod"
FIREBASE_ENV="production"
# Firebase CLI project: lang-trak-prod
# Google Cloud project: lang-trak-prod
```

<!-- section_id: "6478bc4f-3921-43d3-b721-1f75ad980d54" -->
## Best Practices

1. **Always use WSL** for Firebase commands and scripts
2. **Use emulators for unit tests only** - never for development
3. **Test in staging** before production deployments
4. **Verify environment** before running commands: `echo $PROJECT_ID`
5. **Keep environments isolated** - never mix data between environments
6. **Use safety confirmations** for production deployments
7. **Monitor logs** after deployments: `firebase functions:log`

<!-- section_id: "0ab33a89-6c25-4a88-94b9-b36bb895ad55" -->
## Getting Help

- **Operational Status:** [docs/OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md)
- **Production Readiness:** [docs/PRODUCTION_READINESS.md](PRODUCTION_READINESS.md)
- **Firebase Documentation:** https://firebase.google.com/docs
- **Firebase CLI Reference:** https://firebase.google.com/docs/cli

---

**Need immediate help?** Check [OPERATIONAL_STATUS.md](OPERATIONAL_STATUS.md) for current system status and known issues.
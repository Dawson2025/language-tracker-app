---
resource_id: "48c9368e-2a67-4922-b75d-6fefdd3b4aaa"
---
# Quick Start Guide

Get Lang Trak up and running in 5 minutes!

<!-- section_id: "735d9f59-d4bb-4242-9822-a6ed12cb4a26" -->
## Prerequisites ✅

Make sure you have these installed:

- **WSL Ubuntu** (required for Firebase scripts)
- **Node.js** (16+ recommended)
- **Firebase CLI** (`npm install -g firebase-tools`)
- **Google Cloud CLI** (optional but recommended)
- **Authenticated Google Account** with access to Firebase projects

<!-- section_id: "2c02ac3c-8435-495f-87cc-ce0ef06b8d74" -->
## Step 1: Clone and Install

```bash
# Clone the repository
git clone <repository-url>
cd lang-trak-in-progress

# Install dependencies
npm install
```

<!-- section_id: "41def0be-be11-457f-baff-39bcbf36d74e" -->
## Step 2: Verify Firebase Setup

```bash
# Check Firebase authentication
firebase login

# List available projects
firebase projects:list

# Verify you can see:
# - lang-trak-dev
# - lang-trak-staging  
# - lang-trak-prod
```

<!-- section_id: "8204374a-1b04-4aa4-9174-1e51db61da1d" -->
## Step 3: Start Development

**⚠️ Important: Run all Firebase commands in WSL terminal, not Windows PowerShell**

```bash
# Setup development environment
bash scripts/setup-dev-env.sh

# Start Next.js development server
npm run dev
```

Your app should now be running at `http://localhost:3000`

<!-- section_id: "77f1cd72-ad9b-4ebf-8929-b756806c18ce" -->
## Step 4: Run Unit Tests

```bash
# Setup test environment (uses emulators)
bash scripts/setup-test-env.sh

# Start Firebase emulators in another terminal
firebase emulators:start --only firestore,auth

# Run tests
npm test
```

Emulator UI will be available at `http://127.0.0.1:4002`

<!-- section_id: "d3cd2296-9094-4e9e-a954-7c26358dfd3c" -->
## Step 5: Verify Everything Works

<!-- section_id: "e3cbc753-452a-4436-ab7e-3e9c8a5c1ccc" -->
### Check Development Environment
```bash
# Should show: lang-trak-dev
firebase use

# Should show development project info
firebase projects:list --filter="lang-trak-dev"
```

<!-- section_id: "66c58a4f-bf65-4cdf-8564-9ee8ca45e33b" -->
### Check Emulator
```bash
# Start emulator
firebase emulators:start --only firestore,auth

# In another terminal, verify connection
curl http://127.0.0.1:8088
```

<!-- section_id: "67303944-a111-45ac-bdf4-e5970b3e83f4" -->
### Check NPM Scripts
```bash
# Test environment switching
npm run firebase:dev
npm run firebase:test
npm run firebase:staging
```

<!-- section_id: "f3a5c8ca-5259-4b20-938b-2b91030a0c42" -->
## Common Commands

<!-- section_id: "f835ebb2-8c7f-4a09-9603-3ea4d638043e" -->
### Daily Development
```bash
# Start your development session
bash scripts/setup-dev-env.sh
npm run dev
```

<!-- section_id: "cf02640b-900f-4082-9e40-07cdea525fc7" -->
### Unit Testing
```bash
# Setup test environment
bash scripts/setup-test-env.sh

# Start emulators
npm run emulator:start

# Run tests
npm test
```

<!-- section_id: "c7bc620a-ebd7-4cbf-9dca-1600a9de58b1" -->
### Environment Switching
```bash
npm run firebase:dev      # Development
npm run firebase:test     # Unit testing
npm run firebase:staging  # Staging
npm run firebase:prod     # Production
```

<!-- section_id: "644b55b2-a0c7-4a29-bcb1-94c1bb9e815a" -->
## Troubleshooting 🔧

<!-- section_id: "7aa5f733-280e-4a19-a200-adc9b700a126" -->
### "Command not found" errors
- **Problem:** Running scripts from Windows PowerShell
- **Solution:** Always use WSL terminal: `wsl` then run commands

<!-- section_id: "e1cde994-9f11-4bd6-b71e-fbca60cc17b5" -->
### "Permission denied" errors
- **Problem:** Scripts not executable
- **Solution:** `chmod +x scripts/*.sh`

<!-- section_id: "7a786249-61b3-4a05-bfa8-968611721715" -->
### "Project not found" errors
- **Problem:** Not authenticated with Firebase
- **Solution:** `firebase login` and verify project access

<!-- section_id: "968eb239-b7c7-402b-aefb-05b3cff6333d" -->
### Port conflicts
- **Problem:** Emulator ports already in use
- **Solution:** Stop existing processes: `Ctrl+C` or `lsof -i :8088`

<!-- section_id: "cc1bd50b-8fe7-4454-a31e-ee2ded3a1e0e" -->
### Line ending issues
- **Problem:** Scripts won't execute (Windows CRLF)
- **Solution:** Scripts already fixed with Unix LF endings

<!-- section_id: "08f6aa39-875d-4145-b319-b9b2d8961d2e" -->
## Environment Overview

| Environment | Purpose | Firebase Project | URL |
|-------------|---------|------------------|-----|
| **Test** | Unit testing only | Local emulators | `http://127.0.0.1:4002` |
| **Development** | Daily development | `lang-trak-dev` | `https://lang-trak-dev.web.app` |
| **Staging** | Pre-production testing | `lang-trak-staging` | `https://lang-trak-staging.web.app` |
| **Production** | Live application | `lang-trak-prod` | `https://lang-trak-prod.web.app` |

<!-- section_id: "be29f355-d7a8-4377-a132-60ea0b469aa2" -->
## Next Steps

1. **Read the docs:** Check out [Firebase Setup Guide](FIREBASE_SETUP.md)
2. **Development workflow:** See [Development Workflow](DEV_WORKFLOW.md)  
3. **Deploy to staging:** Follow [Production Readiness](PRODUCTION_READINESS.md)
4. **Monitor status:** Check [Operational Status](OPERATIONAL_STATUS.md)

---

**Need help?** Check the full [Firebase Setup Guide](FIREBASE_SETUP.md) or [Troubleshooting section](FIREBASE_SETUP.md#troubleshooting) for detailed solutions.

**Ready to develop?** 🚀 Run `bash scripts/setup-dev-env.sh` and start coding!
# Firebase Free Tier Setup Guide

This guide will help you set up Firebase for your project using the **free tier** with no paid Google APIs required.

## 🚀 Quick Start

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter your project name (e.g., "my-awesome-app")
4. **Disable Google Analytics** (to avoid any paid features)
5. Click "Create project"

### Step 2: Enable Authentication

1. In your Firebase project, go to **Authentication** → **Sign-in method**
2. Enable **Email/Password** authentication
3. Enable **Google** sign-in (free tier)
4. Add your domain to authorized domains if needed

### Step 3: Set Up Firestore Database

1. Go to **Firestore Database**
2. Click "Create database"
3. Choose **Start in test mode** (for development)
4. Select your preferred location
5. Click "Done"

### Step 4: Set Up Storage

1. Go to **Storage**
2. Click "Get started"
3. Choose **Start in test mode**
4. Select the same location as your Firestore
5. Click "Done"

### Step 5: Get Your Configuration

1. Go to **Project Settings** (gear icon)
2. Scroll down to "Your apps"
3. Click "Add app" → Web app (</>) 
4. Enter your app nickname
5. **Don't check "Firebase Hosting"** (we'll set it up separately)
6. Copy the configuration object

## 🔧 Configuration

### Update Your .env File

Replace the placeholder values in your `.env` file with your actual Firebase configuration:

```env
# Firebase Configuration (Free Tier)
VITE_FIREBASE_API_KEY=your_actual_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-actual-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_actual_sender_id
VITE_FIREBASE_APP_ID=your_actual_app_id
VITE_FIREBASE_MEASUREMENT_ID=your_measurement_id
```

### Update .firebaserc

Edit the `.firebaserc` file and replace the project ID:

```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

## 🆓 Free Tier Limits

Firebase offers generous free tier limits:

- **Authentication**: 50,000 monthly active users
- **Firestore**: 1 GiB storage, 50,000 reads/day, 20,000 writes/day
- **Storage**: 5 GB storage, 1 GB/day downloads
- **Hosting**: 10 GB storage, 360 MB/day transfer
- **Functions**: 125,000 invocations/month, 40,000 GB-seconds/month

## 🛠️ Development Commands

### Install Firebase CLI
```bash
npm install -g firebase-tools
```

### Login to Firebase
```bash
firebase login
```

### Initialize Firebase (if needed)
```bash
firebase init
```

### Start Local Emulators
```bash
firebase emulators:start
```

### Deploy to Firebase Hosting
```bash
npm run build
firebase deploy --only hosting
```

## 🔒 Security Rules

The project includes pre-configured security rules:

- **Firestore**: Users can only access their own data
- **Storage**: Users can only upload/access their own files
- **Authentication**: Email/password and Google sign-in enabled

## 🚨 Important Notes

1. **No Paid APIs Required**: This setup uses only free Firebase services
2. **Web Configuration**: Uses Firebase Web SDK (no server-side APIs needed)
3. **Environment Variables**: All sensitive data is in environment variables
4. **Security**: Never commit your actual API keys to version control

## 🔧 Troubleshooting

### Common Issues

1. **"Firebase not initialized"**: Check your .env file configuration
2. **Authentication errors**: Verify your domain is in authorized domains
3. **Permission denied**: Check your Firestore security rules
4. **Storage upload fails**: Verify Storage security rules

### Getting Help

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Support](https://firebase.google.com/support)

## ✅ Verification

After setup, you should be able to:

1. Sign up/sign in with email and password
2. Sign in with Google
3. Store and retrieve data from Firestore
4. Upload and download files from Storage
5. Deploy your app to Firebase Hosting

Your Firebase integration is now ready to use with the free tier! 🎉
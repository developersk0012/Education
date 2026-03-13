# SK Education Web App

## Files Structure

```
sk-education/
├── index.html          ← Login / Register Page
├── welcome.html        ← Welcome + PDF Card Download
├── sk.png              ← LOGO (upload your logo here)
├── sima.png            ← Slider image (upload here)
├── user/
│   ├── index.html      ← Student Dashboard
│   ├── courses.html    ← All Courses Page
│   ├── profile.html    ← Student Profile
│   ├── chat.html       ← Chat with Admin
│   └── downloads.html  ← PDF Downloads
└── admin/
    └── index.html      ← Admin Panel
```

## Setup Instructions

### 1. Logo Files
- Replace `sk.png` with your SK Education logo
- Replace `sima.png` with your slider/banner image

### 2. Firebase Setup
- Go to Firebase Console → Authentication → Enable Phone Authentication
- Add your domain to authorized domains in Firebase Console
- Enable Realtime Database and set rules:

```json
{
  "rules": {
    "users": { ".read": "auth != null", ".write": "auth != null" },
    "courses": { ".read": true, ".write": false },
    "slider": { ".read": true, ".write": false },
    "chats": { ".read": "auth != null", ".write": "auth != null" }
  }
}
```

### 3. Admin Panel
- URL: `yoursite.com/admin/`
- Default Password: `SKAdmin@2026`
- Change this password in `admin/index.html` line containing `SKAdmin@2026`

### 4. Hosting on GitHub Pages / Netlify
1. Upload all files to GitHub repository
2. Enable GitHub Pages from Settings → Pages
3. Your site will be live at: `https://username.github.io/reponame/`

## Admin Panel Features
- View total users, courses stats
- Add courses (YouTube video / PDF link)
- Set category: Hindi, Sanskrit, Math, Science, History
- Set subcategory: Subjective, Objective, Notes
- Manage slider images
- View all registered students

## User Panel Features
- Register with mobile OTP
- Auto-download PDF ID card on registration
- Browse free & paid courses
- Filter by subject category
- Watch YouTube videos inline
- Open PDF notes
- Chat with admin
- Download notes

## Course Image Hosting
Upload images to: https://imgbb.com or https://imgur.com
Then paste the direct image link in Admin → Add Course → Poster Image Link

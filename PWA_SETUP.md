# Progressive Web App (PWA) Setup

Brain Quest is now a full Progressive Web App that works on desktop, mobile browsers, and can be installed as a native app on iOS and Android!

## What's New

✅ **PWA Features Enabled:**
- 📱 Installable on Android & iOS
- 💾 Offline-first with service worker caching
- 🎯 App shortcuts on home screen
- 🔔 Native app experience (no browser UI)
- 🚀 Fast load times with intelligent caching
- 📡 Automatic updates when new versions deploy

## Installation

### Android Chrome / Edge / Samsung Browser
1. Open [https://smarty5.com](https://smarty5.com)
2. Tap the menu (⋮) → **"Install app"** or look for **"Add to Home Screen"**
3. App installs instantly

### iOS (Safari)
1. Open [https://smarty5.com](https://smarty5.com) in Safari
2. Tap the Share button (⬆️)
3. Scroll down and tap **"Add to Home Screen"**
4. Tap "Add" in the top-right
5. App appears on your home screen (works like native app)

### Desktop (Chrome/Edge)
1. Visit [https://smarty5.com](https://smarty5.com)
2. Look for **install icon** in address bar (🖥️ + down arrow)
3. Or use menu → **"Install Brain Quest"**

## How It Works

### Service Worker (`service-worker.js`)
- Caches static assets (CSS, JS, fonts)
- Enables offline fallback page
- Serves cached content instantly
- Automatically syncs with server when online

### Web App Manifest (`manifest.json`)
- Defines app name, icons, colors
- Sets app shortcuts (Math, Quest, Flashcards)
- Specifies standalone display mode
- Provides app store metadata

### PWA Initialization (`pwa-init.js`)
- Registers service worker on page load
- Handles install prompts
- Detects online/offline status
- Shows update notifications

## What Works Offline

✅ **Cached:**
- Static pages (Home, Settings, etc.)
- CSS, JavaScript, Fonts
- Previously visited content

❌ **Requires Connection:**
- LLM features (AI explanations, hints)
- Live news in Daily Discovery
- User authentication
- Real-time data sync

## Deployment on Render

No extra setup needed! PWA works automatically:

1. Manifest served from `/static/manifest.json`
2. Service worker at `/static/service-worker.js`
3. All routes fallback to offline page when needed

The app is production-ready for Render, Apple App Store, and Google Play Store.

## Testing Locally

```bash
# Start dev server
python manage.py runserver

# Open http://localhost:8000
# Dev tools: Chrome DevTools → Application → Manifest & Service Workers
```

### Simulate Offline
1. Chrome DevTools → Network tab
2. Check **"Offline"** checkbox
3. Refresh page → sees cached content

## Icons & Branding

- **App Icon:** SVG emoji (🦊) with purple background
- **Colors:** Theme purple (#7c5cff), Accent pink (#ff5fa2)
- **Shortcuts:** Math (🧮), Quest (🚀), Flashcards (🃏)

All generated programmatically from SVG — no image files needed.

## Browser Support

| Browser | Android | iOS | Desktop |
|---------|---------|-----|---------|
| Chrome | ✅ Full PWA | ✅ Web App | ✅ Full PWA |
| Safari | N/A | ✅ Web App | ✅ Web App |
| Edge | ✅ Full PWA | ✅ Web App | ✅ Full PWA |
| Firefox | ⚠️ Limited | ❌ | ⚠️ Limited |

**Full PWA** = installable + service worker + offline
**Web App** = installable only, limited offline
**Limited** = works but some features missing

## Future Enhancements

- [ ] Sync quiz answers when back online
- [ ] Background sync for achievements
- [ ] Push notifications for daily reminders
- [ ] Share results to social media
- [ ] Native file access (photos, documents)

## Troubleshooting

**"Install button not showing"**
- Only shows once per browser/device
- Already installed? Check home screen or app drawer
- Try different browser

**"App freezes offline"**
- Check Service Worker in DevTools
- Clear cache: Settings → Clear site data
- Service worker updates every 60s

**"Changes not appearing"**
- Service worker caches aggressively
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Wait 60s for update check

---

Built with ❤️ for curious kids ages 7–10. Brain Quest — Feel Brilliant Before Breakfast! 🦊

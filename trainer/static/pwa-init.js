// PWA Registration and Install Handling

let deferredPrompt;
const INSTALL_PROMPT_DISMISSED_KEY = 'pwa_install_dismissed_at';
const DISMISS_DURATION_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

// Check if install prompt was recently dismissed
function shouldShowInstallPrompt() {
  const dismissedAt = localStorage.getItem(INSTALL_PROMPT_DISMISSED_KEY);
  if (!dismissedAt) return true;
  const timeSinceDismiss = Date.now() - parseInt(dismissedAt);
  return timeSinceDismiss > DISMISS_DURATION_MS;
}

// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/service-worker.js', {
      scope: '/'
    }).then(registration => {
      console.log('Service Worker registered:', registration);

      // Check for updates periodically
      setInterval(() => {
        registration.update();
      }, 60000); // Check every minute
    }).catch(error => {
      console.log('Service Worker registration failed:', error);
    });
  });

  // Listen for controller change (service worker updated)
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    // Show update notification to user
    if (navigator.onLine) {
      showUpdatePrompt();
    }
  });
}

// Handle PWA Install Prompt
window.addEventListener('beforeinstallprompt', event => {
  // Don't show on quiz/active task pages
  if (window.location.pathname.includes('/math-challenge/quiz/') ||
      window.location.pathname.includes('/challenge/') ||
      window.location.pathname.includes('/spelling/') ||
      window.location.pathname.includes('/mental-quiz/')) {
    return;
  }

  // Only show if not recently dismissed
  if (!shouldShowInstallPrompt()) {
    return;
  }

  event.preventDefault();
  deferredPrompt = event;

  // Show install button/banner
  const installBanner = document.getElementById('install-banner');
  if (installBanner) {
    installBanner.style.display = 'flex';
  }
});

// Handle app installed
window.addEventListener('appinstalled', () => {
  console.log('Brain Quest installed as app');
  const installBanner = document.getElementById('install-banner');
  if (installBanner) {
    installBanner.style.display = 'none';
  }
  deferredPrompt = null;
});

// Install button handler
function installApp() {
  if (!deferredPrompt) {
    return;
  }
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(choiceResult => {
    if (choiceResult.outcome === 'accepted') {
      console.log('User accepted install prompt');
      localStorage.setItem(INSTALL_PROMPT_DISMISSED_KEY, Date.now().toString());
    } else {
      markInstallPromptDismissed();
    }
    deferredPrompt = null;
    const installBanner = document.getElementById('install-banner');
    if (installBanner) installBanner.style.display = 'none';
  });
}

// Mark install prompt as dismissed
function markInstallPromptDismissed() {
  localStorage.setItem(INSTALL_PROMPT_DISMISSED_KEY, Date.now().toString());
}

// Check if running as standalone app
function isStandaloneApp() {
  return window.matchMedia('(display-mode: standalone)').matches ||
         navigator.standalone === true;
}

// Show update notification
function showUpdatePrompt() {
  const msg = document.createElement('div');
  msg.style.cssText = `
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%);
    background: #2bd99f;
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 0.5rem;
    z-index: 9999;
    max-width: 90%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  `;
  msg.innerHTML = '✅ Brain Quest updated! <a href="#" onclick="location.reload(); return false;" style="color:white; text-decoration:underline; margin-left:0.5rem;">Refresh</a>';
  document.body.appendChild(msg);
  setTimeout(() => msg.remove(), 5000);
}

// Detect online/offline status
window.addEventListener('online', () => {
  console.log('Back online');
});

window.addEventListener('offline', () => {
  console.log('Going offline - cached content will be served');
});

console.log('PWA initialized - Standalone:', isStandaloneApp());

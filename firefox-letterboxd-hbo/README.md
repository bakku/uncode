# Letterboxd Ratings for HBO Max

A Firefox extension that displays [Letterboxd](https://letterboxd.com) ratings for films while browsing [HBO Max](https://play.max.com).

## Features

- Automatically detects when you're viewing a film on HBO Max
- Fetches the Letterboxd community rating for that film
- Displays a rating badge with score and star rating next to the film title
- Click the badge to open the film's Letterboxd page

## Installation

### Temporary Installation (Development)

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
2. Click **Load Temporary Add-on…**
3. Select the `manifest.json` file from this directory

### Permanent Installation

1. Zip all extension files:
   ```bash
   cd firefox-letterboxd-hbo
   zip -r letterboxd-hbo.zip manifest.json background.js content.js styles.css popup.html popup.js popup.css icons/
   ```
2. Submit the `.zip` to [Firefox Add-ons](https://addons.mozilla.org/developers/) for signing
3. Install the signed `.xpi` file in Firefox

## How It Works

1. **Content Script** (`content.js`) runs on `play.max.com` pages and monitors for film detail pages
2. When a film title is detected, it sends a message to the **Background Script** (`background.js`)
3. The background script fetches the film's page from Letterboxd (first trying a direct slug match, then falling back to search)
4. The rating is extracted and sent back to the content script
5. A styled badge is injected into the page showing the Letterboxd rating

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Extension manifest (Manifest V2) |
| `content.js` | Content script injected into HBO Max pages |
| `background.js` | Background script handling Letterboxd requests |
| `styles.css` | Styles for the rating badge |
| `popup.html` | Browser action popup UI |
| `popup.js` | Popup logic |
| `popup.css` | Popup styles |
| `icons/` | Extension icons (SVG) |

## Permissions

- **`https://letterboxd.com/*`** — Required to fetch film ratings from Letterboxd
- **Content script access to `play.max.com`** — Required to detect films and inject the rating badge

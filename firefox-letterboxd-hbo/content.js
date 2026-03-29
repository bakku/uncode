const BADGE_ID = "letterboxd-rating-badge";
const CHECK_INTERVAL_MS = 2000;

let lastTitle = null;
let currentUrl = location.href;

function getFilmTitle() {
  const heading = document.querySelector(
    'h2[class*="title"], h1[class*="title"], [data-testid="title"]'
  );
  if (heading) {
    return heading.textContent.trim();
  }

  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) {
    const content = ogTitle.getAttribute("content");
    if (content) {
      return content.replace(/\s*\|.*$/, "").trim();
    }
  }

  const titleTag = document.querySelector("title");
  if (titleTag) {
    const text = titleTag.textContent;
    const cleaned = text.replace(/\s*[-|].*HBO.*$/i, "").trim();
    if (cleaned && cleaned !== text.trim()) {
      return cleaned;
    }
  }

  return null;
}

function isDetailPage() {
  const path = window.location.pathname;
  // HBO Max uses paths like /movie/<slug> and /feature/<slug> for film pages.
  // The second pattern matches /<section>/<slug> (e.g. /video/watch/...)
  // which covers other possible HBO Max detail page layouts.
  return /^\/(movie|film|feature)\//.test(path) || /^\/video\/watch\//.test(path);
}

function removeBadge() {
  const existing = document.getElementById(BADGE_ID);
  if (existing) {
    existing.remove();
  }
}

function createBadge(data) {
  removeBadge();

  const badge = document.createElement("a");
  badge.id = BADGE_ID;
  badge.href = data.url;
  badge.target = "_blank";
  badge.rel = "noopener noreferrer";
  badge.title = `Letterboxd: ${data.rating} / ${data.outOf}`;

  const stars = ratingToStars(data.rating);

  badge.innerHTML = `
    <span class="letterboxd-badge-logo">
      <svg width="18" height="18" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        <circle cx="250" cy="250" r="240" fill="#00E054"/>
        <circle cx="160" cy="250" r="80" fill="#40BCF4" opacity="0.8"/>
        <circle cx="340" cy="250" r="80" fill="#FF8000" opacity="0.8"/>
      </svg>
    </span>
    <span class="letterboxd-badge-rating">${data.rating.toFixed(1)}</span>
    <span class="letterboxd-badge-stars">${stars}</span>
  `;

  const titleContainer = document.querySelector(
    'h2[class*="title"], h1[class*="title"], [data-testid="title"]'
  );
  const target = titleContainer
    ? titleContainer.parentElement
    : document.querySelector('[class*="detail"], [class*="Detail"]');

  if (target) {
    target.appendChild(badge);
  } else {
    document.body.appendChild(badge);
  }
}

function createErrorBadge(message) {
  removeBadge();

  const badge = document.createElement("span");
  badge.id = BADGE_ID;
  badge.className = "letterboxd-badge-error";

  badge.innerHTML = `
    <span class="letterboxd-badge-logo">
      <svg width="18" height="18" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
        <circle cx="250" cy="250" r="240" fill="#556677"/>
        <circle cx="160" cy="250" r="80" fill="#40BCF4" opacity="0.5"/>
        <circle cx="340" cy="250" r="80" fill="#FF8000" opacity="0.5"/>
      </svg>
    </span>
    <span class="letterboxd-badge-text">${message}</span>
  `;

  const titleContainer = document.querySelector(
    'h2[class*="title"], h1[class*="title"], [data-testid="title"]'
  );
  const target = titleContainer
    ? titleContainer.parentElement
    : document.querySelector('[class*="detail"], [class*="Detail"]');

  if (target) {
    target.appendChild(badge);
  }
}

function ratingToStars(rating) {
  const fullStars = Math.floor(rating);
  const halfStar = rating - fullStars >= 0.5;
  let stars = "★".repeat(fullStars);
  if (halfStar) {
    stars += "½";
  }
  return stars;
}

async function checkForFilm() {
  if (!isDetailPage()) {
    removeBadge();
    lastTitle = null;
    return;
  }

  const title = getFilmTitle();
  if (!title || title === lastTitle) {
    return;
  }

  lastTitle = title;
  removeBadge();

  try {
    const response = await browser.runtime.sendMessage({
      type: "fetchLetterboxdRating",
      title,
    });

    if (response.error) {
      createErrorBadge(response.error);
    } else {
      createBadge(response);
    }
  } catch {
    createErrorBadge("Could not fetch rating");
  }
}

function onUrlChange() {
  if (location.href !== currentUrl) {
    currentUrl = location.href;
    lastTitle = null;
    removeBadge();
    checkForFilm();
  }
}

// Use a MutationObserver as the primary mechanism to detect SPA navigation
// and page content changes on HBO Max.
const observer = new MutationObserver(() => {
  onUrlChange();
});

observer.observe(document.body, { childList: true, subtree: true });

// Fallback polling interval for cases where DOM mutations don't fire
// (e.g. HBO Max updates content without triggering observable mutations).
setInterval(onUrlChange, CHECK_INTERVAL_MS);

checkForFilm();

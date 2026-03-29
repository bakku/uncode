browser.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === "fetchLetterboxdRating") {
    fetchRating(message.title)
      .then((result) => sendResponse(result))
      .catch(() => sendResponse({ error: "Failed to fetch rating" }));
    return true;
  }
});

function slugify(title) {
  return title
    .toLowerCase()
    .replace(/['']/g, "")
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

async function fetchRating(title) {
  const slug = slugify(title);
  const url = `https://letterboxd.com/film/${slug}/`;

  const response = await fetch(url);
  if (!response.ok) {
    return await searchAndFetchRating(title);
  }

  const html = await response.text();
  return parseRatingFromHtml(html, url);
}

async function searchAndFetchRating(title) {
  const searchUrl = `https://letterboxd.com/search/films/${encodeURIComponent(title)}/`;
  const response = await fetch(searchUrl);
  if (!response.ok) {
    return { error: "Film not found on Letterboxd" };
  }

  const html = await response.text();
  const filmLinkMatch = html.match(
    /<span class="film-title-wrapper">\s*<a href="(\/film\/[^"]+\/)"/
  );
  if (!filmLinkMatch) {
    return { error: "Film not found on Letterboxd" };
  }

  const filmUrl = `https://letterboxd.com${filmLinkMatch[1]}`;
  const filmResponse = await fetch(filmUrl);
  if (!filmResponse.ok) {
    return { error: "Could not load film page" };
  }

  const filmHtml = await filmResponse.text();
  return parseRatingFromHtml(filmHtml, filmUrl);
}

function parseRatingFromHtml(html, url) {
  const ratingMatch = html.match(
    /name="twitter:data2"\s+content="([\d.]+) out of 5"/
  );

  const titleMatch = html.match(
    /<meta\s+property="og:title"\s+content="([^"]+)"/
  );

  if (!ratingMatch) {
    return { error: "Rating not available", url };
  }

  const rating = parseFloat(ratingMatch[1]);
  const filmTitle = titleMatch ? titleMatch[1] : "";

  return {
    rating,
    title: filmTitle,
    url,
    outOf: 5,
  };
}

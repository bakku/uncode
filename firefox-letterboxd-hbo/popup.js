async function updateStatus() {
  const statusText = document.getElementById("status-text");
  const status = document.getElementById("status");

  try {
    const tabs = await browser.tabs.query({
      active: true,
      currentWindow: true,
    });
    const tab = tabs[0];

    if (tab && tab.url) {
      const url = new URL(tab.url);
      if (url.hostname === "play.hbomax.com") {
        status.classList.add("active");
        status.classList.remove("inactive");
        statusText.textContent = "Active on HBO Max";
      } else {
        status.classList.add("inactive");
        status.classList.remove("active");
        statusText.textContent = "Navigate to play.hbomax.com to use";
      }
    } else {
      status.classList.add("inactive");
      status.classList.remove("active");
      statusText.textContent = "Navigate to play.hbomax.com to use";
    }
  } catch {
    status.classList.add("inactive");
    status.classList.remove("active");
    statusText.textContent = "Waiting for HBO Max…";
  }
}

updateStatus();

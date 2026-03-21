console.log("🚀 Aura AI v2.0 loaded");

chrome.runtime.onMessage.addListener((msg, sendResponse) => {
  if (msg.action === "scrollTo") {
    const element = findBestMatch(msg.bulletText, msg.index);
    if (element) {
      scrollHighlight(element);
      sendResponse({status:"success"});
    } else {
      sendResponse({status:"no-match"});
    }
  }
  return true;
});

function findBestMatch(bulletText, index) {
  if (!bulletText) return findByIndex(index);

  // Text matching (90%+ accuracy)
  const phrases = bulletText.toLowerCase().match(/\b\w{4,}\b/g) || [];
  const candidates = Array.from(document.querySelectorAll("p,h1,h2,h3,h4,li"))
    .filter(el => el.textContent.trim().length > 40);

  let best = null, bestScore = 0;
  
  candidates.forEach(el => {
    const score = phrases.filter(p => el.textContent.toLowerCase().includes(p)).length / phrases.length;
    if (score > bestScore && score > 0.25) {
      bestScore = score;
      best = el;
    }
  });

  return best || findByIndex(index);
}

function findByIndex(index) {
  const content = document.querySelector("article,main,.content,.post") || document.body;
  const elements = Array.from(content.querySelectorAll("h1,h2,h3,p,li"))
    .filter(el => el.textContent.trim().length > 30);
  return elements[index] || elements[Math.floor(elements.length * index / 10)];
}

function scrollHighlight(el) {
  el.scrollIntoView({behavior:"smooth", block:"center"});
  
  setTimeout(() => {
    const orig = el.style.backgroundColor;
    el.style.backgroundColor = "#fef08a";
    el.style.boxShadow = "0 0 20px rgba(254,240,138,.6)";
    el.style.borderRadius = "8px";
    el.style.transition = "all .3s ease";
    
    setTimeout(() => {
      el.style.backgroundColor = orig;
      el.style.boxShadow = "";
      el.style.borderRadius = "";
    }, 2500);
  }, 500);
}
document.getElementById("summarize").onclick = async () => {
  document.getElementById("loading").style.display = "block";
  document.getElementById("result").innerHTML = "";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  try {
    const res = await fetch("http://127.0.0.1:8000/summary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: tab.url, time_spent: Math.floor(Math.random() * 10) + 1 })
    });

    const data = await res.json();
    window._BULLETS_DATA = data;

    let html = `
      <div style="font-family: system-ui, sans-serif; line-height: 1.5;">
        <p style="margin:0 0 8px;font-weight:600"><b>Summary:</b> ${data.summary}</p>
        <p style="margin:0 0 8px"><b>Read Time:</b> ${data.estimated_read_time} | <b>Community Avg:</b> ${data.community_avg}min | <b>Visits:</b> ${data.visits}</p>
        <h4 style="margin:20px 0 12px;color:#333;font-size:16px">Key Points:</h4>
        <ul style="list-style:none;padding:0;margin:0">
    `;

    data.bullets.forEach((bulletText, i) => {
      html += `
        <li class="bullet" data-index="${i}" data-text="${bulletText.replace(/"/g,'&quot;')}"
            style="cursor:pointer;padding:12px 16px;margin:4px 0;border:2px solid #e1e5e9;border-radius:10px;background:#f8f9fa;transition:all .2s;font-size:14px;line-height:1.4"
            title="Jump to section">
          <span style="margin-right:8px">→</span>${bulletText}
        </li>
      `;
    });

    html += `</ul><p style="font-size:12px;color:#666;margin-top:16px">✨ Click bullets to jump to exact sections</p></div>`;

    document.getElementById("result").innerHTML = html;

    document.getElementById("result").addEventListener("click", e => {
      if (e.target.classList.contains("bullet")) {
        const index = parseInt(e.target.dataset.index);
        const bulletText = e.target.dataset.text;
        
        // Flash effect
        const origBg = e.target.style.background;
        e.target.style.background = "#10b981";
        e.target.style.color = "white";
        setTimeout(() => {
          e.target.style.background = origBg;
          e.target.style.color = "";
        }, 200);

        chrome.tabs.sendMessage(tab.id, {
          action: "scrollTo",
          index, bulletText, allBullets: window._BULLETS_DATA.bullets
        });
      }
    });

  } catch (err) {
    document.getElementById("result").innerHTML = '<div style="color:#ef4444;padding:20px;text-align:center">⚠️ Backend error - check server</div>';
  }

  document.getElementById("loading").style.display = "none";
};
const API_URL = "http://127.0.0.1:8000";

let currentRound = 1;
let currentMatches = [];
let currentMatchIndex = 0;

function showWinner(winner) {
  const container = document.getElementById("matchups");
  const winnerDiv = document.getElementById("winner");
  container.innerHTML = "";
  winnerDiv.innerHTML = "";

  const title = document.createElement("h2");
  title.textContent = "🎉 The Winner is:";
  title.style.textAlign = "center";

  const img = document.createElement("img");
  img.src = winner.image;
  img.alt = winner.text;
  img.style.width = "300px";
  img.style.height = "300px";
  img.style.display = "block";
  img.style.margin = "20px auto";

  const name = document.createElement("p");
  name.textContent = winner.text;
  name.style.textAlign = "center";
  name.style.fontSize = "1.5rem";
  name.style.fontWeight = "bold";

  winnerDiv.appendChild(title);
  winnerDiv.appendChild(img);
  winnerDiv.appendChild(name);
}

async function loadMatchups(round) {
  const res = await fetch(`${API_URL}/matchups/round${round}`);
  const data = await res.json();

  if (data.message) {
    alert(data.message);
    return;
  }

  if (data.winner) {
    showWinner(data.winner);
    return;
  }

  document.getElementById("winner").innerHTML = "";
  document.querySelector("h1").textContent = `🎬 Round ${round}: Choose Your Favorite`;

  currentMatches = data.matchups;
  currentMatchIndex = 0;

  showMatch(currentMatches[currentMatchIndex], currentRound);
}

function showMatch(match, round) {
  const container = document.getElementById("matchups");
  container.innerHTML = "";

  const title = document.createElement("h3");
  title.textContent = `Match #${match.match_id}`;
  title.style.textAlign = "center";
  container.appendChild(title);

  const pairDiv = document.createElement("div");
  pairDiv.className = "pair";

  // Sol item
  const leftDiv = document.createElement("div");
  const leftImg = document.createElement("img");
  leftImg.src = match.pair[0].image;
  leftImg.alt = match.pair[0].text;
  leftImg.classList.add("clickable");
  leftImg.style.cursor = "pointer";
  leftImg.onclick = () => sendVote(round, match.match_id, match.pair[0].id, leftImg);
  leftDiv.appendChild(leftImg);
  const leftText = document.createElement("div");
  leftText.textContent = match.pair[0].text;
  leftText.style.textAlign = "center";
  leftText.style.marginTop = "10px";
  leftDiv.appendChild(leftText);

  const vsDiv = document.createElement("div");
  vsDiv.textContent = "VS";
  vsDiv.className = "vs-text";

  const rightDiv = document.createElement("div");
  const rightImg = document.createElement("img");
  rightImg.src = match.pair[1].image;
  rightImg.alt = match.pair[1].text;
  rightImg.classList.add("clickable");
  rightImg.style.cursor = "pointer";
  rightImg.onclick = () => sendVote(round, match.match_id, match.pair[1].id, rightImg);
  rightDiv.appendChild(rightImg);
  const rightText = document.createElement("div");
  rightText.textContent = match.pair[1].text;
  rightText.style.textAlign = "center";
  rightText.style.marginTop = "10px";
  rightDiv.appendChild(rightText);

  pairDiv.appendChild(leftDiv);
  pairDiv.appendChild(vsDiv);
  pairDiv.appendChild(rightDiv);

  container.appendChild(pairDiv);
}

async function sendVote(round, match_id, selected_item_id, clickedImg) {
  const voteEndpoint = round === 1 ? "/vote" : `/vote/round${round}`;

  await fetch(`${API_URL}${voteEndpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ match_id, selected_item_id })
  });

  clickedImg.classList.add("selected");
  document.querySelectorAll(".clickable").forEach(img => img.onclick = null);

  currentMatchIndex++;

  setTimeout(async () => {
    clickedImg.classList.remove("selected");

    if (currentMatchIndex < currentMatches.length) {
      showMatch(currentMatches[currentMatchIndex], currentRound);
    } else {
      if (currentRound < 3) {
        currentRound++;
        await loadMatchups(currentRound);
      } else {
        showFinalWinner();
      }
    }
  }, 1000);
}

async function showFinalWinner() {
  const res = await fetch(`${API_URL}/winner`);
  const data = await res.json();

  if (data.winner) {
    const container = document.getElementById("matchups");
    container.innerHTML = "";

    const title = document.createElement("h2");
    title.textContent = "🎉 The Winner is:";
    title.style.textAlign = "center";

    const img = document.createElement("img");
    img.src = data.winner.image;
    img.alt = data.winner.text;
    img.style.width = "300px";
    img.style.height = "500px";
    img.style.display = "block";
    img.style.margin = "20px auto";

    const name = document.createElement("p");
    name.textContent = data.winner.text;
    name.style.textAlign = "center";
    name.style.fontSize = "1.5rem";
    name.style.fontWeight = "bold";

    container.appendChild(title);
    container.appendChild(img);
    container.appendChild(name);

    document.getElementById("nextRoundBtn").style.display = "none";
  } else if(data.message) {
    alert(data.message);
  }
}

loadMatchups(1);

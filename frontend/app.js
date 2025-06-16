async function askBot() {
  const userInput = document.getElementById("userInput").value;
  const responseArea = document.getElementById("responseArea");
  responseArea.innerText = "Thinking...";

  const response = await fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: userInput })
  });

  const data = await response.json();
  const res = data.response;

  if (data.source === "local") {
    responseArea.innerText =
      `📜 Kural ${res.number}:
${res.kural}

📝 Meaning:
${res.translation}

🔍 Explanation:
${res.explanation}`;
  } else {
    responseArea.innerText = res.message;
  }
}

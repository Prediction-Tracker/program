document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictionForm");
  const resultDiv = document.getElementById("result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const ticker = document.getElementById("ticker").value.trim().toUpperCase();
    const amount = parseFloat(document.getElementById("amount").value);
    const country = document.getElementById("country").value;
    const sendCopy = document.getElementById("sendCopy").value;

    if (!email || !ticker || isNaN(amount) || amount <= 0 || !country) {
      resultDiv.textContent = "Please fill in all fields correctly.";
      resultDiv.style.color = "red";
      return;
    }

    const data = { email, ticker, amount, send_copy: sendCopy, country };

    try {
      const response = await fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const resData = await response.json();

      if (response.ok) {
        resultDiv.textContent = resData.success;
        resultDiv.style.color = "green";
        form.reset();
      } else {
        resultDiv.textContent = resData.error || "Error submitting the form.";
        resultDiv.style.color = "red";
      }
    } catch (error) {
      resultDiv.textContent = "Network or server error.";
      resultDiv.style.color = "red";
      console.error(error);
    }
  });
});

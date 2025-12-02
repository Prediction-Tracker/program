// script.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("predictionForm");
  const resultDiv = document.getElementById("result");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // evita refresh da página

    // Captura os valores do formulário
    const email = document.getElementById("email").value.trim();
    const ticker = document.getElementById("ticker").value.trim().toUpperCase();
    const amount = parseFloat(document.getElementById("amount").value);
    const sendCopy = document.getElementById("sendCopy").value;

    // Validações básicas
    if (!email || !ticker || isNaN(amount) || amount <= 0) {
      resultDiv.textContent = "Please fill in all fields correctly.";
      resultDiv.style.color = "red";
      return;
    }

    // Prepara os dados para envio
    const data = { email, ticker, amount, send_copy: sendCopy };

    try {
      // Faz requisição para o backend
      const response = await fetch("/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const resData = await response.json();

      if (response.ok) {
        resultDiv.textContent = resData.success;
        resultDiv.style.color = "green";
        form.reset(); // limpa o formulário
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

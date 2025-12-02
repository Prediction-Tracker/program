const backendUrl = "https://program-production-b75c.up.railway.app/predict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predictionForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const ticker = document.getElementById("ticker").value.trim().toUpperCase();

        if (!ticker) {
            alert("Please enter a stock ticker.");
            return;
        }

        try {
            const response = await fetch(backendUrl, {  // <--- usa a variável aqui
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ticker })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            localStorage.setItem("sma_img", data.sma_img);
            localStorage.setItem("forecast_img", data.forecast_img);
            localStorage.setItem("ticker", ticker);

            window.location.href = "results.html";

        } catch (err) {
            console.error(err);
            alert("Error connecting to backend. Make sure the Railway app is running.");
        }
    });
});

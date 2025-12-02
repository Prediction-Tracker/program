const backendUrl = "https://program-production-b75c.up.railway.app/predict";

document.querySelector("#predictionForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const ticker = document.querySelector("#tickerInput").value.trim().toUpperCase();

    if (!ticker) {
        alert("Please enter a ticker.");
        return;
    }

    try {
        const response = await fetch(backendUrl, {
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
        window.location.href = "results.html";

    } catch (err) {
        console.error(err);
        alert("Error connecting to the backend. Make sure it is deployed and the URL is correct.");
    }
});

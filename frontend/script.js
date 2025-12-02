document.getElementById("tickerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const ticker = document.getElementById("ticker").value.trim().toUpperCase();

    const res = await fetch("https://your.backend.url/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker })
    });

    const data = await res.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("sma_img").src = "data:image/png;base64," + data.sma_img;
    document.getElementById("forecast_img").src = "data:image/png;base64," + data.forecast_img;
});

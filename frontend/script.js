document.addEventListener("DOMContentLoaded", () => {

    const backendUrl = "https://program-production-b75c.up.railway.app/predict";

    const form = document.getElementById('predictionForm');
    const smaDiv = document.getElementById('smaChart');
    const forecastDiv = document.getElementById('forecastChart');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const ticker = document.getElementById('ticker').value.trim().toUpperCase();
        if (!ticker) {
            alert("Please enter a stock ticker.");
            return;
        }

        smaDiv.innerHTML = "";
        forecastDiv.innerHTML = "";

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

            const smaImg = document.createElement('img');
            smaImg.src = `data:image/png;base64,${data.sma_img}`;
            smaDiv.appendChild(smaImg);

            const forecastImg = document.createElement('img');
            forecastImg.src = `data:image/png;base64,${data.forecast_img}`;
            forecastDiv.appendChild(forecastImg);

        } catch (err) {
            console.error(err);
            alert("Erro conectando ao backend.");
        }
    });
});

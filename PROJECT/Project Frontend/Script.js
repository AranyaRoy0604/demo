function predictEnergy() {
  const household_size = document.getElementById("household_size").value;
  const temperature = document.getElementById("temperature").value;
  const has_ac = document.getElementById("has_ac").value;
  const peak_usage = document.getElementById("peak_usage").value;

  // Basic validation
  if (!household_size || !temperature || !has_ac || !peak_usage) {
    document.getElementById("result").innerText = "⚠️ Please fill in all fields.";
    return;
  }

  const data = {
    household_size: Number(household_size),
    temperature: Number(temperature),
    has_ac: Number(has_ac),
    peak_usage: Number(peak_usage)
  };

  // Show loading state
  document.getElementById("result").innerText = "⏳ Predicting energy consumption...";

  fetch("http://127.0.0.1:80/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      if (result.error) {
        document.getElementById("result").innerText = " Error: " + result.error;
      } else {
        document.getElementById("result").innerText =
          "✅ Predicted Energy Consumption: " + result.predicted_energy + " kWh";
      }
    })
    .catch(error => {
      document.getElementById("result").innerText = " Request failed: " + error;
    });
}
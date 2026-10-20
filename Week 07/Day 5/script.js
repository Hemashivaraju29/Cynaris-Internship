const API = "http://127.0.0.1:8000";
let sessionId = null;
let chartInstance = null;

const fileInput = document.getElementById("csvFile");
const uploadStatus = document.getElementById("uploadStatus");
const questionInput = document.getElementById("question");
const answerElement = document.getElementById("answer");

document.getElementById("uploadBtn").addEventListener("click", async () => {
  const file = fileInput.files[0];

  if (!file) {
    uploadStatus.textContent = "Please choose a CSV file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  uploadStatus.textContent = "Uploading...";

  try {
    const response = await fetch(`${API}/cia/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Upload failed.");
    }

    sessionId = data.session_id;
    uploadStatus.textContent = `Uploaded ${data.filename} (${data.rows} rows).`;
  } catch (error) {
    uploadStatus.textContent = `Error: ${error.message}`;
  }
});

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  if (!sessionId) {
    answerElement.textContent = "Upload a CSV before asking a question.";
    return;
  }

  const question = questionInput.value.trim();

  if (!question) {
    answerElement.textContent = "Enter a question first.";
    return;
  }

  answerElement.textContent = "Analyzing...";

  try {
    const response = await fetch(`${API}/cia/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        question,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed.");
    }

    answerElement.textContent =
      typeof data.answer === "object"
        ? JSON.stringify(data.answer, null, 2)
        : `Answer: ${data.answer}`;

    if (data.chart && data.chart.chartjs) {
      renderChart(data.chart.chartjs);
    }
  } catch (error) {
    answerElement.textContent = `Error: ${error.message}`;
  }
});

function renderChart(chartData) {
  const canvas = document.getElementById("salesChart");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(canvas, {
    type: chartData.type || "bar",
    data: {
      labels: chartData.labels,
      datasets: chartData.datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true },
      },
    },
  });
}

// MindfulPath — Chart.js Helpers

const moodColors = {
  1: '#ef4444',
  2: '#f97316',
  3: '#eab308',
  4: '#22c55e',
  5: '#06b6d4'
};

function renderMoodChart(canvasId, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx || !data || data.length === 0) return;

  const labels = data.map(d => {
    const date = new Date(d.created_at);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  });

  const scores = data.map(d => d.mood_score);
  const pointColors = scores.map(s => moodColors[s] || '#eab308');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Mood Score',
        data: scores,
        borderColor: '#7c3aed',
        backgroundColor: 'rgba(124, 58, 237, 0.1)',
        pointBackgroundColor: pointColors,
        pointBorderColor: pointColors,
        pointRadius: 6,
        pointHoverRadius: 8,
        tension: 0.3,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 1,
          max: 5,
          ticks: {
            stepSize: 1,
            color: '#999',
            callback: function(value) {
              const labels = { 1: 'Very Sad', 2: 'Sad', 3: 'Neutral', 4: 'Happy', 5: 'Very Happy' };
              return labels[value] || value;
            }
          },
          grid: { color: 'rgba(255,255,255,0.05)' }
        },
        x: {
          ticks: { color: '#999' },
          grid: { color: 'rgba(255,255,255,0.05)' }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              const labels = { 1: 'Very Sad', 2: 'Sad', 3: 'Neutral', 4: 'Happy', 5: 'Very Happy' };
              return labels[context.raw] || context.raw;
            }
          }
        }
      }
    }
  });
}

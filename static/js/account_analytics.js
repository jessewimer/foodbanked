// Stats Page Chart.js Visualizations
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        // Parse data from script tags
        const visitsDataElement = document.getElementById('visitsData');
        const ageDataElement = document.getElementById('ageData');
        
        const visitsData = visitsDataElement ? JSON.parse(visitsDataElement.textContent) : null;
        const ageData = ageDataElement ? JSON.parse(ageDataElement.textContent) : null;
        
        // Visits Over Time Line Chart
        const visitsCtx = document.getElementById('visitsChart');
        if (visitsCtx && visitsData) {
            new Chart(visitsCtx, {
                type: 'line',
                data: {
                    labels: visitsData.labels,
                    datasets: [{
                        label: 'Visits',
                        data: visitsData.values,
                        borderColor: '#d97706',
                        backgroundColor: 'rgba(217, 119, 6, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#d97706',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: '#1f2937',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            padding: 12,
                            cornerRadius: 8,
                            displayColors: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0,
                                color: '#6b7280'
                            },
                            grid: {
                                color: '#e5e7eb'
                            }
                        },
                        x: {
                            ticks: {
                                color: '#6b7280'
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });
        }
        
        // Age Distribution Doughnut Chart
        const ageCtx = document.getElementById('ageChart');
        if (ageCtx && ageData) {
            new Chart(ageCtx, {
                type: 'doughnut',
                data: {
                    labels: ageData.labels,
                    datasets: [{
                        data: ageData.values,
                        backgroundColor: [
                            '#d97706',
                            '#fbbf24',
                            '#f59e0b',
                            '#b45309'
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                padding: 15,
                                font: {
                                    size: 12
                                },
                                color: '#1f2937'
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1f2937',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    });
})();
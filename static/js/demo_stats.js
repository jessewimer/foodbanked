// Demo Stats JavaScript with Chart.js
(function() {
    'use strict';
    
    document.addEventListener('DOMContentLoaded', function() {
        
        // Visits Over Time Chart
        const visitsCtx = document.getElementById('visitsChart');
        if (visitsCtx) {
            new Chart(visitsCtx, {
                type: 'line',
                data: {
                    labels: ['Sept.', 'Oct.', 'Nov.', 'Dec.'],
                    datasets: [{
                        label: 'Visits',
                        data: [345, 222, 275, 381],
                        borderColor: '#d97706',
                        backgroundColor: 'rgba(217, 119, 6, 0.1)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: '#d97706',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
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
                            padding: 12,
                            titleFont: {
                                size: 14
                            },
                            bodyFont: {
                                size: 13
                            },
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#e5e7eb',
                                drawBorder: false
                            },
                            ticks: {
                                color: '#6b7280',
                                font: {
                                    size: 12
                                }
                            }
                        },
                        x: {
                            grid: {
                                display: false,
                                drawBorder: false
                            },
                            ticks: {
                                color: '#6b7280',
                                font: {
                                    size: 12
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // Age Distribution Pie Chart
        const ageCtx = document.getElementById('ageChart');
        if (ageCtx) {
            new Chart(ageCtx, {
                type: 'doughnut',
                data: {
                    labels: ['0-17', '18-30', '31-50', '51+'],
                    datasets: [{
                        data: [892, 743, 1124, 882],
                        backgroundColor: [
                            '#fbbf24',
                            '#f59e0b',
                            '#d97706',
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
                                    size: 13
                                },
                                color: '#1f2937',
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1f2937',
                            padding: 12,
                            titleFont: {
                                size: 14
                            },
                            bodyFont: {
                                size: 13
                            },
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return ` ${label}: ${value} people (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // Animate data bars on scroll
        const dataRows = document.querySelectorAll('.data-row');
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target.querySelector('.data-bar');
                    if (bar) {
                        const width = bar.style.width;
                        bar.style.width = '0%';
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 100);
                    }
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        dataRows.forEach(row => {
            observer.observe(row);
        });
        
    });
})();
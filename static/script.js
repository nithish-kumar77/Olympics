// static/scripts.js

let currentIndex = 0;

function showNextImage() {
    const carousel = document.querySelector('.carousel');
    const images = document.querySelectorAll('.carousel img');
    currentIndex = (currentIndex + 1) % images.length;
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Change image every 4 seconds
setInterval(showNextImage, 4000);


function confirmDeletion(country) {
    return confirm(`Are you sure you want to delete the country "${country}"?`);
}


// Function to initialize the Bar Graph for Medal Counts
function initializeMedalsChart(goldCount, silverCount, bronzeCount) {
    const ctx = document.getElementById('medalsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Gold', 'Silver', 'Bronze'],
            datasets: [{
                label: 'Medals Count',
                data: [goldCount, silverCount, bronzeCount],
                backgroundColor: [
                    'rgba(255, 215, 0, 0.8)', // Gold
                    'rgba(192, 192, 192, 0.8)', // Silver
                    'rgba(205, 127, 50, 0.8)'  // Bronze
                ],
                borderColor: [
                    'rgba(255, 215, 0, 1)', // Gold
                    'rgba(192, 192, 192, 1)', // Silver
                    'rgba(205, 127, 50, 1)'  // Bronze
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Medals'
                    }
                }
            }
        }
    });
}


// Function to filter the players table
function setupSearchForPlayersTable() {
    const searchInput = document.getElementById('searchPlayers'); // Input box for search
    const playersTable = document.getElementById('playersTable'); // Table ID for players
    const rows = playersTable.querySelectorAll('tbody tr'); // All table rows in the tbody

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();

        rows.forEach((row) => {
            const cells = Array.from(row.getElementsByTagName('td')); // Get all table cells
            const match = cells.some((cell) => cell.textContent.toLowerCase().includes(filter)); // Match filter text
            row.style.display = match ? '' : 'none'; // Toggle visibility based on match
        });
    });
}

// Call this function to initialize the search functionality
document.addEventListener('DOMContentLoaded', () => {
    setupSearchForPlayersTable();
});


document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchMedals');
    const medalsTable = document.getElementById('medalsTable');
    const rows = medalsTable.querySelectorAll('tbody tr');

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();

        rows.forEach((row) => {
            const cells = Array.from(row.getElementsByTagName('td'));
            const match = cells.some((cell) => cell.textContent.toLowerCase().includes(filter));
            row.style.display = match ? '' : 'none';
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchEvents');
    const eventsTable = document.getElementById('eventsTable');
    const rows = eventsTable.querySelectorAll('tbody tr');

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();

        rows.forEach((row) => {
            const cells = Array.from(row.getElementsByTagName('td'));
            const match = cells.some((cell) => cell.textContent.toLowerCase().includes(filter));
            row.style.display = match ? '' : 'none';
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchMedalists');
    const medalistsTable = document.getElementById('medalistsTable');
    const rows = medalistsTable.querySelectorAll('tbody tr');

    searchInput.addEventListener('input', function () {
        const filter = searchInput.value.toLowerCase();

        rows.forEach((row) => {
            const cells = Array.from(row.getElementsByTagName('td'));
            const match = cells.some((cell) => cell.textContent.toLowerCase().includes(filter));
            row.style.display = match ? '' : 'none';
        });
    });
});

const medalData = JSON.parse(document.getElementById('medalData').textContent);

const ctx = document.getElementById('medalsGraph').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: medalData.map(item => item.country), // Extract country names
        datasets: [
            {
                label: 'Gold Medals',
                data: medalData.map(item => item.gold), // Extract gold counts
                backgroundColor: 'gold',
            },
            {
                label: 'Silver Medals',
                data: medalData.map(item => item.silver),
                backgroundColor: 'silver',
            },
            {
                label: 'Bronze Medals',
                data: medalData.map(item => item.bronze),
                backgroundColor: 'bronze',
            },
        ],
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
        },
    },
});





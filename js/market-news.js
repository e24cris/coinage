// Market News Fetching Script
document.addEventListener('DOMContentLoaded', async () => {
    const newsContainer = document.getElementById('news-container');
    const API_KEY = 'YOUR_FINNHUB_API_KEY'; // Replace with actual API key

    try {
        const response = await fetch(`https://finnhub.io/api/v1/news?category=general&token=${API_KEY}`);
        const newsData = await response.json();

        // Display top 3 news articles
        newsData.slice(0, 3).forEach(article => {
            const newsCard = document.createElement('div');
            newsCard.classList.add('bg-blue-900', 'p-6', 'rounded-lg', 'shadow-lg');
            newsCard.innerHTML = `
                <img src="${article.image}" alt="${article.headline}" class="w-full h-48 object-cover rounded-t-lg mb-4">
                <h3 class="text-xl font-semibold mb-2">${article.headline}</h3>
                <p class="text-sm mb-4">${article.summary.substring(0, 150)}...</p>
                <a href="${article.url}" target="_blank" class="text-blue-300 hover:underline">
                    Read More
                </a>
            `;
            newsContainer.appendChild(newsCard);
        });
    } catch (error) {
        console.error('Error fetching market news:', error);
        newsContainer.innerHTML = `
            <div class="col-span-full text-center">
                <p>Unable to fetch market news at the moment. Please try again later.</p>
            </div>
        `;
    }
});

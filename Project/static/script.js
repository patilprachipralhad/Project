document.getElementById('summarizeButton').addEventListener('click', function() {
    const articleText = document.getElementById('articleText').value;
    const articleUrl = document.getElementById('articleUrl').value;

    fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            article_text: articleText,
            article_url: articleUrl
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            const modal = document.getElementById('summaryModal');
            const summaryText = document.getElementById('summaryText');
            summaryText.innerText = data.summary;
            modal.style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
});

document.querySelector('.close-button').addEventListener('click', function() {
    const modal = document.getElementById('summaryModal');
    modal.style.display = 'none';
});

window.onclick = function(event) {
    const modal = document.getElementById('summaryModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

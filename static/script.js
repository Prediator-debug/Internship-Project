document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const messageInput = document.getElementById('messageInput');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.getElementById('btnLoader');
    const resultContainer = document.getElementById('resultContainer');
    const resultOutput = document.getElementById('resultOutput');

    analyzeBtn.addEventListener('click', async () => {
        const text = messageInput.value.trim();
        
        if (!text) {
            // Little shake animation for empty input
            messageInput.style.transform = 'translateX(-5px)';
            setTimeout(() => messageInput.style.transform = 'translateX(5px)', 50);
            setTimeout(() => messageInput.style.transform = 'translateX(0)', 100);
            return;
        }

        // UI Loading state
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
        resultContainer.classList.add('hidden');
        resultOutput.className = 'result-output';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
            } else if (data.prediction) {
                resultOutput.textContent = data.prediction;
                if (data.prediction === 'Spam') {
                    resultOutput.classList.add('spam');
                } else {
                    resultOutput.classList.add('ham');
                }
                resultContainer.classList.remove('hidden');
            }
        } catch (error) {
            alert('Got an error contacting the server. Is it running?');
            console.error(error);
        } finally {
            // Restore UI
            analyzeBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    });

    clearBtn.addEventListener('click', () => {
        messageInput.value = '';
        resultContainer.classList.add('hidden');
        messageInput.focus();
    });
});

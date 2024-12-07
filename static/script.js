/* static/script.js */

document.getElementById('submitBtn').addEventListener('click', () => {
    const emailContent = document.getElementById('emailContent').value.trim();
    const resultDiv = document.getElementById('result');

    // Clear previous results
    resultDiv.style.display = 'none';
    resultDiv.className = 'mt-4 p-3 rounded text-center';

    if (!emailContent) {
        resultDiv.style.display = 'block';
        resultDiv.classList.add('error');
        resultDiv.innerText = 'Please enter the email content.';
        return;
    }

    // Show a loading spinner
    resultDiv.style.display = 'block';
    resultDiv.classList.add('bg-light');
    resultDiv.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Analyzing your email...</p>
    `;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: emailContent })
    })
    .then(response => response.json())
    .then(data => {
        // Clear loading spinner
        resultDiv.innerHTML = '';

        if (data.error) {
            resultDiv.classList.add('error');
            resultDiv.innerText = data.error;
        } else {
            const phishing = (data.phishing_likelihood * 100).toFixed(2);
            const legitimate = (data.legitimate_likelihood * 100).toFixed(2);
            
            if (phishing > legitimate) {
                resultDiv.classList.add('phishing');
                resultDiv.innerHTML = `
                    <h4 class="mb-3">Phishing Detected!</h4>
                    <p><strong>Phishing Likelihood:</strong> ${phishing}%</p>
                    <p><strong>Legitimate Likelihood:</strong> ${legitimate}%</p>
                `;
            } else {
                resultDiv.classList.add('legitimate');
                resultDiv.innerHTML = `
                    <h4 class="mb-3">Legitimate Email!</h4>
                    <p><strong>Legitimate Likelihood:</strong> ${legitimate}%</p>
                    <p><strong>Phishing Likelihood:</strong> ${phishing}%</p>
                `;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.classList.add('error');
        resultDiv.innerText = 'An error occurred while processing your request.';
    });
});

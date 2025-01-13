document.getElementById('howto-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const question = document.getElementById('question-input').value.trim();
    if (!question) {
        alert("Please enter a 'how-to' question.");
        return;
    }

    // Show loading message while processing
    document.getElementById('answer').textContent = "Processing your request...";
    document.getElementById('documentation-link').textContent = "";

    // Send the question to the backend (app.py)
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('answer').textContent = "Error: " + data.error;
        } else {
            document.getElementById('answer').textContent = data.response;
            if (data.documentation) {
                document.getElementById('documentation-link').innerHTML = `
                    <strong>Relevant Documentation:</strong> 
                    <a href="${data.documentation}" target="_blank">${data.documentation}</a>`;
            } else {
                document.getElementById('documentation-link').textContent = "No relevant documentation found.";
            }
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById('answer').textContent = "An error occurred while processing your request.";
    });
});

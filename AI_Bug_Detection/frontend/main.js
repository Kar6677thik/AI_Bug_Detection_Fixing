document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('codeInput');
    const analyzeButton = document.getElementById('analyzeButton');
    const resultsDiv = document.getElementById('results');
    
    analyzeButton.addEventListener('click', async function() {
        const code = codeInput.value.trim();
        if (!code) {
            alert('Please enter some code to analyze');
            return;
        }
        
        analyzeButton.disabled = true;
        analyzeButton.textContent = 'Analyzing...';
        resultsDiv.innerHTML = '<div class="loading">Analyzing your code...</div>';
        
        try {
            // Changed from https://localhost:5000/analyze to http://127.0.0.1:8000/analyze
            // Your FastAPI server is running on 8000, not 5000, and doesn't use HTTPS
            const response = await fetch('https://e0ee-35-227-72-66.ngrok-free.app/full-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    language: 'python' // Default to Python for now
                })
            });
            
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        } finally {
            analyzeButton.disabled = false;
            analyzeButton.textContent = 'Analyze Code';
        }
    });
    
    function displayResults(data) {
        if (!data.success) {
            resultsDiv.innerHTML = `<div class="error">${data.error || 'Unknown error occurred'}</div>`;
            return;
        }
        
        let html = '';
        const results = data.results;
        
        if (results.bug_report.bugs && results.bug_report.bugs.length > 0) {
            html += '<h2>Detected Bugs</h2>';
            results.bug_report.bugs.forEach(bug => {
                html += `
                    <div class="bug-card">
                        <h3>${bug.description || 'Unknown bug'}</h3>
                        <p>Line ${bug.line || 'unknown'}</p>
                    </div>
                `;
            });
        } else {
            html += '<h2>No bugs detected!</h2>';
            // Show the analysis anyway
            if (results.bug_report.analysis) {
                html += `<div class="analysis-card">
                    <h3>Analysis</h3>
                    <pre>${results.bug_report.analysis}</pre>
                </div>`;
            }
        }
        
        if (results.fixes && results.fixes.length > 0) {
            html += '<h2>Suggested Fixes</h2>';
            results.fixes.forEach(fix => {
                html += `
                    <div class="fix-card">
                        <h3>${fix.bug.description || 'Bug'}</h3>
                        <pre><code>${fix.fix || 'No fix suggested'}</code></pre>
                        <p>Confidence: ${(fix.confidence * 100).toFixed(1)}%</p>
                    </div>
                `;
            });
        }
        
        resultsDiv.innerHTML = html;
    }
});
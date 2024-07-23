document.getElementById('predict-btn').addEventListener('click', () => {
    const operationTime = document.getElementById('operation-time').value;
    const location = document.getElementById('location').value;
    const company = document.getElementById('company').value;
    const engine = document.getElementById('engine').value;
    const milage = document.getElementById('milage').value;

    fetch('http://127.0.0.1:5000/predict-maintenance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            operation_time: operationTime,
            location: location,
            company: company,
            engine: engine,
            milage: milage
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction-result').innerText = `Maintenance Needed: ${data.maintenance_needed}`;
    })
    .catch(error => console.error('Error:', error));
});

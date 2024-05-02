function uploadAudio() {
    const formData = new FormData(document.getElementById('uploadForm'));
    document.getElementById('loader').style.display = 'block'; // Show the spinner

    fetch('/transcribe', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server responded with status ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('transcription').innerText = data.transcription;
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        document.getElementById('loader').style.display = 'none'; // Hide the spinner
    });
}

//cfb_assistant.js
function showLoading() {
    // Show the loading div manually when the form is submitted
    document.getElementById('loading').style.display = 'block';
    document.getElementById('response').style.display = 'none';
}

document.getElementById('response').addEventListener('htmx:afterSwap', function () {
    // Hide the loading div when the response is displayed
    document.getElementById('loading').style.display = 'none';
    document.getElementById('response').style.display = 'block';
});

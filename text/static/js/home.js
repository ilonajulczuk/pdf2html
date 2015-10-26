function getCookie(sKey) {
    if (!sKey) { return null; }
    return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
}

var form = document.getElementById('file-form');
var fileSelect = document.getElementById('file-select');
var titleText = document.getElementById('doc-title')
var uploadButton = document.getElementById('upload-button');

form.onsubmit = function(event) {
    event.preventDefault();

    // Get the selected files from the input.
    var files = fileSelect.files;
    // Create a new FormData object.
    if (files[0] == undefined) {
        alert("Choose a file!")
        return
    }
    uploadButton.innerHTML = 'Uploading...';

    var formData = new FormData();
    // Add the file to the request.
    formData.append('file', files[0]);
    // Add the file to the request.
    formData.append('title', titleText.value);

    // Set up the request.
    var xhr = new XMLHttpRequest();
    // Open the connection.
    xhr.open('POST', '/api/documents/', true);
    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    // Set up a handler for when the request finishes.
    xhr.onload = function () {
        if (xhr.status === 201) {
            uploadButton.innerHTML = 'Upload';
            alert("Succes!");
        } else {
            alert('An error occurred!');
        }
    };
    // Send the Data.
    xhr.send(formData);
}

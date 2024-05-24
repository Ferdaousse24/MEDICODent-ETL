document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const uploadButton = document.getElementById('uploadButton');
    const progressBar = document.querySelector('.progress-bar');
    const uploadStatus = document.getElementById('uploadStatus');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        const xhr = new XMLHttpRequest();

        xhr.open('POST', '/upload', true);

        xhr.upload.onprogress = function (e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete.toFixed(2) + '%';
                progressBar.innerHTML = percentComplete.toFixed(2) + '%';
            }
        };

        xhr.onload = function () {
            if (xhr.status === 200) {
                uploadStatus.innerHTML = '<p class="text-success">Fichier téléchargé avec succès!</p>';
            } else {
                uploadStatus.innerHTML = '<p class="text-danger">Erreur de téléchargement du fichier.</p>';
            }
        };

        xhr.onerror = function () {
            uploadStatus.innerHTML = '<p class="text-danger">Erreur de téléchargement du fichier.</p>';
        };

        xhr.send(formData);
    });
});

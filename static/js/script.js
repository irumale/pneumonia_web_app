// script.js

function handleImage() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  const errorText = document.getElementById('error');

  if (!file) {
    errorText.innerText = "Please select an image file.";
    return;
  }

  const img = new Image();
  const objectUrl = URL.createObjectURL(file);

  img.onload = function () {
    if (img.width > 512 || img.height > 512) {
      errorText.innerText = "Image must not exceed 512x512 pixels.";
      return;
    }

    sessionStorage.setItem('uploadedImage', objectUrl);
    window.location.href = 'preview.html';
  };
  img.src = objectUrl;
}

window.onload = function () {
  const previewImg = document.getElementById('previewImg');
  const resultImg = document.getElementById('resultImg');
  const resultText = document.getElementById('resultText');
  const uploadedImage = sessionStorage.getItem('uploadedImage');

  if (previewImg) previewImg.src = uploadedImage;
  if (resultImg) resultImg.src = uploadedImage;
  if (resultText) resultText.innerText = sessionStorage.getItem('prediction');
};

function goHome() {
  sessionStorage.clear();
  window.location.href = 'index.html';
}

function predict() {
  const imageData = sessionStorage.getItem('uploadedImage');

  // For now, simulate a random prediction
  const prediction = Math.random() > 0.5 ? "Pneumonia Detected" : "Normal";

  sessionStorage.setItem('prediction', prediction);
  window.location.href = 'result.html';
}

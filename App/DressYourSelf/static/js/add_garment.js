const caret = document.querySelector('.caret');
const select = document.querySelector('#category');

select.addEventListener('mousedown', () => {
    caret.classList.toggle('caret-rotate');
});

document.addEventListener("click", function (event) {
    if (!select.contains(event.target) || event.target === caret) {
      caret.classList.remove('caret-rotate');
    }
});

document.addEventListener("DOMContentLoaded", function () {    
    // Prevent form submission if the default option is selected
    document.querySelector("form").addEventListener("submit", function (e) {
      if (selectElement.value === "") {
        e.preventDefault();
        alert("Please select an option.");
      }
    });
});

const imageInput = document.querySelector('#image');
const imagePreview = document.querySelector('#imagePreview')

imageInput.addEventListener('change', () => {
    const image = imageInput.files[0];
    imagePreview.src = URL.createObjectURL(image);
});
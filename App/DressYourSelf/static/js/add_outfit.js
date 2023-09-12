const imageInput = document.querySelector('#image');
const imagePreview = document.querySelector('#imagePreview')

imageInput.addEventListener('change', () => {
    const image = imageInput.files[0];
    imagePreview.src = URL.createObjectURL(image);
});
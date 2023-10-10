const imageInput = document.querySelector('#image');
const imagePreview = document.querySelector('#imagePreview')

imageInput.addEventListener('change', () => {
    const image = imageInput.files[0];
    imagePreview.src = URL.createObjectURL(image);
});

function hideModals(modals) {
    modals.forEach(modal => {
        modal.classList.add('inactive');
    });
}

const modals = document.querySelectorAll('.modal');
const modalButtons = document.querySelectorAll('[data-modal-button]');
modalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.garments-container').querySelector('.modal');
        modal.showModal();
        hideModals(modals);
        modal.classList.remove('inactive');
    });
});
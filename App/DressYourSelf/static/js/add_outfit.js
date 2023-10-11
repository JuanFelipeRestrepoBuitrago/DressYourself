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

function closeModal(modal) {
    modal.classList.add('inactive');
    modal.close();
}

function deleteGarment(garment, input, deleteModalGarmentButton, modalGarment, chosenGarments) {
    modalGarment.classList.remove('chosen');
    deleteModalGarmentButton.classList.add('inactive');
    input.value = input.value.replace(garment.dataset.garmentId, '');
    input.value = input.value.replace(',,', ',');
    if (input.value[0] === ',') {
        input.value = input.value.substring(1);
    } else if (input.value[input.value.length - 1] === ',') {
        input.value = input.value.substring(0, input.value.length - 1);
    }
    chosenGarments.removeChild(garment);
}

function deleteGarmentEvent(button) {
    const garment = button.closest('.garment');
    const chosenGarments = garment.closest('.chosen-garments');
    const garmentsContainer = chosenGarments.closest('.garments-container');
    const input = garmentsContainer.previousElementSibling;
    const modalGarment = garmentsContainer.querySelector(`.modal .garment[data-garment-id="${garment.dataset.garmentId}"]`);
    const deleteModalGarmentButton = modalGarment.querySelector('.btn-close');

    deleteGarment(garment, input, deleteModalGarmentButton, modalGarment, chosenGarments);
}

const modals = document.querySelectorAll('.modal');
const modalButtons = document.querySelectorAll('[data-modal-button]');
const closeButtons = document.querySelectorAll('[data-modal-close]');
const modalGarments = document.querySelectorAll('dialog .garments .garment');
const deleteChosenGarmentButtons = document.querySelectorAll('.chosen-garments .garment .btn-close');
const deleteFromModalButtons = document.querySelectorAll('.modal .garment .btn-close');

modalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.garments-container').querySelector('.modal');
        modal.showModal();
        hideModals(modals);
        modal.classList.remove('inactive');
    });
});

closeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal');
        closeModal(modal);
    });
});


modalGarments.forEach(garment => {
    garment.addEventListener('click', (event) => {
        const modal = garment.closest('.modal');
        const garmentsContainer = modal.closest('.garments-container');
        const chosenGarments = garmentsContainer.querySelector('.chosen-garments');
        const input = garmentsContainer.previousElementSibling;
        const deleteGarmentButton = garment.querySelector('.btn-close');

        if (!garment.classList.contains('chosen') && event.target !== deleteGarmentButton && !deleteGarmentButton.contains(event.target)) {
            deleteGarmentButton.classList.remove('inactive');
            garment.classList.add('chosen');
            if (input.value === '') {
                input.value = garment.dataset.garmentId;
            } else {
                input.value += ',' + garment.dataset.garmentId;
            }
            const chosenGarment = garment.cloneNode(true);
            chosenGarments.appendChild(chosenGarment);
            closeModal(modal);

            const deleteChosenGarmentButton = chosenGarment.querySelector('.btn-close');
            deleteChosenGarmentButton.addEventListener('click', () => {
                deleteGarmentEvent(deleteChosenGarmentButton);
            });
        }
    });
});

deleteChosenGarmentButtons.forEach(button => {
    button.addEventListener('click', () => {
        deleteGarmentEvent(button);
    });
});

deleteFromModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modalGarment = button.closest('.garment');
        const modal = modalGarment.closest('.modal');
        const garmentsContainer = modal.closest('.garments-container');
        const chosenGarments = garmentsContainer.querySelector('.chosen-garments');
        const input = garmentsContainer.previousElementSibling;
        const garment = garmentsContainer.querySelector(`.chosen-garments .garment[data-garment-id="${modalGarment.dataset.garmentId}"]`);
        const deleteModalGarmentButton = modalGarment.querySelector('.btn-close');

        deleteGarment(garment, input, deleteModalGarmentButton, modalGarment, chosenGarments);
        closeModal(modal)
    });
});
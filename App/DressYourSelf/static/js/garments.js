const detailsContainer = document.querySelector('.garment-detail');
const closeDetails = document.querySelector('.garment-detail .close-garment-detail');
const garmentsDetail = document.querySelectorAll('.garment-detail [data-garment-id]');
const garments = document.querySelectorAll('.garment-card');

function closeDetailsContainer() {
    detailsContainer.classList.add('inactive');
}

function checkEventTarget(event, targets) {
    for (let i = 0; i < targets.length; i++) {
        if (targets[i] === event.target || targets[i].contains(event.target)) {
            return true;
        }
    }
    return false;
}

garments.forEach(garment => {
    garment.addEventListener('click', () => {
        const garmentId = garment.querySelector('.garment-info [data-garment-id]').getAttribute('data-garment-id');
        detailsContainer.classList.remove('inactive');
        garmentsDetail.forEach(garmentDetail => {
            if (garmentDetail.getAttribute('data-garment-id') === garmentId) {
                garmentDetail.classList.remove('inactive');
            } else {
                garmentDetail.classList.add('inactive');
            }
        });
    });
});

document.addEventListener('click', (event) => {
    if (!checkEventTarget(event, garments) && detailsContainer !== event.target && !detailsContainer.contains(event.target)) {
        closeDetailsContainer();
    }
});

closeDetails.addEventListener('click', closeDetailsContainer);
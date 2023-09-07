const detailsContainer = document.querySelector('.garment-detail');
const closeDetails = document.querySelector('.garment-detail .close-garment-detail');
const garmentsDetail = document.querySelectorAll('.garment-detail [data-garment-id]');
const garments = document.querySelectorAll('.garment-card');
const searchInput = document.querySelector('#search');

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

searchInput.addEventListener('input', (event) => {
    const searchValue = searchInput.value.toLowerCase();
    console.log(searchValue);
    garments.forEach(garment => {
        const garmentName = garment.querySelector('.garment-info [data-garment-name]').getAttribute('data-garment-name').toLowerCase();
        const garmentCategory = garment.querySelector('.garment-info [data-garment-category]').getAttribute('data-garment-category').toLowerCase();
        const garmentDescription = garment.querySelector('.garment-info [data-garment-description]').getAttribute('data-garment-description').toLowerCase();
        const garmentBrand = garment.querySelector('.garment-info [data-garment-brand]').getAttribute('data-garment-brand').toLowerCase();
        const garmentColor = garment.querySelector('.garment-info [data-garment-color]').getAttribute('data-garment-color').toLowerCase();
        const garmentSize = garment.querySelector('.garment-info [data-garment-size]').getAttribute('data-garment-size').toLowerCase();
        console.log(garmentName, garmentCategory, garmentDescription, garmentBrand, garmentColor, garmentSize);

        if (garmentName.includes(searchValue) || garmentCategory.includes(searchValue) || garmentDescription.includes(searchValue) || garmentBrand.includes(searchValue) || garmentColor.includes(searchValue) || garmentSize.includes(searchValue)) {
            console.log('includes');
            garment.classList.remove('inactive');
        } else {
            console.log('not includes');
            garment.classList.add('inactive');
        }
    });
});
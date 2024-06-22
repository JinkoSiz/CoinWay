const accountTab = document.querySelectorAll('.account-btn'),
    accountItem = document.querySelectorAll('.account-item');

accountTab.forEach(item => {
    item.addEventListener('click', (e) => {

        targetItem = item.dataset.id;

        accountItem.forEach(item => {
            item.classList.add('hide');
            if (item.classList.contains(targetItem)) {
                item.classList.remove('hide')
            }
        })

    })
})
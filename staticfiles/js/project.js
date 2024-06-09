'use strict';

document.addEventListener('DOMContentLoaded', () => {

    //POPUP

    const openPopupBtn = document.querySelector('#popupBtn'),
        closePopupBtn = document.querySelector('.filter-popup-close'),
        acceptPopupBtn = document.querySelector('.filter-popup-accept'),
        bgPopup = document.querySelector('.filter-popup-bg'),
        popupFilterList = document.querySelector('.filter-popup-value-block'),
        popupFilterItem = document.querySelectorAll('.filter-popup-value-item'),
        resetBtn = document.querySelector('.filter-popup-reset'),
        searcPanel = document.querySelector('.filter-popup-input'),
        searchForPush = document.querySelector('.filter-popup-input-secret'),
        popup = document.querySelector('.filter-popup'),
        archiveBtn = document.querySelector('.archive-btn');

    var pushValues = [];

    const savedValues = JSON.parse(localStorage.getItem('pushValues')) || [];
    pushValues = savedValues;
    popupFilterItem.forEach(item => {
        if (savedValues.includes(item.dataset.net)) {
            item.classList.add('active');
        }
    });

    if (searchForPush != null) {
        searchForPush.value = pushValues.join(' ');
    }

    if(openPopupBtn != null) {
        openPopupBtn.addEventListener('click', (e) => {
            e.preventDefault();
            popup.classList.add('active');
            bgPopup.classList.add('active');
        })
    }

    if(resetBtn != null) {
        resetBtn.addEventListener('click', (e) => {
            popupFilterItem.forEach(item => {
                item.classList.remove('active');
            })
            pushValues = [];
            localStorage.removeItem('pushValues');
        })
    }

    document.addEventListener('click', (e) => {
        e.preventDefault;
        if ((e.target === closePopupBtn || e.target === acceptPopupBtn || e.target === bgPopup) && popup.classList.contains('active')) {
            popup.classList.remove('active');
            bgPopup.classList.remove('active');
        }

    });

    popupFilterItem.forEach(item => {
        if (item != null) {
            item.addEventListener('click', () => {
                item.classList.toggle('active');
                if (item.classList.contains('active')) {
                    pushValues.push(item.dataset.net);
                } else {
                    for (let i = 0, len = pushValues.length; i < len; i++) {
                        if (pushValues[i] === item.dataset.net) {
                            pushValues.splice(i, 1);
                            break;
                        }
                    }
                }
                searchForPush.value = pushValues.join(' ');
                console.log(searchForPush.value);
            })
        }
    })

    if (acceptPopupBtn != null) {
        acceptPopupBtn.addEventListener('click', (e) => {
            localStorage.setItem('pushValues', JSON.stringify(pushValues));
        });
    }

    HTMLElement.prototype.getNodesByText = function (text) {
        const expr = `.//*[text()[contains(
        translate(.,
          'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
          'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        ),
        '${text.toLowerCase()}'
        )]]`;    /**/
        const nodeSet = document.evaluate(expr, this, null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
            null);
        return Array.from({ length: nodeSet.snapshotLength },
            (v, i) => nodeSet.snapshotItem(i)
        );
    };

    if (searcPanel != null) {
        searcPanel.addEventListener('input', e => {
            popupFilterItem.forEach(item => {
                item.classList.remove('search-result')
            });
            const searchStr = popupFilterList.dataset.search = e.target.value.trim();
            if (!searchStr.length) return;
            for (const el of popupFilterList.getNodesByText(searchStr)) {
                const card = el.closest('.filter-popup-value-item');
                if (card) card.classList.add('search-result');
            }
        });
    }

    //TABS

    const slider = document.querySelector('.slider-tabs-block-visible'),
        slides = Array.from(document.querySelectorAll('.slider-tabs-item')),
        contentItem = document.querySelectorAll('.projects-list-wrapper');

    let isDragging = false,
        startPos = 0,
        currentTranslate = 0,
        prevTranslate = 0,
        animationID = 0,
        currentIndex = 0,
        sliderWidth = slider.offsetWidth,
        maxTranslate = sliderWidth / 3,
        minTranslate = -sliderWidth / 3;

    slider.addEventListener('touchstart', touchStart(0));
    slider.addEventListener('touchend', touchEnd);
    slider.addEventListener('touchmove', touchMove);
    //
    slider.addEventListener('mousedown', touchStart(0));
    slider.addEventListener('mouseup', touchEnd);
    slider.addEventListener('mouseleave', touchEnd);
    slider.addEventListener('mousemove', touchMove);

    slides.forEach((slide, index) => {

        slide.addEventListener('dragstart', (e) => e.preventDefault());
        slide.addEventListener('touchstart', touchStart(index));
        slide.addEventListener('touchend', touchEnd);
        slide.addEventListener('touchmove', touchMove);
        slide.addEventListener('mousedown', touchStart(index));
        slide.addEventListener('mouseup', touchEnd);
        slide.addEventListener('mouseleave', touchEnd);
        slide.addEventListener('mousemove', touchMove);

        slide.addEventListener('click', (e) => {
            if(!isDragging) {
                removeClass(slides);

                slide.classList.add('active');

                let itemClass = e.target.dataset.tab;

                if (itemClass === 'all') {
                    contentItem.forEach(item  => {
                        item.classList.remove('hide');
                        hideArchive();
                    });
                } else {
                    contentItem.forEach(item  => {
                        item.classList.remove('hide')
                        if(!item.classList.contains(itemClass)) {
                            item.classList.add('hide');
                        }
                        hideArchive();
                    });
                }
            }
        });
    })

    window.oncontextmenu = function (event) {
        event.preventDefault();
        event.stopPropagation();
        return false;
    }

    function removeClass(selector) {
        selector.forEach(item => item.classList.remove('active'));
    }

    function touchStart(index) {
        return function (event) {
            maxTranslate = sliderWidth / 3;
            minTranslate = -sliderWidth / 3;
            currentIndex = index;
            startPos = getPositionX(event);
            isDragging = true;
            animationID = requestAnimationFrame(animation);
            slider.classList.add('grabbing');
        }
    }

    function touchEnd() {

        isDragging = false;
        cancelAnimationFrame(animationID);
        setPositionByIndex();
        slider.classList.remove('grabbing');
    }

    function touchMove(event) {
        if (isDragging) {
            const currentPosition = getPositionX(event);
            currentTranslate = prevTranslate + currentPosition - startPos;
            if (currentTranslate < minTranslate) {
                currentTranslate = minTranslate + (currentTranslate - minTranslate) / 3;
            } else if (currentTranslate > maxTranslate) {
                currentTranslate = maxTranslate + (currentTranslate - maxTranslate) / 3;
            }
            setSliderPosition();
        }
    }

    function getPositionX(event) {
        return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
    }

    function animation() {
        setSliderPosition();
        if (isDragging) requestAnimationFrame(animation);
    }

    function setSliderPosition() {
        slider.style.transform = `translateX(${currentTranslate}px)`;
    }

    function setPositionByIndex() {

        if (currentTranslate < minTranslate) {
            currentTranslate = minTranslate;
        } else if (currentTranslate > maxTranslate) {
            currentTranslate = maxTranslate;
        }

        prevTranslate = currentTranslate;
        setSliderPosition();
    }

//Archive BTN

    if(archiveBtn !== null) {
        archiveBtn.addEventListener('click', (e) => {
            archiveBtn.classList.toggle('active')
            contentItem.forEach(item => {
                if(archiveBtn.classList.contains('active')) {
                    item.classList.add('hide');
                    if (item.classList.contains('hide') && item.classList.contains('Archive')) {
                        item.classList.remove('hide');
                    }
                } else {
                    item.classList.remove('hide');
                    if (item.classList.contains('Archive')) {
                        item.classList.add('hide');
                    }
                }

            })
        })
    }

    function hideArchive() {
        contentItem.forEach(item => {
            if (item.classList.contains('Archive')) {
                item.classList.add('hide');
            }
        })
    }
    hideArchive();

})
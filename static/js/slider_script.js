document.addEventListener('DOMContentLoaded', function () {
    var swiper1 = new Swiper('.swiper-container', {
        slidesPerView: 'auto',
        spaceBetween: 10,
        loop: true, // Enable looping
        navigation: {
            nextEl: '.swiper-container .swiper-button-next',
            prevEl: '.swiper-container .swiper-button-prev',
        },
        breakpoints: {
            // when window width is <= 640px
            640: {
                slidesPerView: 2,
            },
            // when window width is <= 768px
            768: {
                slidesPerView: 4,
            },
            // when window width is <= 1024px
            1024: {
                slidesPerView: 5,
            },
        },
    });


    var swiper2 = new Swiper('.swiper-container-2', {
        slidesPerView: 'auto',
        spaceBetween: 10,
        loop: true,
        navigation: {
            nextEl: '.swiper-container-2 .swiper-button-next',
            prevEl: '.swiper-container-2 .swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 3,
            },
            768: {
                slidesPerView: 4,
            },
            1024: {
                slidesPerView: 4,
            },
        },
        // pagination: {
        //     el: '.swiper-container-2 .swiper-pagination',
        //     clickable: true,
        // },
    });
});
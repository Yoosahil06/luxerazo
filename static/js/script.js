document.addEventListener('DOMContentLoaded', function () {
  const swiper = new Swiper('.hero-swiper', {
    loop: true,
    autoplay: {
      delay: 3500,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    }
  });
});

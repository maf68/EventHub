document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star-rating label');
  
    stars.forEach((star, index) => {
      star.addEventListener('click', function() {
        for (let i = 0; i < stars.length; i++) {
          if (i <= index) {
            stars[i].classList.add('checked');
          } else {
            stars[i].classList.remove('checked');
          }
        }
  
        const input = star.parentNode.querySelector('input');
        input.value = index + 1;
      });
    });
  });
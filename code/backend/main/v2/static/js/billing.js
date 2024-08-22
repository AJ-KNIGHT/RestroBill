    
    // Minus button click event listener
    document.querySelectorAll('.number-input .minus').forEach(button => {
        button.addEventListener('click', function () {
          this.closest('.number-input').querySelector('input').stepDown();
        });
      });
  
      // Plus button click event listener  
      document.querySelectorAll('.number-input .plus').forEach(button => {
        button.addEventListener('click', function () {
          this.closest('.number-input').querySelector('input').stepUp();
        });
      });
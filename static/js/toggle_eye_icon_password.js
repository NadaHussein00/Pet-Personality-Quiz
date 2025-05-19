// Toggles password visibility and icon color when clicking on toggle elements

document.addEventListener('DOMContentLoaded', () => {
    const toggles = document.querySelectorAll('.toggle-password'); 
    toggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        const targetId = toggle.getAttribute('data-target');  
        const input = document.getElementById(targetId);       
        if (input) {
          if (input.type === 'password') {
            input.type = 'text';
            toggle.style.color = '#000';
          } else {
            input.type = 'password';
            toggle.style.color = '#666';
          }
        }
      });
    });
  });
  

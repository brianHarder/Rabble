function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Select2 for member selection
  if ($('#id_members').length) {
    $('#id_members').select2({
      theme: 'bootstrap-5',
      width: '100%',
      placeholder: 'Search and select members...',
      allowClear: true
    });
  }

  const btn = document.getElementById('like-btn');
  if (!btn) return;
  
  const url = btn.dataset.likeUrl;
  const username = btn.dataset.username;
  const csrftoken = getCookie('csrftoken');
  const countSpan = document.getElementById('like-count');

  if (btn.dataset.liked === 'True') {
    btn.classList.add('liked');
  }

  btn.addEventListener('click', async () => {
    if (!username) return alert('Log in to like posts');

    try {
      const res = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ user: username }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      countSpan.textContent = data.like_count;

      btn.classList.toggle('liked', data.liked);
      btn.dataset.liked = data.liked ? 'True' : 'False';

    } catch (err) {
      console.error('Error toggling like:', err);
      alert('Sorry, could not toggle like.');
    }
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const commentLikeBtns = document.querySelectorAll('.comment-like-btn');
  const csrftoken = getCookie('csrftoken');

  commentLikeBtns.forEach(btn => {
      if (btn.dataset.liked === 'True') {
          btn.classList.add('liked');
      }

      btn.addEventListener('click', async () => {
          const username = btn.dataset.username;
          if (!username) return alert('Log in to like comments');

          try {
              const res = await fetch(btn.dataset.likeUrl, {
                  method: 'POST',
                  credentials: 'same-origin',
                  headers: {
                      'Content-Type': 'application/json',
                      'X-CSRFToken': csrftoken,
                  },
                  body: JSON.stringify({ user: username }),
              });
              if (!res.ok) throw new Error(`HTTP ${res.status}`);
              const data = await res.json();

              const countSpan = btn.querySelector('.comment-like-count');
              countSpan.textContent = data.like_count;

              btn.classList.toggle('liked', data.liked);
              btn.dataset.liked = data.liked ? 'True' : 'False';

          } catch (err) {
              console.error('Error toggling like:', err);
              alert('Sorry, could not toggle like.');
          }
      });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  // Handle private checkbox and members list for both rabble and subrabble forms
  var priv = document.getElementById("id_private");
  var members = document.getElementById("members-field");
  if (!priv || !members) return;

  function toggle() {
    members.style.display = priv.checked ? "block" : "none";
    if (priv.checked) {
      // Find the current user's option and make it selected
      var currentUserId = document.querySelector('meta[name="user-id"]').content;
      var userOption = $(`#id_members option[value="${currentUserId}"]`);
      if (userOption.length) {
        userOption.prop('selected', true);
        // Trigger Select2 to update
        $('#id_members').trigger('change');
      }
    }
  }
  priv.addEventListener("change", toggle);
  toggle();
});

// Password visibility toggle functionality
function initializePasswordToggles() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        const toggleButton = document.createElement('button');
        toggleButton.className = 'btn btn-outline-secondary';
        toggleButton.type = 'button';
        toggleButton.innerHTML = '<i class="bi bi-eye"></i>';
        wrapper.appendChild(toggleButton);
        
        toggleButton.addEventListener('click', function() {
            const type = field.getAttribute('type') === 'password' ? 'text' : 'password';
            field.setAttribute('type', type);
            this.innerHTML = type === 'password' ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
        });
    });
}

// Initialize password toggles when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializePasswordToggles();
});


document.addEventListener('DOMContentLoaded', function() {
  // Initialize the carousel
  var carouselElement = document.getElementById('subrabblesCarousel');
  if (!carouselElement) return;

  // Only initialize if there are visible items
  var visibleItems = carouselElement.querySelectorAll('.carousel-item');
  if (visibleItems.length === 0) return;

  var carousel = new bootstrap.Carousel(carouselElement, {
    interval: 5000,
    wrap: true
  });
  
  // Function to update indicators
  function updateIndicators() {
    var indicators = carouselElement.querySelectorAll('.carousel-indicators button');
    var items = carouselElement.querySelectorAll('.carousel-item');
    
    // Remove all existing indicators
    indicators.forEach(indicator => indicator.remove());
    
    // Create new indicators for all items
    items.forEach((item, index) => {
      var button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('data-bs-target', '#subrabblesCarousel');
      button.setAttribute('data-bs-slide-to', index);
      button.setAttribute('aria-label', 'SubRabble ' + (index + 1));
      button.setAttribute('data-bs-slide', index);
      
      if (index === 0) {
        button.classList.add('active');
        button.setAttribute('aria-current', 'true');
      }
      
      carouselElement.querySelector('.carousel-indicators').appendChild(button);
    });
  }

  // Update indicators when slide changes
  carouselElement.addEventListener('slide.bs.carousel', function (e) {
    var indicators = carouselElement.querySelectorAll('.carousel-indicators button');
    indicators.forEach(function(indicator, index) {
      if (index === e.to) {
        indicator.classList.add('active');
        indicator.setAttribute('aria-current', 'true');
      } else {
        indicator.classList.remove('active');
        indicator.removeAttribute('aria-current');
      }
    });
  });

  // Initial update of indicators
  updateIndicators();
});

document.addEventListener('DOMContentLoaded', function() {
  const privateCheckbox = document.querySelector('#id_private');
  const membersField = document.querySelector('#members-field');
  
  function updateMembersField() {
    membersField.style.display = privateCheckbox.checked ? 'block' : 'none';
  }
  
  privateCheckbox.addEventListener('change', updateMembersField);
  updateMembersField();
});
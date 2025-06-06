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

  const btn       = document.getElementById('like-btn');
  if (!btn) return;
  
  const url       = btn.dataset.likeUrl;
  const username  = btn.dataset.username;
  const csrftoken = getCookie('csrftoken');
  const countSpan = document.getElementById('like-count');
  const icon      = btn.querySelector('i');

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

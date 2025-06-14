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
  const btn       = document.getElementById('like-btn');
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
  var priv = document.getElementById("id_private");
  var members = document.getElementById("members-field");
  if (!priv || !members) return;
  function toggle() {
    members.style.display = priv.checked ? "block" : "none";
  }
  priv.addEventListener("change", toggle);
  toggle();
});

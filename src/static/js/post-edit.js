document.addEventListener('DOMContentLoaded', function() {
  const postForm = document.getElementById('post-form');
  if (postForm) {
    postForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const data = {
        title: formData.get('title'),
        body: formData.get('body'),
        anonymous: formData.get('anonymous') === 'on'
      };

      fetch(postForm.dataset.editUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (response.ok) {
          window.location.href = postForm.dataset.successUrl;
        } else {
          response.json().then(data => {
            // Display validation errors
            Object.keys(data).forEach(field => {
              const errorElement = document.querySelector(`#id_${field}`).nextElementSibling;
              if (errorElement) {
                errorElement.textContent = data[field].join(', ');
              }
            });
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  }

  const commentForm = document.getElementById('comment-form');
  if (commentForm) {
    commentForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const data = {
        text: formData.get('text'),
        anonymous: formData.get('anonymous') === 'on'
      };

      fetch(commentForm.dataset.editUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: JSON.stringify(data)
      })
      .then(response => {
        if (response.ok) {
          window.location.href = commentForm.dataset.successUrl;
        } else {
          response.json().then(data => {
            // Display validation errors
            Object.keys(data).forEach(field => {
              const errorElement = document.querySelector(`#id_${field}`).nextElementSibling;
              if (errorElement) {
                errorElement.textContent = data[field].join(', ');
              }
            });
          });
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
  }
});
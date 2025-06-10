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

  const subrabbleForm = document.getElementById('subrabble-form');
  if (subrabbleForm) {
    subrabbleForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      // Get form data
      const formData = new FormData(subrabbleForm);
      const data = {};
      for (let [key, value] of formData.entries()) {
        if (key === 'members') {
          // Handle multiple select for members
          if (!data.members) data.members = [];
          data.members.push(value);
        } else if (key === 'allow_anonymous' || key === 'private') {
          data[key] = value === 'on';
        } else {
          data[key] = value;
        }
      }

      try {
        const response = await fetch(subrabbleForm.dataset.editUrl, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: JSON.stringify(data)
        });

        if (response.ok) {
          // If community_id was changed, we need to update the success URL
          const responseData = await response.json();
          if (data.subrabble_community_id && data.subrabble_community_id !== subrabbleForm.dataset.originalCommunityId) {
            window.location.href = subrabbleForm.dataset.successUrl.replace(
              subrabbleForm.dataset.originalCommunityId,
              data.subrabble_community_id
            );
          } else {
            window.location.href = subrabbleForm.dataset.successUrl;
          }
        } else {
          const errorData = await response.json();
          // Display errors
          const errorDiv = document.createElement('div');
          errorDiv.className = 'alert alert-danger';
          errorDiv.innerHTML = Object.entries(errorData)
            .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
            .join('<br>');
          subrabbleForm.insertBefore(errorDiv, subrabbleForm.firstChild);
        }
      } catch (error) {
        console.error('Error:', error);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.textContent = 'An error occurred while saving changes.';
        subrabbleForm.insertBefore(errorDiv, subrabbleForm.firstChild);
      }
    });
  }
});
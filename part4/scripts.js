document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.querySelector('#login-form');
  const errorMessage = document.querySelector('#error-message');

  if (loginForm) {
    loginForm.addEventListener('submit', function (event) {
      event.preventDefault();

      errorMessage.style.display = 'none';
      errorMessage.textContent = '';

      const email = document.querySelector('#email').value;
      const password = document.querySelector('#password').value;

      fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(
          {
            email: email,
            password: password
          }
        )
      })
        .then(function (response) {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error(response.statusText);
          }
        })
        .then(function (data) {
          document.cookie = 'token=' + data.access_token + '; path=/';
          window.location.href = 'index.html';
        })
        .catch(function (error) {
          console.error('Error during login:', error);

          errorMessage.textContent = 'Email or password incorrect.';
          errorMessage.style.display = 'block';
        });
    });
  }
});
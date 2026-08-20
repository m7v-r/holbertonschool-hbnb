document.addEventListener('DOMContentLoaded', function () {
  
  // ==========================================
  // TASK 1: LOGIN PAGE LOGIC
  // ==========================================
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
        body: JSON.stringify({
          email: email,
          password: password
        })
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

  // ==========================================
  // TASK 2: INDEX PAGE LOGIC
  // ==========================================
  const placesList = document.querySelector('#places-list');

  if (placesList) {
    // We removed populateDropdown() from here because we need the data first!
    checkAuthentication();
  }
});

// --- Helper Functions for Task 2 ---

// 1. Grabs the JWT token from the browser cookies
function getCookie(name) {
  const cookieString = document.cookie;
  const cookies = cookieString.split('; ');

  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const parts = cookie.split('=');
    if (parts[0] === name) {
      return parts[1];
    }
  }
  return null;
}

// 2. Checks if user is logged in and handles the UI
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// 3. API call to get places
function fetchPlaces(token) {
  fetch('http://127.0.0.1:5000/api/v1/places', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }
  })
  .then(function (response) {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to fetch places');
    }
  })
  .then(function (placesData) {
    displayPlaces(placesData);
    populateDynamicDropdown(placesData); // <-- Build the dropdown dynamically
    setupFilter(placesData);
  })
  .catch(function (error) {
    console.error('Error fetching places:', error);
  });
}

// 4. Builds the HTML for the places and injects it into the page
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = ''; 

  places.forEach(function (place) {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';

    placeCard.innerHTML =
      '<h2>' + place.name + '</h2>' +
      '<p>Price per night: $' + place.price + '</p>' +
      '<button class="details-button">View Details</button>';

    placesList.appendChild(placeCard);
  });
}

// 5. NEW: Dynamically inspects prices and builds the dropdown options
function populateDynamicDropdown(places) {
  const priceFilter = document.getElementById('price-filter');
  priceFilter.innerHTML = ''; // Clear out any existing options

  // Always add the "All" option first
  const allOption = document.createElement('option');
  allOption.value = 'All';
  allOption.textContent = 'All';
  priceFilter.appendChild(allOption);

  if (places.length === 0) return; // Stop here if there are no places

  // Find the absolute lowest and highest prices in the array
  let minPrice = Infinity;
  let maxPrice = -Infinity;

  places.forEach(function(place) {
    if (place.price < minPrice) {
      minPrice = place.price;
    }
    if (place.price > maxPrice) {
      maxPrice = place.price;
    }
  });

  // Round up to the nearest 10 (e.g., 95 -> 100, 389 -> 390)
  const startTarget = Math.ceil(minPrice / 10) * 10;
  const endTarget = Math.ceil(maxPrice / 10) * 10;

  // Generate options in increments of 10
  for (let currentPrice = startTarget; currentPrice <= endTarget; currentPrice += 10) {
    const opt = document.createElement('option');
    opt.value = currentPrice;
    opt.textContent = '$' + currentPrice;
    priceFilter.appendChild(opt);
  }
}

// 6. Client-side filtering logic
function setupFilter(allPlaces) {
  const priceFilter = document.getElementById('price-filter');

  if (priceFilter) {
    priceFilter.addEventListener('change', function (event) {
      const selectedPrice = event.target.value;

      if (selectedPrice === 'All') {
        displayPlaces(allPlaces);
      } else {
        const maxPrice = parseInt(selectedPrice, 10);
        
        const filteredPlaces = allPlaces.filter(function (place) {
          return place.price <= maxPrice;
        });

        displayPlaces(filteredPlaces);
      }
    });
  }
}
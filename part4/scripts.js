const API_URL = "http://127.0.0.1:5000/api/v1";

/* ---------- Cookies ---------- */

function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }

    return null;
}

/* ---------- Login ---------- */

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Login failed");
    }

    document.cookie =
        `token=${encodeURIComponent(data.access_token)}; path=/`;

    window.location.href = "index.html";
}

function setupLogin() {
    const form = document.getElementById("login-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const error = document.getElementById("login-error");

        error.textContent = "";

        try {
            await loginUser(email, password);
        } catch (err) {
            error.textContent = err.message;
        }
    });
}

/* ---------- Places ---------- */

async function fetchPlaces(token) {
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}/places/`, {
        method: "GET",
        headers: headers
    });

    if (!response.ok) {
        throw new Error("Failed to fetch places");
    }

    const places = await response.json();
    displayPlaces(places);
}

function displayPlaces(places) {
    const list = document.getElementById("places-list");

    if (!list) {
        return;
    }

    list.innerHTML = "";

    places.forEach((place) => {
        const card = document.createElement("div");
        card.className = "place-card";
        card.dataset.price = place.price;

        card.innerHTML = `
            <h2>${escapeHTML(place.title)}</h2>
            <p>${escapeHTML(place.description || "No description")}</p>
            <p>Price: ${place.price} SAR / night</p>
            <a class="details-button"
               href="place.html?id=${encodeURIComponent(place.id)}">
                View Details
            </a>
        `;

        list.appendChild(card);
    });
}

function setupPriceFilter() {
    const filter = document.getElementById("price-filter");

    if (!filter) {
        return;
    }

    filter.addEventListener("change", (event) => {
        const selected = event.target.value;
        const cards = document.querySelectorAll(".place-card");

        cards.forEach((card) => {
            const price = Number(card.dataset.price);

            card.style.display =
                selected === "all" || price <= Number(selected)
                    ? ""
                    : "none";
        });
    });
}

async function setupIndex() {
    const list = document.getElementById("places-list");

    if (!list) {
        return;
    }

    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    if (!token) {
        if (loginLink) {
            loginLink.style.display = "block";
        }

        window.location.href = "login.html";
        return;
    }

    if (loginLink) {
        loginLink.style.display = "none";
    }

    try {
        await fetchPlaces(token);
    } catch (err) {
        console.error(err);
    }

    setupPriceFilter();
}

/* ---------- Place details ---------- */

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

async function fetchPlaceDetails(token, placeId) {
    const response = await fetch(
        `${API_URL}/places/${encodeURIComponent(placeId)}`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch place details");
    }

    const place = await response.json();
    displayPlaceDetails(place);

    await fetchPlaceReviews(placeId, token);
}

function displayPlaceDetails(place) {
    const container = document.getElementById("place-details");

    if (!container) {
        return;
    }

    const owner = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : place.owner_id || "Unknown";

    const amenities = (place.amenities || [])
        .map((amenity) =>
            `<li>${escapeHTML(amenity.name || amenity.id || amenity)}</li>`
        )
        .join("");

    container.innerHTML = `
        <div class="place-info">
            <h1>${escapeHTML(place.title)}</h1>
            <p><strong>Host:</strong> ${escapeHTML(owner)}</p>
            <p><strong>Price:</strong> ${place.price} SAR / night</p>
            <p><strong>Description:</strong>
                ${escapeHTML(place.description || "No description")}
            </p>

            <h2>Amenities</h2>
            <ul>
                ${amenities || "<li>No amenities listed</li>"}
            </ul>
        </div>
    `;
}

async function fetchPlaceReviews(placeId, token) {
    const response = await fetch(
        `${API_URL}/places/${encodeURIComponent(placeId)}/reviews`
    );

    if (!response.ok) {
        throw new Error("Failed to fetch reviews");
    }

    const reviews = await response.json();
    displayReviews(reviews);
}

function displayReviews(reviews) {
    const list = document.getElementById("reviews-list");

    if (!list) {
        return;
    }

    list.innerHTML = "";

    if (!reviews.length) {
        list.innerHTML = "<p>No reviews yet.</p>";
        return;
    }

    reviews.forEach((review) => {
        const card = document.createElement("div");
        card.className = "review-card";

        card.innerHTML = `
            <p><strong>Comment:</strong>
                ${escapeHTML(review.text)}
            </p>
            <p><strong>Rating:</strong> ${review.rating}/5</p>
            <p><strong>User:</strong>
                ${escapeHTML(review.user_id || "User")}
            </p>
        `;

        list.appendChild(card);
    });
}

function setupAddReviewLink() {
    const section = document.getElementById("add-review");
    const link = document.getElementById("add-review-link");

    if (!section || !link) {
        return;
    }

    const token = getCookie("token");

    if (!token) {
        section.style.display = "none";
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (placeId) {
        link.href =
            `add_review.html?id=${encodeURIComponent(placeId)}`;
    }
}

/* ---------- Add review ---------- */

async function submitReview(token, placeId, text, rating) {
    const response = await fetch(`${API_URL}/reviews/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
            text: text,
            rating: Number(rating),
            place_id: placeId
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Failed to submit review");
    }

    return data;
}

function setupReviewForm() {
    const form = document.getElementById("review-form");

    if (!form) {
        return;
    }

    const token = getCookie("token");

    if (!token) {
        window.location.href = "index.html";
        return;
    }

    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        window.location.href = "index.html";
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const text = document.getElementById("review").value;
        const rating = document.getElementById("rating").value;
        const message = document.getElementById("review-message");

        message.textContent = "";

        try {
            await submitReview(token, placeId, text, rating);

            message.textContent =
                "Review submitted successfully.";

            form.reset();
        } catch (err) {
            message.textContent = err.message;
        }
    });
}

/* ---------- Small HTML safety helper ---------- */

function escapeHTML(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

/* ---------- Page startup ---------- */

document.addEventListener("DOMContentLoaded", async () => {
    setupLogin();
    setupAddReviewLink();
    setupReviewForm();

    const placeDetails =
        document.getElementById("place-details");

    if (placeDetails) {
        const placeId = getPlaceIdFromURL();

        if (!placeId) {
            placeDetails.innerHTML =
                "<p>Invalid place ID.</p>";
            return;
        }

        const token = getCookie("token");

        try {
            await fetchPlaceDetails(token, placeId);
        } catch (err) {
            placeDetails.innerHTML =
                "<p>Failed to load place details.</p>";
            console.error(err);
        }
    } else {
        await setupIndex();
    }
});

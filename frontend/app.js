const API_BASE = "http://localhost:8000";

const dishes = [
  {id:"pizza-margherita",name:"Margherita Pizza",category:"Pizza",price:189,emoji:"🍕",rating:"4.9",description:"Tomato, mozzarella, fresh basil",badge:"Bestseller"},
  {id:"grilled-chicken",name:"Grilled Chicken",category:"Mains",price:249,emoji:"🍗",rating:"4.8",description:"Herb-marinated, grilled to perfection",badge:"Chef's pick"},
  {id:"pasta-alfredo",name:"Pasta Alfredo",category:"Pasta",price:219,emoji:"🍝",rating:"4.7",description:"Creamy parmesan sauce and herbs",badge:"Comfort food"},
  {id:"classic-burger",name:"Classic Burger",category:"Mains",price:229,emoji:"🍔",rating:"4.8",description:"Juicy beef, cheddar, house sauce",badge:"Fan favourite"},
  {id:"crispy-fries",name:"Crispy Fries",category:"Sides",price:79,emoji:"🍟",rating:"4.6",description:"Golden, crunchy, perfectly salted",badge:"Perfect side"},
  {id:"garden-salad",name:"Garden Salad",category:"Sides",price:119,emoji:"🥗",rating:"4.7",description:"Crisp greens, tomato, lemon dressing",badge:"Fresh pick"}
];

const $ = (selector) => document.querySelector(selector);
const menuGrid = $("#menu-grid");
const cartCount = $("#cart-count");
const cartItems = $("#cart-items");
const cartTotal = $("#cart-total");
const toast = $("#toast");
let selectedCategory = "All";
let authMode = "login";
let cart = loadCart();
let toastTimer;

function loadCart() {
  try { return JSON.parse(localStorage.getItem("ff_cart") || "{}"); }
  catch { return {}; }
}
function saveCart() {
  localStorage.setItem("ff_cart", JSON.stringify(cart));
  renderCart();
}
function money(amount) {
  return `EGP ${Number(amount).toFixed(2)}`;
}
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2300);
}
function renderMenu() {
  const query = $("#menu-search").value.trim().toLowerCase();
  const visible = dishes.filter(d => (selectedCategory === "All" || d.category === selectedCategory)
    && `${d.name} ${d.description} ${d.category}`.toLowerCase().includes(query));
  menuGrid.innerHTML = visible.length ? visible.map(d => `
    <article class="dish-card">
      <div class="dish-art"><span class="dish-badge">${d.badge}</span><span class="dish-emoji" aria-hidden="true">${d.emoji}</span></div>
      <div class="dish-info">
        <div class="dish-top"><div><h3>${d.name}</h3><p>${d.description}</p></div><span class="dish-price">${money(d.price)}</span></div>
        <div class="dish-bottom"><div class="rating">★ ${d.rating}<span> · ${d.category}</span></div><button class="add-button" data-add="${d.id}" aria-label="Add ${d.name} to cart">+</button></div>
      </div>
    </article>`).join("") : `<div class="empty-state">No dishes match that search. Try another name.</div>`;
}
function cartQuantity() {
  return Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
}
function renderCart() {
  const items = Object.values(cart);
  cartCount.textContent = cartQuantity();
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  cartTotal.textContent = money(total);
  if (!items.length) {
    cartItems.innerHTML = `<div class="cart-empty"><span>🛍️</span>Your basket is waiting for something delicious.</div>`;
    return;
  }
  cartItems.innerHTML = items.map(item => `
    <div class="cart-row">
      <div class="cart-thumb">${item.emoji}</div>
      <div><h4>${item.name}</h4><small>${money(item.price)} each</small>
        <div class="quantity-controls">
          <button data-qty="${item.id}" data-delta="-1" aria-label="Decrease ${item.name} quantity">−</button>
          <span>${item.quantity}</span>
          <button data-qty="${item.id}" data-delta="1" aria-label="Increase ${item.name} quantity">+</button>
        </div>
      </div><span class="line-total">${money(item.price * item.quantity)}</span>
    </div>`).join("");
}
function addToCart(id) {
  const dish = dishes.find(d => d.id === id);
  if (!dish) return;
  if (cart[id]) cart[id].quantity += 1;
  else cart[id] = {...dish, quantity: 1};
  saveCart();
  showToast(`${dish.name} added to your basket`);
}
function changeQuantity(id, delta) {
  if (!cart[id]) return;
  cart[id].quantity += delta;
  if (cart[id].quantity <= 0) delete cart[id];
  saveCart();
}
function openOverlay(id) { $(`#${id}`).hidden = false; document.body.style.overflow = "hidden"; }
function closeOverlay(id) { $(`#${id}`).hidden = true; document.body.style.overflow = ""; }
function setAuthMode(mode) {
  authMode = mode;
  document.querySelectorAll("[data-auth-mode]").forEach(btn => btn.classList.toggle("active", btn.dataset.authMode === mode));
  $("#auth-title").innerHTML = mode === "login" ? "Sign in <em>and savour.</em>" : "Join us <em>at the table.</em>";
  $("#auth-submit").innerHTML = mode === "login" ? 'Sign in <span>→</span>' : 'Create account <span>→</span>';
  $("#name-field").hidden = mode !== "register";
  $("#phone-field").hidden = mode !== "register";
  $("#auth-message").textContent = "";
  $("#auth-form").elements.password.autocomplete = mode === "login" ? "current-password" : "new-password";
}
async function checkApi() {
  const status = $("#api-status");
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) throw new Error("API unavailable");
    status.classList.add("online");
    status.innerHTML = "<i></i> API connected";
  } catch {
    status.classList.remove("online");
    status.innerHTML = "<i></i> API not reachable";
  }
}
async function handleAuth(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("#auth-message");
  const data = Object.fromEntries(new FormData(form).entries());
  const endpoint = authMode === "login" ? "/users/login" : "/users/register";
  message.className = "form-message";
  message.textContent = "Connecting to API…";
  $("#auth-submit").disabled = true;
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
      const detail = typeof result.detail === "string" ? result.detail : "Request failed. Check the fields and try again.";
      throw new Error(detail);
    }
    if (authMode === "login" && result.access_token) {
      localStorage.setItem("ff_access_token", result.access_token);
      localStorage.setItem("ff_user_email", data.email);
    }
    message.className = "form-message success";
    message.textContent = authMode === "login" ? "Signed in successfully." : "Account created successfully. You can now sign in.";
    if (authMode === "register") {
      form.reset();
      setAuthMode("login");
      message.className = "form-message success";
      message.textContent = "Account created. Please sign in.";
    } else {
      $("#open-auth").textContent = "My account";
      showToast("Welcome back!");
      setTimeout(() => closeOverlay("auth-overlay"), 700);
    }
  } catch (error) {
    message.className = "form-message error";
    message.textContent = error.message.includes("Failed to fetch")
      ? "Could not connect. Check that the API is running and CORS is enabled."
      : error.message;
  } finally {
    $("#auth-submit").disabled = false;
  }
}

document.addEventListener("click", (event) => {
  const addButton = event.target.closest("[data-add]");
  if (addButton) addToCart(addButton.dataset.add);
  const qtyButton = event.target.closest("[data-qty]");
  if (qtyButton) changeQuantity(qtyButton.dataset.qty, Number(qtyButton.dataset.delta));
  const closeButton = event.target.closest("[data-close]");
  if (closeButton) closeOverlay(closeButton.dataset.close);
  const authButton = event.target.closest("[data-auth-mode]");
  if (authButton) setAuthMode(authButton.dataset.authMode);
  const categoryButton = event.target.closest("[data-category]");
  if (categoryButton) {
    selectedCategory = categoryButton.dataset.category;
    document.querySelectorAll("[data-category]").forEach(btn => btn.classList.toggle("active", btn === categoryButton));
    renderMenu();
  }
});
$("#open-cart").addEventListener("click", () => { renderCart(); openOverlay("cart-overlay"); });
$("#open-auth").addEventListener("click", () => openOverlay("auth-overlay"));
$("#mobile-menu").addEventListener("click", () => $(".nav-links").classList.toggle("open"));
document.querySelectorAll(".nav-links a").forEach(link => link.addEventListener("click", () => $(".nav-links").classList.remove("open")));
document.querySelectorAll(".overlay").forEach(overlay => overlay.addEventListener("click", event => {
  if (event.target === overlay) closeOverlay(overlay.id);
}));
document.addEventListener("keydown", event => {
  if (event.key === "Escape") document.querySelectorAll(".overlay:not([hidden])").forEach(el => closeOverlay(el.id));
});
$("#menu-search").addEventListener("input", renderMenu);
$("#auth-form").addEventListener("submit", handleAuth);
$("#checkout-button").addEventListener("click", () => {
  const message = $("#cart-message");
  if (!cartQuantity()) {
    message.className = "form-message error";
    message.textContent = "Add at least one dish before checkout.";
    return;
  }
  message.className = "form-message";
  message.textContent = "The current backend checkout is a demo endpoint. We'll connect real order creation after reviewing its request schema.";
});
renderMenu();
renderCart();
checkApi();

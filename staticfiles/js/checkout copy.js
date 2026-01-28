const API_BASE = "http://127.0.0.1:2222";
//alert('99999') // debug
const orderItemsEl = document.getElementById("order-items");
const grandTotalEl = document.getElementById("grand-total");
const authErrorEl = document.getElementById("auth-error");

const placeOrderBtn = document.getElementById("place-order-btn");
const paymentSection = document.getElementById("payment-section");
const payBtn = document.getElementById("pay-btn");
const paymentStatus = document.getElementById("payment-status");
// -----------


if (!window.STRIPE_PUBLISHABLE_KEY) {
  alert("Stripe key missing");
}

let stripe = Stripe(window.STRIPE_PUBLISHABLE_KEY);
//alert(STRIPE_PUBLISHABLE_KEY)



// -----------------

let elements = stripe.elements();
let cardElement;

let clientSecret = null;

/* -------------------------------
   AUTH CHECK + LOAD CART
-------------------------------- */
async function loadCheckout() {
  const token = localStorage.getItem("access");
  if (!token) {
    authErrorEl.innerText = "Please login to continue checkout.";
    return;
  }

  const res = await apiFetch(`${API_BASE}/api/checkout/summary/`);
  if (!res.ok) {
    authErrorEl.innerText = "Unable to load cart. Please login again.";
    return;
  }

  const data = await res.json();
  renderCart(data);
}

function renderCart(data) {
  orderItemsEl.innerHTML = "";
  let total = 0;

  data.items.forEach(item => {
    const price = Number(item.price);
    const qty = Number(item.qty);
    const rowTotal = price * qty;

    total += rowTotal;

    orderItemsEl.innerHTML += `
      <tr>
        <td>${item.product}</td>
        <td>${qty}</td>
        <td>₹${price.toFixed(2)}</td>
        <td>₹${rowTotal.toFixed(2)}</td>
      </tr>
    `;
  });

  grandTotalEl.innerText = Number(data.total).toFixed(2);
}

/*
function renderCart(cart) {
  orderItemsEl.innerHTML = "";
  let total = 0;

  cart.items.forEach(item => {
    const row = document.createElement("tr");
    const rowTotal = Number(item.price_snapshot) * Number(item.quantity);
    total += rowTotal;

    row.innerHTML = `
      <td>${item.product.name}</td>
      <td>${Number(item.quantity)}</td>
      <td>₹${Number(item.price_snapshot)}</td>
      <td>₹${Number(rowTotal)}</td>
    `;
    orderItemsEl.appendChild(row);
  });

  grandTotalEl.innerText = total.toFixed(2);
}
*/
/* -------------------------------
   PLACE ORDER (CREATE INTENT)
-------------------------------- */
placeOrderBtn.addEventListener("click", async () => {
  paymentStatus.innerText = "Creating order...";

  const res = await apiFetch(`${API_BASE}/api/order-payment/place-order/`, {
    method: "POST"
  });

  if (!res.ok) {
    paymentStatus.innerText = "Order creation failed.";
    return;
  }

  const data = await res.json();
  clientSecret = data.client_secret;

  initStripeUI();
});

/* -------------------------------
   STRIPE UI
-------------------------------- */
function initStripeUI() {
  paymentSection.style.display = "block";

  cardElement = elements.create("card");
  cardElement.mount("#card-element");

  paymentStatus.innerText = "Enter card details.";
}

/* -------------------------------
   PAY NOW
-------------------------------- */
payBtn.addEventListener("click", async () => {
  paymentStatus.innerText = "Processing payment...";

  const result = await stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: cardElement,
    }
  });

  if (result.error)
  {
    paymentStatus.innerText = result.error.message;
  }
  else
     {
    if (result.paymentIntent.status === "succeeded") {
      paymentStatus.innerText = "Payment successful 🎉";
      alert(result)
      prompt(result.card)
      window.location.href = "/order-success/";
    }
  }
});

/* INIT */
loadCheckout();

async function checkUser() {
  const res = await apiFetch("/api/auth/me/");
  const box = document.getElementById("user-status");

  if (res.ok) {
    const data = await res.json();
    box.innerText = data.username;
  } else {
    box.innerText = "Guest";
  }
} 

async function loadProducts() {
  const res = await fetch("/api/products/");
  const data = await res.json();

  const box = document.getElementById("product-list");
  box.innerHTML = "";

  data.results.forEach(p => {
    box.innerHTML += `
      <div>
        <h4>${p.name}</h4>
        <p>₹${p.final_price}</p>
        <button onclick="addToCart(${p.id})">Add</button>
      </div>
    `;
  });
}

async function addToCart(id) {
  const res = await apiFetch("/api/cart/cart/add_item/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product: id, quantity: 1 })
  });

  if (!res.ok) {
    alert("Login required");
  } else {
    loadCart();
  }
}

async function loadCart() {
  const res = await apiFetch("/api/cart/cart/list_items/");
  if (!res.ok) return;

  const data = await res.json();

  let totalQty = 0;
  data.items.forEach(item => {
    totalQty += item.quantity;
  });

  document.getElementById("cart-count").innerText = totalQty;
}
checkUser();
loadProducts();
loadCart();

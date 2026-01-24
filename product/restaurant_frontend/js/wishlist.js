async function loadWishlist() {
  const res = await apiFetch("/api/wishlist/");
   if (!res.ok) {
    alert("Please login to view your cart");
    return;
  }
  

  const data = await res.json();

  const box = document.getElementById("wishlist-items");
  box.innerHTML = "";

  if (data.data.length === 0) {
    box.innerHTML = "<p>No items in wishlist</p>";
    return;
  }

  data.data.forEach(item => {
    box.innerHTML += `
      <div>
        <b>${item.product.name}</b> 
        ₹${item.product.price}

        <button onclick="removeFromWishlist(${item.product.id})">
          Remove
        </button>

        <button onclick="moveToCart(${item.product.id})">
          Move to Cart
        </button>
      </div>
      <hr>
    `;
  });
}

async function removeFromWishlist(productId) {
  const res = await apiFetch("/api/wishlist/", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product: productId })
  });

  if (res.ok) loadWishlist();
}

async function moveToCart(productId) {
  await apiFetch("/api/cart/cart/add_item/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product: productId, quantity: 1 })
  });

  await removeFromWishlist(productId);
}

document.addEventListener("DOMContentLoaded", loadWishlist);

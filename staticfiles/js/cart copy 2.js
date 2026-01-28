async function loadCart() {
    const box = document.getElementById("cart-items");
    box.innerHTML = `
    <div class="loading" style="text-align: center; padding: 40px;">
      <div style="display: inline-block; width: 50px; height: 50px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite;"></div>
      <p>Loading your cart...</p>
    </div>
  `;
  //alert('222')
  const res = await apiFetch("/api/cart/cart/list_items/");
  if (!res.ok) {
    alert("Please login to view your cart");
    return;
  }

  const data = await res.json();
  console.log("CART API DATA:", data);

  //const box = document.getElementById("cart-items");
  let total = 0;

  if (!data.items || data.items.length === 0) {
    box.innerHTML = `
      <div class="empty-cart">
        <div class="empty-cart-icon">🛒</div>
        <p>Your cart is empty</p>
        <p>Add some delicious items from our menu!</p>
      </div>
    `;
  } else {
    let cartHTML = '';
    
    data.items.forEach(item => {
      const itemTotal = item.quantity * item.product_price;
      total += itemTotal;

      cartHTML += `
        <div class="cart-item" data-item-id="${item.product}">
          <div class="item-info">
            <div class="item-name">${item.product_name}</div>
            <div class="item-price">₹${item.product_price} per item</div>
          </div>
          <div class="item-actions">
            <div class="quantity-controls">
              <button class="qty-btn decrease" onclick="updateQty(${item.product}, -1)">
                <i class="fas fa-minus"></i>
              </button>
              <span class="quantity">${item.quantity}</span>
              <button class="qty-btn" onclick="updateQty(${item.product}, 1)">
                <i class="fas fa-plus"></i>
              </button>
            </div>
            <div class="item-subtotal">₹${itemTotal}</div>
            <button class="remove-btn" onclick="removeItem(${item.product})">
              <i class="fas fa-trash"></i> Remove
            </button>
          </div>
        </div>
      `;
    });
    
    box.innerHTML = cartHTML;
  }

  document.getElementById("cart-total").innerText = total.toLocaleString('en-IN');
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("Cart page loaded");
  loadCart();
});

async function updateQty(productId, change) {
  const res = await apiFetch("/api/cart/cart/add_item/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      product: productId,
      quantity: change
    })
  });

  if (res.ok) {
    // Show feedback animation
    const itemElement = document.querySelector(`[data-item-id="${productId}"]`);
    if (itemElement) {
      itemElement.style.transform = 'scale(1.02)';
      setTimeout(() => {
        itemElement.style.transform = '';
      }, 200);
    }
    loadCart();
  }
}

async function removeItem(productId) {
  if (!confirm("Are you sure you want to remove this item from your cart?")) {
    return;
  }

  const res = await apiFetch("/api/cart/cart/remove_item/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product: productId })
  });

  if (res.ok) {
    // Remove animation
    const itemElement = document.querySelector(`[data-item-id="${productId}"]`);
    if (itemElement) {
      itemElement.style.opacity = '0';
      itemElement.style.transform = 'translateX(-20px)';
      setTimeout(() => {
        loadCart();
      }, 300);
    } else {
      loadCart();
    }
  }
}

function checkout() {
  // Check if cart is empty
  const cartTotal = document.getElementById("cart-total").innerText;
  if (parseInt(cartTotal) === 0) {
    alert("Your cart is empty! Add some items before checkout.");
    return;
  }

  if (confirm(`Proceed to checkout with total of ₹${cartTotal}?`)) {
    // Here you can redirect to checkout page or open checkout modal
    alert("Checkout initiated! 🚀\nRedirecting to payment...");
    // window.location.href = "/checkout/"; // Uncomment to redirect to checkout page
  }
}

// Add at the top of loadCart function

  
  
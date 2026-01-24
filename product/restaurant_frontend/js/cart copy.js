// Fixed loadCart function for your API response
async function loadCart() {
  const box = document.getElementById("cart-items");
  box.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Loading your cart...</p>
    </div>
  `;
  
  try {
    const res = await apiFetch("/api/cart/cart/list_items/");
    
    if (!res.ok) {
      if (res.status === 401) {
        showNotification("Please login to view your cart", "error");
      } else {
        showNotification("Failed to load cart. Please try again.", "error");
      }
      box.innerHTML = `
        <div class="empty-cart">
          <div class="empty-cart-icon">🔒</div>
          <p>Login Required</p>
          <p>Please login to view your cart</p>
          <a href="/login" class="btn" style="display: inline-block; margin-top: 20px; padding: 12px 24px; background: var(--primary-red); color: white; border-radius: 25px; text-decoration: none;">Login Now</a>
        </div>
      `;
      return;
    }

    const data = await res.json();
    console.log("CART API DATA:", data);

    let total = 0;
    let cartHTML = '';

    if (!data.items || data.items.length === 0) {
      box.innerHTML = `
        <div class="empty-cart">
          <div class="empty-cart-icon">🛒</div>
          <p>Your cart is empty</p>
          <p>Add some delicious items from our menu!</p>
        </div>
      `;
    } else {
      // We need to fetch product details to get prices
      // First, let's fetch all products to get prices
      const productsRes = await fetch("/api/products/");
      const productsData = await productsRes.json();
      
      // Create a map of product ID to price
      const priceMap = {};
      productsData.results.forEach(product => {
        priceMap[product.id] = parseFloat(product.final_price);
      });

      // Now render cart items with prices
      data.items.forEach(item => {
        const productPrice = priceMap[item.product] || 0; // Fallback to 0 if price not found
        const itemTotal = item.quantity * productPrice;
        total += itemTotal;

        cartHTML += `
          <div class="cart-item" data-item-id="${item.product}">
            <div class="item-info">
              <div class="item-name">${item.product_name}</div>
              <div class="item-price">₹${productPrice.toFixed(2)} per item</div>
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
              <div class="item-subtotal">₹${itemTotal.toFixed(2)}</div>
              <button class="remove-btn" onclick="removeItem(${item.product})">
                <i class="fas fa-trash"></i> Remove
              </button>
            </div>
          </div>
        `;
      });
      
      box.innerHTML = cartHTML;
    }

    document.getElementById("cart-total").innerText = total.toFixed(2);

  } catch (error) {
    console.error("Error loading cart:", error);
    box.innerHTML = `
      <div class="empty-cart">
        <div class="empty-cart-icon">⚠️</div>
        <p>Error loading cart</p>
        <p>Please try again later</p>
        <button onclick="loadCart()" class="btn" style="margin-top: 20px; padding: 12px 24px; background: var(--primary-blue); color: white; border: none; border-radius: 25px; cursor: pointer;">Retry</button>
      </div>
    `;
  }
}

// Fixed updateQty function
async function updateQty(productId, change) {
  try {
    // First, get current cart to find item quantity
    const cartRes = await apiFetch("/api/cart/cart/list_items/");
    if (!cartRes.ok) {
      showNotification("Failed to update quantity. Please try again.", "error");
      return;
    }
    
    const cartData = await cartRes.json();
    const cartItem = cartData.items.find(item => item.product === productId);
    const currentQty = cartItem ? cartItem.quantity : 0;
    const newQty = currentQty + change;
    
    if (newQty < 1) {
      // If quantity becomes 0 or negative, remove item
      await removeItem(productId);
      return;
    }
    
    const res = await apiFetch("/api/cart/cart/add_item/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product: productId,
        quantity: change  // Send the delta, not the total
      })
    });

    if (res.ok) {
      const updatedData = await res.json();
      console.log("Updated item:", updatedData);
      
      // Show feedback animation
      const itemElement = document.querySelector(`[data-item-id="${productId}"]`);
      if (itemElement) {
        if (change > 0) {
          // Added item - green highlight
          itemElement.style.background = 'linear-gradient(to right, transparent, rgba(6, 214, 160, 0.2), transparent)';
        } else {
          // Removed item - orange highlight
          itemElement.style.background = 'linear-gradient(to right, transparent, rgba(255, 157, 0, 0.2), transparent)';
        }
        itemElement.style.transform = 'scale(1.05)';
        
        setTimeout(() => {
          itemElement.style.transform = '';
          itemElement.style.background = '';
        }, 300);
      }
      
      // Show notification
      if (change > 0) {
        showNotification(`Added 1 more item to cart!`, "success");
      } else {
        showNotification(`Removed 1 item from cart`, "info");
      }
      
      loadCart();
    } else {
      const errorData = await res.json();
      showNotification(errorData.detail || "Failed to update quantity", "error");
    }
    
  } catch (error) {
    console.error("Error updating quantity:", error);
    showNotification("Failed to update quantity. Please try again.", "error");
  }
}

// Fixed removeItem function
async function removeItem(productId) {
  if (!confirm("Are you sure you want to remove this item from your cart?")) {
    return;
  }

  try {
    const res = await apiFetch("/api/cart/cart/remove_item/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product: productId })
    });

    if (res.ok) {
      // Create confetti animation
      createConfetti();
      
      // Remove animation
      const itemElement = document.querySelector(`[data-item-id="${productId}"]`);
      if (itemElement) {
        itemElement.style.opacity = '0';
        itemElement.style.transform = 'translateX(-50px) rotate(-10deg)';
        setTimeout(() => {
          showNotification("Item removed from cart", "success");
          loadCart();
        }, 400);
      } else {
        showNotification("Item removed from cart", "success");
        loadCart();
      }
    } else {
      const errorData = await res.json();
      showNotification(errorData.detail || "Failed to remove item", "error");
    }
  } catch (error) {
    console.error("Error removing item:", error);
    showNotification("Failed to remove item. Please try again.", "error");
  }
}

// Add this helper function for notifications
function showNotification(message, type = "info") {
  // Create notification element if it doesn't exist
  let notification = document.getElementById("notification");
  if (!notification) {
    notification = document.createElement("div");
    notification.id = "notification";
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 25px;
      border-radius: 15px;
      color: white;
      font-weight: bold;
      z-index: 1000;
      box-shadow: 0 8px 20px rgba(0,0,0,0.2);
      border: 4px solid #073B4C;
      animation: slideIn 0.3s ease;
      font-family: 'Comic Neue', cursive;
    `;
    document.body.appendChild(notification);
  }
  
  // Set color based on type
  if (type === "error") {
    notification.style.background = "linear-gradient(135deg, var(--primary-red), #FF5D8F)";
  } else if (type === "success") {
    notification.style.background = "linear-gradient(135deg, var(--primary-green), var(--primary-blue))";
  } else {
    notification.style.background = "linear-gradient(135deg, var(--primary-blue), var(--primary-purple))";
  }
  
  notification.innerText = message;
  notification.style.display = 'block';
  
  // Add animation style if not already present
  if (!document.getElementById('notification-style')) {
    const style = document.createElement('style');
    style.id = 'notification-style';
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
    `;
    document.head.appendChild(style);
  }
  
  setTimeout(() => {
    notification.style.display = 'none';
  }, 3000);
}

// Confetti animation function
function createConfetti(count = 30) {
  const colors = ['#FFD166', '#EF476F', '#06D6A0', '#118AB2', '#8338EC', '#FF5D8F', '#FF9E00'];
  
  for (let i = 0; i < count; i++) {
    const confetti = document.createElement('div');
    confetti.className = 'confetti';
    confetti.style.left = Math.random() * 100 + 'vw';
    confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.animation = `confetti ${Math.random() * 2 + 1}s linear forwards`;
    confetti.style.animationDelay = Math.random() * 0.5 + 's';
    confetti.style.width = Math.random() * 15 + 10 + 'px';
    confetti.style.height = confetti.style.width;
    confetti.style.position = 'fixed';
    confetti.style.zIndex = '9999';
    confetti.style.borderRadius = '50%';
    confetti.style.opacity = '0';
    
    // Add confetti animation if not already present
    if (!document.getElementById('confetti-style')) {
      const style = document.createElement('style');
      style.id = 'confetti-style';
      style.textContent = `
        @keyframes confetti {
          0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
          100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }
    
    document.body.appendChild(confetti);
    
    setTimeout(() => {
      confetti.remove();
    }, 2000);
  }
}

// Update the DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", () => {
  console.log("Cart page loaded");
  loadCart();
});

// Update the checkout function
function checkout() {
  // Check if cart is empty by checking if cart-total is 0
  const cartTotalElement = document.getElementById("cart-total");
  if (!cartTotalElement) return;
  
  const cartTotalText = cartTotalElement.innerText;
  const cartTotalValue = parseFloat(cartTotalText);
  
  if (isNaN(cartTotalValue) || cartTotalValue === 0) {
    showNotification("Your cart is empty! Add some items before checkout.", "error");
    return;
  }

  if (confirm(`Proceed to checkout with total of ₹${cartTotalValue.toFixed(2)}?`)) {
    // Create celebration animation
    createConfetti(50);
    setTimeout(() => {
      showNotification("Checkout initiated! 🚀 Redirecting to payment...", "success");
      // window.location.href = "/checkout/"; // Uncomment to redirect to checkout page
    }, 500);
  }
}
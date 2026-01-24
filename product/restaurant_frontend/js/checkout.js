const API_BASE = "http://127.0.0.1:2222";

// DOM Elements
const orderItemsEl = document.getElementById("order-items");
const grandTotalEl = document.getElementById("grand-total");
const authErrorEl = document.getElementById("auth-error");
const placeOrderBtn = document.getElementById("place-order-btn");
const paymentSection = document.getElementById("payment-section");
const payBtn = document.getElementById("pay-btn");
const paymentStatus = document.getElementById("payment-status");
const paymentMethodSelect = document.getElementById("payment-method");

// UI Components
let loadingOverlay, shimmerLoader, paymentLoader, progressBar, toastContainer;
let confirmationModal, paymentSuccessModal, paymentProcessingModal;

// State Management
let isProcessing = false;
let debounceTimeout = null;
let paymentResult = null;

// Stripe
if (!window.STRIPE_PUBLISHABLE_KEY) {
  showToast("Stripe key missing", "error");
}

let stripe = Stripe(window.STRIPE_PUBLISHABLE_KEY);
let elements = stripe.elements();
let cardElement;
let clientSecret = null;

/* ======================
   UI COMPONENT SETUP
======================= */
function setupUIComponents() {
  // Create loading overlay
  loadingOverlay = document.createElement('div');
  loadingOverlay.className = 'payment-ui-overlay';
  loadingOverlay.innerHTML = `
    <div class="payment-loading-container">
      <div class="payment-spinner-animation">
        <div class="spinner-circle"></div>
        <div class="spinner-circle"></div>
        <div class="spinner-circle"></div>
        <div class="spinner-circle"></div>
      </div>
      <div class="payment-loading-text">Preparing your payment...</div>
      <div class="payment-subtext">Securing your transaction</div>
    </div>
  `;
  document.body.appendChild(loadingOverlay);
  
  // Create shimmer loader
  shimmerLoader = document.createElement('div');
  shimmerLoader.className = 'payment-shimmer-loader';
  shimmerLoader.innerHTML = `
    <div class="payment-shimmer-line"></div>
    <div class="payment-shimmer-line"></div>
    <div class="payment-shimmer-line"></div>
    <div class="payment-shimmer-line"></div>
  `;
  
  // Create payment processing modal
  paymentProcessingModal = document.createElement('div');
  paymentProcessingModal.className = 'payment-processing-modal';
  paymentProcessingModal.innerHTML = `
    <div class="processing-modal-content">
      <div class="processing-animation">
        <div class="secure-shield-icon">🛡️</div>
        <div class="rotating-rings">
          <div class="ring ring-1"></div>
          <div class="ring ring-2"></div>
          <div class="ring ring-3"></div>
        </div>
        <div class="sparkle sparkle-1">✨</div>
        <div class="sparkle sparkle-2">✨</div>
        <div class="sparkle sparkle-3">✨</div>
      </div>
      <h3 class="processing-title">Processing Payment</h3>
      <p class="processing-message">Please wait while we secure your transaction</p>
      <div class="processing-progress">
        <div class="progress-track">
          <div class="progress-fill-animated"></div>
        </div>
        <div class="progress-steps">
          <span class="step">Verifying</span>
          <span class="step">Processing</span>
          <span class="step">Confirming</span>
        </div>
      </div>
      <div class="processing-details">
        <div class="detail-item">
          <span class="detail-label">Status:</span>
          <span class="detail-value status-indicator">Initializing...</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Security:</span>
          <span class="detail-value security-badge">256-bit Encrypted</span>
        </div>
      </div>
    </div>
  `;
  
  // Create payment success modal
  paymentSuccessModal = document.createElement('div');
  paymentSuccessModal.className = 'payment-success-modal';
  paymentSuccessModal.innerHTML = `
    <div class="success-modal-content">
      <div class="success-animation">
        <div class="success-checkmark">
          <div class="check-icon">✓</div>
        </div>
        <div class="confetti-container"></div>
      </div>
      <h2 class="success-title">Payment Successful! 🎉</h2>
      <div class="success-details">
        <div class="success-detail-card">
          <div class="detail-header">
            <span class="detail-icon">💰</span>
            <span class="detail-title">Amount Paid</span>
          </div>
          <div class="detail-value" id="success-amount">₹0.00</div>
        </div>
        <div class="success-detail-card">
          <div class="detail-header">
            <span class="detail-icon">📄</span>
            <span class="detail-title">Transaction ID</span>
          </div>
          <div class="detail-value" id="success-transaction">Loading...</div>
        </div>
        <div class="success-detail-card">
          <div class="detail-header">
            <span class="detail-icon">🕒</span>
            <span class="detail-title">Time</span>
          </div>
          <div class="detail-value" id="success-time">${new Date().toLocaleTimeString()}</div>
        </div>
      </div>
      <div class="success-message">
        <p>Your payment has been processed successfully!</p>
        <p class="success-submessage">You will be redirected to the order confirmation page shortly.</p>
      </div>
      <div class="success-actions">
        <button class="success-btn primary-btn" id="continue-to-confirmation">
          Continue to Confirmation Page
        </button>
        <button class="success-btn secondary-btn" id="view-receipt">
          View Receipt
        </button>
      </div>
      <div class="success-footer">
        <span class="footer-note">💡 Pro tip: Save this transaction ID for future reference</span>
      </div>
    </div>
  `;
  
  // Create toast container
  toastContainer = document.createElement('div');
  toastContainer.className = 'payment-toast-container';
  document.body.appendChild(toastContainer);
  
  // Add enhanced styles
  addPaymentStyles();
}

/* ======================
   PAYMENT STYLES
======================= */
function addPaymentStyles() {
  const style = document.createElement('style');
  style.textContent = `
    /* Payment Overlay */
    .payment-ui-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,248,255,0.98) 100%);
      backdrop-filter: blur(10px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 9998;
      animation: fadeInPayment 0.4s ease;
    }
    
    @keyframes fadeInPayment {
      from { opacity: 0; backdrop-filter: blur(0); }
      to { opacity: 1; backdrop-filter: blur(10px); }
    }
    
    .payment-loading-container {
      text-align: center;
      padding: 40px;
      background: white;
      border-radius: 24px;
      box-shadow: 0 20px 60px rgba(106, 90, 249, 0.15);
      border: 2px solid #f0f0ff;
      animation: floatAnimation 3s ease-in-out infinite;
    }
    
    @keyframes floatAnimation {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    
    .payment-spinner-animation {
      position: relative;
      width: 120px;
      height: 120px;
      margin: 0 auto 30px;
    }
    
    .spinner-circle {
      position: absolute;
      width: 100%;
      height: 100%;
      border: 3px solid transparent;
      border-radius: 50%;
      border-top-color: #6A5AF9;
      animation: spinPayment 2s linear infinite;
    }
    
    .spinner-circle:nth-child(2) {
      border-top-color: #FF6B8B;
      animation-delay: 0.5s;
      width: 85%;
      height: 85%;
      top: 7.5%;
      left: 7.5%;
    }
    
    .spinner-circle:nth-child(3) {
      border-top-color: #00D4AA;
      animation-delay: 1s;
      width: 70%;
      height: 70%;
      top: 15%;
      left: 15%;
    }
    
    .spinner-circle:nth-child(4) {
      border-top-color: #FFAA2C;
      animation-delay: 1.5s;
      width: 55%;
      height: 55%;
      top: 22.5%;
      left: 22.5%;
    }
    
    @keyframes spinPayment {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .payment-loading-text {
      font-size: 1.4em;
      font-weight: 700;
      color: #333;
      margin-bottom: 8px;
      background: linear-gradient(90deg, #6A5AF9, #FF6B8B, #00D4AA);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .payment-subtext {
      color: #666;
      font-size: 0.95em;
    }
    
    /* Payment Processing Modal */
    .payment-processing-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(15px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 10000;
      animation: modalAppear 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes modalAppear {
      from {
        opacity: 0;
        transform: scale(0.9);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }
    
    .processing-modal-content {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border-radius: 28px;
      padding: 50px 40px;
      width: 90%;
      max-width: 500px;
      text-align: center;
      border: 2px solid rgba(106, 90, 249, 0.3);
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
      position: relative;
      overflow: hidden;
    }
    
    .processing-modal-content::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: conic-gradient(
        transparent,
        rgba(106, 90, 249, 0.1),
        transparent 30%
      );
      animation: rotateBorder 3s linear infinite;
      z-index: 0;
    }
    
    @keyframes rotateBorder {
      100% { transform: rotate(360deg); }
    }
    
    .processing-animation {
      position: relative;
      width: 150px;
      height: 150px;
      margin: 0 auto 30px;
      z-index: 1;
    }
    
    .secure-shield-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 50px;
      color: #00D4AA;
      z-index: 3;
      animation: pulseShield 2s ease-in-out infinite;
    }
    
    @keyframes pulseShield {
      0%, 100% { transform: translate(-50%, -50%) scale(1); }
      50% { transform: translate(-50%, -50%) scale(1.1); }
    }
    
    .rotating-rings {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
    }
    
    .ring {
      position: absolute;
      border-radius: 50%;
      border: 2px dashed;
    }
    
    .ring-1 {
      width: 100%;
      height: 100%;
      border-color: rgba(106, 90, 249, 0.4);
      animation: rotateRing 20s linear infinite;
    }
    
    .ring-2 {
      width: 80%;
      height: 80%;
      top: 10%;
      left: 10%;
      border-color: rgba(0, 212, 170, 0.4);
      animation: rotateRing 15s linear infinite reverse;
    }
    
    .ring-3 {
      width: 60%;
      height: 60%;
      top: 20%;
      left: 20%;
      border-color: rgba(255, 107, 139, 0.4);
      animation: rotateRing 10s linear infinite;
    }
    
    @keyframes rotateRing {
      100% { transform: rotate(360deg); }
    }
    
    .sparkle {
      position: absolute;
      font-size: 20px;
      animation: sparkleFloat 3s ease-in-out infinite;
    }
    
    .sparkle-1 { top: 20%; left: 20%; animation-delay: 0s; }
    .sparkle-2 { top: 70%; right: 20%; animation-delay: 1s; }
    .sparkle-3 { bottom: 30%; left: 40%; animation-delay: 2s; }
    
    @keyframes sparkleFloat {
      0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.5; }
      50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
    }
    
    .processing-title {
      color: white;
      font-size: 1.8em;
      margin-bottom: 10px;
      font-weight: 700;
      background: linear-gradient(90deg, #6A5AF9, #00D4AA);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .processing-message {
      color: #aaa;
      margin-bottom: 30px;
      font-size: 1.1em;
    }
    
    .processing-progress {
      margin: 30px 0;
    }
    
    .progress-track {
      height: 6px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 3px;
      overflow: hidden;
      margin-bottom: 15px;
    }
    
    .progress-fill-animated {
      height: 100%;
      width: 30%;
      background: linear-gradient(90deg, #6A5AF9, #00D4AA);
      border-radius: 3px;
      animation: progressFill 2s ease-in-out infinite alternate;
    }
    
    @keyframes progressFill {
      0% { width: 30%; }
      100% { width: 70%; }
    }
    
    .progress-steps {
      display: flex;
      justify-content: space-between;
      color: #888;
      font-size: 0.9em;
    }
    
    .processing-details {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 20px;
      margin-top: 30px;
    }
    
    .detail-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 10px;
    }
    
    .detail-label {
      color: #aaa;
    }
    
    .detail-value {
      color: white;
      font-weight: 600;
    }
    
    .status-indicator {
      color: #FFAA2C;
      animation: statusPulse 2s infinite;
    }
    
    @keyframes statusPulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.6; }
    }
    
    .security-badge {
      background: linear-gradient(90deg, #00D4AA, #06b894);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.85em;
    }
    
    /* Payment Success Modal */
    .payment-success-modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.9);
      backdrop-filter: blur(20px);
      display: none;
      justify-content: center;
      align-items: center;
      z-index: 10001;
      animation: successModalAppear 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes successModalAppear {
      from {
        opacity: 0;
        transform: scale(0.8) rotate(-5deg);
      }
      to {
        opacity: 1;
        transform: scale(1) rotate(0deg);
      }
    }
    
    .success-modal-content {
      background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
      border-radius: 32px;
      padding: 60px 40px;
      width: 90%;
      max-width: 600px;
      text-align: center;
      border: 3px solid rgba(0, 212, 170, 0.3);
      box-shadow: 
        0 40px 100px rgba(0, 212, 170, 0.2),
        inset 0 0 100px rgba(106, 90, 249, 0.1);
      position: relative;
      overflow: hidden;
    }
    
    .success-modal-content::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: radial-gradient(circle at 30% 30%, rgba(106, 90, 249, 0.1) 0%, transparent 50%),
                  radial-gradient(circle at 70% 70%, rgba(0, 212, 170, 0.1) 0%, transparent 50%);
      z-index: 0;
    }
    
    .success-animation {
      position: relative;
      width: 180px;
      height: 180px;
      margin: 0 auto 40px;
      z-index: 1;
    }
    
    .success-checkmark {
      position: absolute;
      width: 100%;
      height: 100%;
      background: linear-gradient(135deg, #00D4AA, #06b894);
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      animation: checkmarkPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      transform: scale(0);
    }
    
    @keyframes checkmarkPop {
      0% { transform: scale(0) rotate(-180deg); }
      70% { transform: scale(1.1) rotate(10deg); }
      100% { transform: scale(1) rotate(0deg); }
    }
    
    .check-icon {
      font-size: 80px;
      color: white;
      font-weight: bold;
    }
    
    .confetti-container {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      pointer-events: none;
    }
    
    .success-title {
      color: white;
      font-size: 2.5em;
      margin-bottom: 30px;
      font-weight: 800;
      background: linear-gradient(90deg, #00D4AA, #6A5AF9);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: 0 5px 15px rgba(0, 212, 170, 0.3);
      animation: titleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
      0% { text-shadow: 0 5px 15px rgba(0, 212, 170, 0.3); }
      100% { text-shadow: 0 5px 30px rgba(106, 90, 249, 0.5); }
    }
    
    .success-details {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 20px;
      margin: 40px 0;
      z-index: 1;
      position: relative;
    }
    
    .success-detail-card {
      background: rgba(255, 255, 255, 0.05);
      border-radius: 16px;
      padding: 20px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      transition: transform 0.3s ease;
    }
    
    .success-detail-card:hover {
      transform: translateY(-5px);
      background: rgba(255, 255, 255, 0.08);
    }
    
    .detail-header {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
    }
    
    .detail-icon {
      font-size: 1.5em;
      margin-right: 10px;
    }
    
    .detail-title {
      color: #aaa;
      font-size: 0.9em;
      font-weight: 600;
    }
    
    .detail-value {
      color: white;
      font-size: 1.4em;
      font-weight: 700;
    }
    
    .success-message {
      color: #ddd;
      margin: 30px 0;
      font-size: 1.1em;
      line-height: 1.6;
    }
    
    .success-submessage {
      color: #aaa;
      font-size: 0.95em;
      margin-top: 10px;
    }
    
    .success-actions {
      display: flex;
      gap: 15px;
      margin-top: 40px;
      z-index: 1;
      position: relative;
    }
    
    .success-btn {
      flex: 1;
      padding: 18px 25px;
      border: none;
      border-radius: 12px;
      font-size: 1.1em;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    
    .primary-btn {
      background: linear-gradient(90deg, #00D4AA, #06b894);
      color: white;
      box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3);
    }
    
    .primary-btn:hover {
      transform: translateY(-3px);
      box-shadow: 0 12px 35px rgba(0, 212, 170, 0.4);
    }
    
    .secondary-btn {
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .secondary-btn:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: translateY(-3px);
    }
    
    .success-footer {
      margin-top: 30px;
      color: #888;
      font-size: 0.9em;
      z-index: 1;
      position: relative;
    }
    
    /* Toast Notifications */
    .payment-toast-container {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 10002;
      max-width: 350px;
    }
    
    .payment-toast {
      background: rgba(30, 30, 46, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 10px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: center;
      animation: toastSlideIn 0.3s ease, toastFadeOut 0.3s ease 2.7s forwards;
      border-left: 4px solid #6A5AF9;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .payment-toast.success {
      border-left-color: #00D4AA;
    }
    
    .payment-toast.error {
      border-left-color: #FF6B8B;
    }
    
    @keyframes toastSlideIn {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes toastFadeOut {
      to {
        opacity: 0;
        transform: translateX(100%);
      }
    }
    
    /* Enhanced Payment Section */
    #payment-section {
      transition: all 0.5s ease;
    }
    
    .payment-section-enhanced {
      animation: paymentSectionReveal 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes paymentSectionReveal {
      from {
        opacity: 0;
        transform: translateY(30px) scale(0.95);
      }
      to {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }
    
    /* Confetti Animation */
    .confetti-piece {
      position: absolute;
      width: 10px;
      height: 20px;
      background: linear-gradient(45deg, #00D4AA, #6A5AF9, #FF6B8B, #FFAA2C);
      opacity: 0;
      animation: confettiFall 3s ease-out forwards;
    }
    
    @keyframes confettiFall {
      0% {
        transform: translateY(-100px) rotate(0deg);
        opacity: 1;
      }
      100% {
        transform: translateY(1000px) rotate(720deg);
        opacity: 0;
      }
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
      .processing-modal-content,
      .success-modal-content {
        padding: 30px 20px;
        margin: 20px;
      }
      
      .success-details {
        grid-template-columns: 1fr;
      }
      
      .success-actions {
        flex-direction: column;
      }
      
      .success-title {
        font-size: 2em;
      }
    }
  `;
  document.head.appendChild(style);
}

/* ======================
   PAYMENT MODAL FUNCTIONS
======================= */
function showPaymentProcessingModal(show = true) {
  if (paymentProcessingModal) {
    if (show) {
      document.body.appendChild(paymentProcessingModal);
      paymentProcessingModal.style.display = 'flex';
      
      // Update status messages periodically
      const statusMessages = [
        "Verifying card details...",
        "Processing payment with bank...",
        "Securing transaction...",
        "Finalizing payment..."
      ];
      
      let currentStatus = 0;
      const statusElement = paymentProcessingModal.querySelector('.status-indicator');
      const progressInterval = setInterval(() => {
        if (statusElement && currentStatus < statusMessages.length) {
          statusElement.textContent = statusMessages[currentStatus];
          currentStatus++;
          
          // Update progress steps
          const steps = paymentProcessingModal.querySelectorAll('.step');
          steps.forEach((step, index) => {
            step.classList.toggle('active', index <= currentStatus);
          });
        }
      }, 1500);
      
      // Store interval for cleanup
      paymentProcessingModal._progressInterval = progressInterval;
    } else {
      if (paymentProcessingModal._progressInterval) {
        clearInterval(paymentProcessingModal._progressInterval);
      }
      paymentProcessingModal.style.display = 'none';
      if (paymentProcessingModal.parentNode) {
        paymentProcessingModal.parentNode.removeChild(paymentProcessingModal);
      }
    }
  }
}

function showPaymentSuccessModal(paymentData) {
  if (paymentSuccessModal) {
    document.body.appendChild(paymentSuccessModal);
    paymentSuccessModal.style.display = 'flex';
    
    // Update modal with payment data
    const amountEl = paymentSuccessModal.querySelector('#success-amount');
    const transactionEl = paymentSuccessModal.querySelector('#success-transaction');
    const timeEl = paymentSuccessModal.querySelector('#success-time');
    
    if (amountEl && paymentData && paymentData.amount) {
      amountEl.textContent = `₹${(paymentData.amount / 100).toFixed(2)}`;
    } else {
      amountEl.textContent = grandTotalEl.textContent ? `₹${grandTotalEl.textContent}` : '₹0.00';
    }
    
    if (transactionEl && paymentData && paymentData.id) {
      transactionEl.textContent = paymentData.id.substring(0, 12) + '...';
    }
    
    if (timeEl) {
      timeEl.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    }
    
    // Create confetti animation
    createConfettiAnimation();
    
    // Add event listeners to buttons
    const continueBtn = paymentSuccessModal.querySelector('#continue-to-confirmation');
    const receiptBtn = paymentSuccessModal.querySelector('#view-receipt');
    
    if (continueBtn) {
      continueBtn.addEventListener('click', () => {
        closePaymentSuccessModal();
        // Add smooth transition effect
        document.body.style.opacity = '0.7';
        document.body.style.transition = 'opacity 0.5s ease';
        
        setTimeout(() => {
          window.location.href = "/order-success/";
        }, 500);
      });
    }
    
    if (receiptBtn) {
      receiptBtn.addEventListener('click', () => {
        showToast("Receipt generation coming soon!", "info");
        // In real app, this would generate/download receipt
      });
    }
    
    // Auto-redirect after 15 seconds
    const autoRedirect = setTimeout(() => {
      closePaymentSuccessModal();
      window.location.href = "/order-success/";
    }, 15000);
    
    // Store timeout for cleanup
    paymentSuccessModal._autoRedirect = autoRedirect;
  }
}

function closePaymentSuccessModal() {
  if (paymentSuccessModal) {
    if (paymentSuccessModal._autoRedirect) {
      clearTimeout(paymentSuccessModal._autoRedirect);
    }
    paymentSuccessModal.style.display = 'none';
    if (paymentSuccessModal.parentNode) {
      paymentSuccessModal.parentNode.removeChild(paymentSuccessModal);
    }
  }
}

function createConfettiAnimation() {
  const confettiContainer = paymentSuccessModal.querySelector('.confetti-container');
  if (!confettiContainer) return;
  
  const colors = ['#00D4AA', '#6A5AF9', '#FF6B8B', '#FFAA2C', '#FFD166', '#118AB2'];
  
  for (let i = 0; i < 100; i++) {
    const confetti = document.createElement('div');
    confetti.className = 'confetti-piece';
    confetti.style.left = Math.random() * 100 + '%';
    confetti.style.width = Math.random() * 10 + 5 + 'px';
    confetti.style.height = Math.random() * 10 + 10 + 'px';
    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.animationDelay = Math.random() * 2 + 's';
    confetti.style.animationDuration = Math.random() * 2 + 2 + 's';
    
    confettiContainer.appendChild(confetti);
    
    // Remove after animation
    setTimeout(() => {
      if (confetti.parentNode === confettiContainer) {
        confettiContainer.removeChild(confetti);
      }
    }, 5000);
  }
}

function showToast(message, type = 'info', duration = 3000) {
  if (!toastContainer) return;
  
  const toast = document.createElement('div');
  toast.className = `payment-toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
    <span class="toast-message">${message}</span>
  `;
  
  toastContainer.appendChild(toast);
  
  setTimeout(() => {
    if (toast.parentNode === toastContainer) {
      toastContainer.removeChild(toast);
    }
  }, duration);
}

/* ======================
   ENHANCED PAYMENT FLOW
======================= */
payBtn.addEventListener("click", async () => {
  if (isProcessing) return;
  
  isProcessing = true;
  payBtn.disabled = true;
  
  // Show processing modal
  showPaymentProcessingModal(true);
  
  try {
    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: cardElement,
      }
    });

    // Close processing modal
    showPaymentProcessingModal(false);
    
    if (result.error) {
      showToast(`Payment failed: ${result.error.message}`, "error");
      paymentStatus.innerHTML = `<span class="status-indicator">Payment failed: ${result.error.message}</span>`;
      isProcessing = false;
      payBtn.disabled = false;
      return;
    }
    
    if (result.paymentIntent.status === "succeeded") {
      // Store payment result
      paymentResult = result.paymentIntent;
      
      // Show success modal with payment details
      showPaymentSuccessModal({
        amount: paymentResult.amount,
        id: paymentResult.id,
        currency: paymentResult.currency,
        created: paymentResult.created
      });
      
      // Update payment status
      paymentStatus.innerHTML = `<span class="status-indicator success">Payment successful!</span>`;
      
      // Mark payment section as completed
      paymentSection.classList.add('payment-completed');
      
      // Send success notification to server (optional)
      try {
        await apiFetch(`${API_BASE}/api/order-payment/payment-success/`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            payment_intent_id: paymentResult.id,
            status: paymentResult.status
          })
        });
      } catch (error) {
        console.log("Payment success notification failed, but payment was successful");
      }
    }
  } catch (error) {
    showPaymentProcessingModal(false);
    showToast("Payment processing error", "error");
    paymentStatus.innerHTML = `<span class="status-indicator error">Processing error</span>`;
    isProcessing = false;
    payBtn.disabled = false;
  }
});

/* ======================
   ENHANCED INITIALIZATION
======================= */
function initStripeUI() {
  paymentSection.style.display = "block";
  paymentSection.classList.add('payment-section-enhanced');
  
  // Add enhanced card element
  cardElement = elements.create("card", {
    style: {
      base: {
        fontSize: '18px',
        color: '#32325d',
        fontFamily: 'Comic Neue, cursive',
        '::placeholder': {
          color: '#aab7c4',
          fontSize: '16px'
        },
        iconColor: '#6A5AF9'
      },
      invalid: {
        color: '#FF6B8B',
        iconColor: '#FF6B8B'
      },
      complete: {
        color: '#00D4AA',
        iconColor: '#00D4AA'
      }
    },
    hidePostalCode: true,
    iconStyle: 'solid'
  });
  
  cardElement.mount("#card-element");
  
  // Enhanced event listeners for card element
  cardElement.on('focus', () => {
    document.getElementById('card-element').classList.add('StripeElement--focus');
    showToast("Enter your card details securely", "info", 2000);
  });
  
  cardElement.on('blur', () => {
    document.getElementById('card-element').classList.remove('StripeElement--focus');
  });
  
  cardElement.on('change', (event) => {
    const cardElementDiv = document.getElementById('card-element');
    if (event.error) {
      cardElementDiv.classList.add('StripeElement--invalid');
      cardElementDiv.classList.remove('StripeElement--complete');
      showToast(event.error.message, "error", 3000);
    } else if (event.complete) {
      cardElementDiv.classList.remove('StripeElement--invalid');
      cardElementDiv.classList.add('StripeElement--complete');
      showToast("Card details validated ✓", "success", 2000);
    } else {
      cardElementDiv.classList.remove('StripeElement--invalid');
      cardElementDiv.classList.remove('StripeElement--complete');
    }
  });
  
  paymentStatus.innerHTML = `<span class="status-indicator">Ready for payment</span>`;
}

/* ======================
   INITIAL SETUP
======================= */
document.addEventListener('DOMContentLoaded', () => {
  // Setup all UI components
  setupUIComponents();
  
  // Show initial loading
  showLoading(true);
  
  // Load checkout data
  setTimeout(async () => {
    try {
      const token = localStorage.getItem("access");
      if (!token) {
        authErrorEl.innerText = "Please login to continue checkout.";
        authErrorEl.style.display = 'block';
        showToast("Please login to continue", "warning");
        return;
      }

      const res = await apiFetch(`${API_BASE}/api/checkout/summary/`);
      
      if (!res.ok) {
        throw new Error("Unable to load cart");
      }

      const data = await res.json();
      renderCart(data);
      showToast("Ready for payment", "success");
    } catch (error) {
      showToast("Failed to load checkout", "error");
    } finally {
      showLoading(false);
    }
  }, 1000);
});

/* ======================
   ORIGINAL FUNCTIONS (UNMODIFIED)
======================= */
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

/* INIT */
loadCheckout();
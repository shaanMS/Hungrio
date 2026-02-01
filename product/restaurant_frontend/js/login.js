// async function login() 
// {
//   const username = document.getElementById("username").value;
//   const password = document.getElementById("password").value;
//   const captchaKey = document.getElementById("captcha_key").value;
//   const captchaValue = document.getElementById("captcha_value").value;

//   const res = await fetch("/api/auth/login/", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//   //   body: JSON.stringify({ username, password ,captchaKey, captchaValue})
//   // });
//     body: JSON.stringify({
//     username,
//     password,
//     captcha_key: captchaKey,
//     captcha_value: captchaValue,
//       })
//     };
//     if(!res.ok) 
//     {
//     alert("Login failed");
//     return;
//     }

//   const data = await res.json();

//   localStorage.setItem("access", data.access);
//   localStorage.setItem("refresh", data.refresh);
//   //window.location.href = "/";
  
//   setTimeout(() => {
//    window.location.replace("/");
// }, 100); 
// }
 

// async function loadCaptcha() {
//   const res = await fetch("/api/captcha/");
//   const data = await res.json();

//   document.getElementById("captcha-img").src = data.captcha_image;
//   document.getElementById("captcha_key").value = data.captcha_key;
// }

// window.onload = loadCaptcha;





async function login() {
  try {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const captchaKey = document.getElementById("captcha_key").value;
    const captchaValue = document.getElementById("captcha_value").value.trim();

    if (!username || !password || !captchaValue) {
      alert("All fields are required");
      return;
    }

    const res = await fetch("/api/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
        captcha_key: captchaKey,
        captcha_value: captchaValue,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      alert(err.detail || "Login failed");
      loadCaptcha(); // ❗ wrong captcha par refresh
      return;
    }

    const data = await res.json();

    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);

    window.location.replace("/");
  } catch (error) {
    console.error("Login error:", error);
    alert("Something went wrong");
  }
}

// async function loadCaptcha() {
//   try {
//     const res = await fetch("/api/captcha/");
//     if (!res.ok) {
//       throw new Error("Captcha load failed");
//     }

//     const data = await res.json();

//     document.getElementById("captcha-img").src = data.captcha_image;
//     document.getElementById("captcha_key").value = data.captcha_key;
//     document.getElementById("captcha_value").value = ""; // clear old input


//     // for dbugging
//     imgElement.onload = () => console.log("Captcha image loaded successfully!");
//     imgElement.onerror = () => console.log("Captcha image failed to load!");
//   } catch (error) {
//     console.error("Captcha error:", error);
//   }
// }

// window.addEventListener("load", loadCaptcha);




async function loadCaptcha() {
  try {
    console.log("Starting captcha load...");

    const res = await fetch("/api/captcha/");
    console.log("Captcha fetch status:", res.status);

    if (!res.ok) {
      const errText = await res.text();
      console.error("Captcha API failed:", res.status, errText);
      throw new Error("Captcha load failed");
    }

    const data = await res.json();
    console.log("Captcha data:", data);

    // Image element ko yahan se pakdo
    const img = document.getElementById("captcha-img");
    if (!img) {
      console.error("Captcha img element not found in DOM!");
      return;
    }

    // Src set karo
    img.src = data.captcha_image;
    console.log("Setting captcha src to:", data.captcha_image);

    // Hidden key set
    const keyInput = document.getElementById("captcha_key");
    if (keyInput) keyInput.value = data.captcha_key;

    // Clear input
    const valueInput = document.getElementById("captcha_value");
    if (valueInput) valueInput.value = "";

    // Debug load events (ab sahi variable use kar rahe)
    img.onload = () => {
      console.log("Captcha image LOADED successfully!");
    };

    img.onerror = (e) => {
      console.error("Captcha image FAILED to load:", e);
      // Fallback dikhane ke liye (test ke liye)
      img.src = "https://via.placeholder.com/280x80?text=Image+Load+Failed";
    };

  } catch (error) {
    console.error("Captcha loading error:", error);
  }
}

// Window load pe call
window.addEventListener("load", () => {
  console.log("Window fully loaded – calling loadCaptcha()");
  loadCaptcha();
});
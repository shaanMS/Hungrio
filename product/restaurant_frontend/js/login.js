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

async function loadCaptcha() {
  try {
    const res = await fetch("/api/captcha/");
    if (!res.ok) {
      throw new Error("Captcha load failed");
    }

    const data = await res.json();

    document.getElementById("captcha-img").src = data.captcha_image;
    document.getElementById("captcha_key").value = data.captcha_key;
    document.getElementById("captcha_value").value = ""; // clear old input


    // for dbugging
    imgElement.onload = () => console.log("Captcha image loaded successfully!");
    imgElement.onerror = () => console.log("Captcha image failed to load!");
  } catch (error) {
    console.error("Captcha error:", error);
  }
}

window.addEventListener("load", loadCaptcha);

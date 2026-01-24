async function login() 
{
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/auth/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) 
    {
    alert("Login failed");
    return;
    }

  const data = await res.json();

  localStorage.setItem("access", data.access);
  localStorage.setItem("refresh", data.refresh);
  //window.location.href = "/";
  
  setTimeout(() => {
   window.location.replace("/");
}, 100); 
}
 
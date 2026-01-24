async function login() 
{
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  alert('243546587342')
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
  alert('243546587342')
  setTimeout(() => {
  window.location.replace("/");
}, 100);
}
 
// static/js/api.js   ← yahi file sab jagah use hoti hai
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem("access");

    // Default headers + user override
    const headers = {
        "Content-Type": "application/json",
        ... (options.headers || {}),
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    console.log(`[apiFetch] → ${url}`);               // debug
    console.log("Headers sent:", headers);            // debug
    console.log("Token used:", !!token);              // debug

    const response = await fetch(url, {
        ...options,
        headers,
        credentials: "same-origin",                   // important for cookies if needed
    });

    if (!response.ok) {
        console.warn(`API failed: ${response.status} ${url}`);
    }

    return response;
}
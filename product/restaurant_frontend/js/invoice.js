// static/js/invoice.js
import { apiFetch } from "./api.js";

export async function fetchInvoice(orderId) {
    return apiFetch(`/api/invoices/${orderId}/stripe/download/`, {
        method: "GET",
    });
}

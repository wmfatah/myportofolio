function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");

    if (!container) {
        return;
    }

    const toast = document.createElement("div");

    toast.classList.add("toast");

    if (type === "success") {
        toast.classList.add("toast-success");
    } else {
        toast.classList.add("toast-error");
    }

    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(function () {
        toast.remove();
    }, 3000);
}
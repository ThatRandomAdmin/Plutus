document.addEventListener("DOMContentLoaded", () => {
    const errorPopup = document.getElementById("error-popup");
    if (!errorPopup) {
        return;
    }

    const text = errorPopup.textContent || "";
    if (!text.trim()) {
        return;
    }

    setTimeout(() => {
        errorPopup.remove();
    }, 5000);
});

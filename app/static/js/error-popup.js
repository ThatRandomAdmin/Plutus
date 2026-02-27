document.addEventListener("DOMContentLoaded", () => {
    const popupWrap = document.querySelector(".flash-popup-wrap");
    if (!popupWrap) {
        return;
    }

    setTimeout(() => {
        popupWrap.remove();
    }, 5000);
});

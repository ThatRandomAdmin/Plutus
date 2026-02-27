(() => {
    const tabContainer = document.querySelector(".transactions-shell[data-active-tab]");
    if (!tabContainer) {
        return;
    }

    const tabButtons = tabContainer.querySelectorAll(".bank-tab-button");
    const tabPanels = tabContainer.querySelectorAll(".bank-tab-panel");
    const initialTabId = tabContainer.dataset.activeTab || "upload-tab-panel";

    function openTab(tabId) {
        tabPanels.forEach((panel) => {
            panel.classList.toggle("is-active", panel.id === tabId);
        });

        tabButtons.forEach((button) => {
            button.classList.toggle("is-active", button.dataset.tab === tabId);
        });
    }

    tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
            openTab(button.dataset.tab);
        });
    });

    openTab(initialTabId);
})();

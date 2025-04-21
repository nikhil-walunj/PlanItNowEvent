function toggleMenu() {
    document.querySelector(".nav-links").classList.toggle("active");
}

document.addEventListener("DOMContentLoaded", function () {
    const bookingTable = document.querySelector(".booking-table");
    const bookSection = document.querySelector(".book-section");

    if (bookingTable) {
        const rowCount = bookingTable.querySelectorAll("tbody tr").length;

        if (rowCount > 6 && bookSection) {
            bookSection.classList.add("scrollable");
        }
    }
});

window.onload = function() {
    const scrollContainer = document.getElementById("event-scroll-container");
    scrollContainer.scrollTop = 0;
};


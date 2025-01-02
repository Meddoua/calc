document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll("input, select");
    inputs.forEach(input => {
        input.addEventListener("input", function() {
            if (input.checkValidity()) {
                input.classList.remove("invalid");
                input.classList.add("valid");
            } else {
                input.classList.remove("valid");
                input.classList.add("invalid");
            }
        });
    });
});
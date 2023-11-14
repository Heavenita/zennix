document.addEventListener("DOMContentLoaded", function() {
    const ipv4Inputs = document.querySelectorAll(".ipv4-input");
    ipv4Inputs.forEach(function(inputElement) {
        inputElement.addEventListener("input", function() {
            let inputValue = inputElement.value
                .replace(/[^\d.]/g, "");

            const octets = inputValue.split(".", 4);
            let formattedValue = "";

            for (let i = 0; i < octets.length; i++) {
                if (i > 0){
                    formattedValue += ".";
                }
                if (octets[i].length > 0) {
                    formattedValue += Math.min(parseInt(octets[i], 10), 255);
                }
            }

            inputElement.value = formattedValue;
        });
    });
});
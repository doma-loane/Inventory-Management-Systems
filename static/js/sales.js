document.addEventListener("DOMContentLoaded", function () {
    const scanProductCodeInput = document.getElementById("scanProductCode");
    const productNameField = document.getElementById("productName");
    const productPriceField = document.getElementById("productPrice");
    const productStockField = document.getElementById("productStock");

    // Fetch product details by product code
    scanProductCodeInput.addEventListener("input", function () {
        const productCode = this.value.trim();

        if (productCode) {
            fetch(`/get-product-by-code?code=${productCode}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        productNameField.innerText = data.name;
                        productPriceField.innerText = `₦${data.price}`;
                        productStockField.innerText = data.stock;
                    } else {
                        alert("Product not found.");
                        productNameField.innerText = "N/A";
                        productPriceField.innerText = "N/A";
                        productStockField.innerText = "N/A";
                    }
                })
                .catch(error => {
                    console.error("Error fetching product details:", error);
                    alert("An error occurred while retrieving product details.");
                });
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    console.log('JavaScript loaded');

    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-btn');
    const confirmButton = document.getElementById('confirm-btn');
    const nameInput = document.getElementById('name');
    const ocrStatus = document.getElementById('ocr-status');
    const addProductForm = document.getElementById("add-product-form");
    const successMessage = document.createElement("p");
    successMessage.id = "successMessage";
    successMessage.style.display = "none";
    successMessage.style.color = "green";
    addProductForm.parentNode.insertBefore(successMessage, addProductForm);

    const productCodeField = document.getElementById("product_code");
    const barcodeScanner = document.getElementById("scanner");

    // Access the camera and start the video stream
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error("Camera access error:", err);
            alert("Cannot access camera. Please check permissions.");
        });

    // Capture image from video when button is clicked
    captureButton.addEventListener('click', function() {
        ocrStatus.style.display = 'block';
        ocrStatus.textContent = "Scanning...";

        // Draw image on canvas
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas image to data URL
        const imageData = canvas.toDataURL('image/png');

        // Run OCR using Tesseract.js
        Tesseract.recognize(imageData, 'eng', { logger: m => console.log(m) })
            .then(({ data: { text } }) => {
                console.log("Extracted Text:", text);
                
                // Extract first line as product name
                const firstLine = text.trim().split('\n')[0];
                nameInput.value = firstLine;

                ocrStatus.textContent = "Scan complete!";
                setTimeout(() => { ocrStatus.style.display = 'none'; }, 2000);
            })
            .catch(err => {
                console.error("OCR Error:", err);
                ocrStatus.textContent = "Scan failed. Try again.";
                setTimeout(() => { ocrStatus.style.display = 'none'; }, 3000);
            });
    });

    // Confirm button allows user to finalize extracted text
    confirmButton.addEventListener('click', function() {
        alert("Product name confirmed: " + nameInput.value);
    });

    // Existing category and subcategory handling
    const categoryDropdown = document.getElementById("category");
    const subcategoryDiv = document.getElementById("subcategoryDiv");
    const subcategorySelect = document.getElementById("subcategory");
    const otherCategoryDiv = document.getElementById("otherCategoryDiv");

    categoryDropdown.addEventListener("change", function () {
        let selectedCategory = this.value;

        // Reset and hide subcategory and "Other" fields
        subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';
        subcategoryDiv.style.display = "none";
        otherCategoryDiv.style.display = "none";

        if (selectedCategory === "others") {
            // Show "Other" input field
            otherCategoryDiv.style.display = "block";
        } else {
            // Show subcategories dropdown and fetch subcategories dynamically
            subcategoryDiv.style.display = "block";

            fetch(`/get-subcategories?category_id=${selectedCategory}`)
                .then(response => response.json())
                .then(data => {
                    subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>'; // Reset dropdown

                    data.forEach(sub => {
                        let option = document.createElement("option");
                        option.value = sub.id;
                        option.textContent = sub.name;
                        subcategorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error("Error loading subcategories:", error));
        }
    });

    subcategorySelect.addEventListener("change", function () {
        if (this.value === "Other") {
            otherCategoryDiv.style.display = "block";
        } else {
            otherCategoryDiv.style.display = "none";
        }
    });

    // Handle form submission dynamically
    addProductForm.addEventListener("submit", async function(event) {
        event.preventDefault(); // Prevent default form submission

        let formData = new FormData(this);

        try {
            let response = await fetch(this.action, {
                method: "POST",
                body: formData,
            });

            let result = await response.json();

            if (result.success) {
                successMessage.innerText = result.message;
                successMessage.style.display = "block";

                // Optionally, clear the form
                this.reset();
            } else {
                alert("Failed to add product. Please try again.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        }
    });

    // Auto-fill product code when a barcode is scanned
    barcodeScanner.addEventListener("change", function (event) {
        let scannedCode = event.target.value.trim();

        if (scannedCode) {
            productCodeField.value = scannedCode; // Use scanned barcode
        } else {
            productCodeField.value = generateUniqueCode(); // Generate unique code
        }
    });

    // Function to generate a unique product code if no barcode is provided
    function generateUniqueCode() {
        return "P" + Math.random().toString(36).substr(2, 8).toUpperCase();
    }
});

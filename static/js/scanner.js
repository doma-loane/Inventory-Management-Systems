document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("scanner");
    const resultText = document.getElementById("result-text");
    const startButton = document.getElementById("start-scanner");

    let isScanning = false;

    startButton.addEventListener("click", () => {
        if (!isScanning) {
            startScanning();
        } else {
            stopScanning();
        }
    });

    function startScanning() {
        isScanning = true;
        resultText.innerText = "Scanning...";

        // Start QuaggaJS for barcode scanning with optimized resolution and locator settings
        Quagga.init({
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: { ideal: 640 },  // Lower width for faster processing
                    height: { ideal: 480 },
                    facingMode: "environment" // Back camera
                },
                target: video
            },
            locator: {
                halfSample: true,
                patchSize: "large" // Use "large" for better detection on curved surfaces
            },
            decoder: {
                readers: ["ean_reader", "code_128_reader", "upc_reader"] // Common retail barcodes
            }
        }, function (err) {
            if (err) {
                console.error("QuaggaJS Init Error:", err);
                return;
            }
            Quagga.start();
        });

        Quagga.onDetected((data) => {
            stopScanning();
            resultText.innerText = `Barcode: ${data.codeResult.code}`;
        });

        // Start ZXing for QR code scanning
        const codeReader = new ZXing.BrowserMultiFormatReader();
        codeReader.decodeFromVideoDevice(undefined, video, (result, err) => {
            if (result) {
                stopScanning();
                resultText.innerText = `QR Code: ${result.text}`;
            }
        });
    }

    function stopScanning() {
        isScanning = false;
        Quagga.stop();
    }

    // Function to compress images for upload efficiency
    function compressImage(canvas, quality = 0.6) {
        return canvas.toDataURL("image/jpeg", quality);
    }
});

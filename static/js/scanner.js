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

        // Start QuaggaJS for barcode scanning with optimized settings
        Quagga.init({
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: 640,
                    height: 480,
                    facingMode: "environment",
                    focusMode: "continuous"  // Ensures camera autofocus
                },
                target: video
            },
            locator: {
                halfSample: true,
                patchSize: "large"  // Use "large" for better detection on curved surfaces
            },
            decoder: {
                readers: [
                    "code_128_reader",
                    "ean_reader",
                    "ean_8_reader",
                    "upc_reader",
                    "qr_reader"  // Supports QR codes
                ],
                multiple: false  // Disable multiple barcode detection for faster scans
            }
        }, function (err) {
            if (err) {
                console.error("QuaggaJS Init Error:", err);
                return;
            }
            Quagga.start();
        });

        // Enhance image processing for better scans
        Quagga.onProcessed(function (result) {
            let canvas = Quagga.canvas.dom.overlay;
            let ctx = canvas.getContext("2d");
            ctx.filter = "contrast(150%) brightness(120%)";  // Improves barcode visibility
        });

        Quagga.onDetected((data) => {
            stopScanning();
            resultText.innerText = `Barcode: ${data.codeResult.code}`;
        });

        // Retry scan if no result is detected within 2 seconds
        setTimeout(() => {
            if (!Quagga.result) {
                console.log("Retrying scan...");
                Quagga.start();
            }
        }, 2000);
    }

    function stopScanning() {
        isScanning = false;
        Quagga.stop();
    }
});

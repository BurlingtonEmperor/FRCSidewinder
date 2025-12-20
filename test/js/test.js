// The Tesseract variable is now globally available
        const runOCR = async () => {
            const image = document.getElementById('sampleImage');
            // Create a worker and specify the language
            const worker = await Tesseract.createWorker('eng');

            // Run recognition on the image
            const ret = await worker.recognize(image);

            // Log the result text
            document.getElementById('outputText').textContent = ret.data.text;

            // Terminate the worker to free up resources
            await worker.terminate();
        };

        runOCR();
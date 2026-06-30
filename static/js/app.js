// ==========================================
// RegPilot Frontend
// app.js
// ==========================================



// ==========================================
// Notifications
// ==========================================

function showNotification(message, type = "success") {

    const notification = document.getElementById("notification");

    const icon = document.getElementById("notification-icon");

    const text = document.getElementById("notification-message");

    if (!notification || !icon || !text) return;

    text.innerHTML = message;

    switch (type) {

        case "success":
            icon.innerHTML = "✅";
            notification.style.background = "rgba(22,163,74,.95)";
            break;

        case "info":
            icon.innerHTML = "ℹ️";
            notification.style.background = "rgba(37,99,235,.95)";
            break;

        case "warning":
            icon.innerHTML = "⚠️";
            notification.style.background = "rgba(217,119,6,.95)";
            break;

        case "danger":
            icon.innerHTML = "❌";
            notification.style.background = "rgba(220,38,38,.95)";
            break;

        default:
            icon.innerHTML = "✅";
            notification.style.background = "rgba(22,163,74,.95)";
    }

    notification.classList.add("show");

    setTimeout(() => {

        notification.classList.remove("show");

    }, 2500);

}



// ==========================================
// Page Initialization
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

    initializeMarkdown();

    initializeCopyButton();

    initializePrintButton();

    initializeUploadArea();

});



// ==========================================
// Markdown Rendering
// ==========================================

function initializeMarkdown() {

    const container = document.getElementById("markdown-response");

    if (!container)
        return;

    marked.setOptions({
        breaks: true,
        gfm: true
    });

    const markdown = container.textContent.trim();

    container.innerHTML = marked.parse(markdown);

}



// ==========================================
// Copy Report
// ==========================================

function initializeCopyButton() {

    const copyButton = document.getElementById("copyBtn");

    if (!copyButton)
        return;

    copyButton.addEventListener("click", async () => {

        const report = document.getElementById("markdown-response").innerText;

        try {

            await navigator.clipboard.writeText(report);

            showNotification(
                "Report copied successfully",
                "success"
            );

            copyButton.innerHTML =
                '<i class="bi bi-check-circle-fill"></i> Copied!';

            copyButton.classList.remove("btn-light");

            copyButton.classList.add("btn-success");

            setTimeout(() => {

                copyButton.innerHTML =
                    '<i class="bi bi-clipboard"></i> Copy Report';

                copyButton.classList.remove("btn-success");

                copyButton.classList.add("btn-light");

            }, 2000);

        }

        catch (err) {

            console.error(err);

            showNotification(
                "Unable to copy report",
                "danger"
            );

        }

    });

}



// ==========================================
// Print Report
// ==========================================

function initializePrintButton() {

    const printBtn = document.getElementById("printBtn");

    if (!printBtn)
        return;

    printBtn.addEventListener("click", () => {

        const report = document.getElementById("markdown-response").innerHTML;

        const printWindow = window.open("", "_blank");

        printWindow.document.write(`

        <html>

        <head>

            <title>RegPilot Report</title>

            <link
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
                rel="stylesheet">

            <style>

                body{

                    padding:40px;
                    font-family:Arial,sans-serif;

                }

                h1,h2,h3{

                    margin-top:35px;

                }

                p{

                    line-height:1.8;

                }

                ul,ol{

                    margin-left:25px;

                }

                .report-title{

                    border-bottom:3px solid #198754;
                    margin-bottom:30px;
                    padding-bottom:10px;

                }

            </style>

        </head>

        <body>

            <div class="report-title">

                <h2>RegPilot AI Regulatory Report</h2>

                <p>

                    Generated using Amazon Nova

                </p>

            </div>

            ${report}

        </body>

        </html>

        `);

        printWindow.document.close();

        printWindow.focus();

        setTimeout(() => {

            printWindow.print();

            printWindow.close();

        }, 500);

    });

}

// ==========================================
// Smart Upload Experience
// ==========================================

function initializeUploadArea() {

    const fileInput = document.getElementById("fileInput");
    const dropZone = document.getElementById("dropZone");
    const uploadIcon = document.getElementById("uploadIcon");
    const uploadTitle = document.getElementById("uploadTitle");
    const uploadSubtitle = document.getElementById("uploadSubtitle");
    const uploadInfo = document.getElementById("uploadInfo");

    if (!fileInput) return;

    fileInput.addEventListener("change", function () {

        if (!this.files.length) return;

        const file = this.files[0];

        const size =
            file.size >= 1024 * 1024
                ? (file.size / (1024 * 1024)).toFixed(2) + " MB"
                : (file.size / 1024).toFixed(1) + " KB";

        dropZone.classList.add("ready");

        dropZone.animate(
            [
                { transform: "scale(.97)", opacity: .8 },
                { transform: "scale(1)", opacity: 1 }
            ],
            {
                duration:250,
                easing:"ease-out"
            }
        );

        uploadIcon.className =
            "bi bi-file-earmark-check-fill text-success";

        uploadTitle.textContent = file.name;  

        uploadSubtitle.innerHTML = `
        <span class="upload-status">
            <i class="bi bi-check-circle-fill"></i>
            Ready for AI Analysis
        </span>
        `;

        uploadInfo.innerHTML = `
        <div class="upload-size">
            File Size: <strong>${size}</strong>
        </div>

        <a href="#" id="changeFileHint">
            Change Selected File
        </a>
        `;

        const changeHint = document.getElementById("changeFileHint");
        changeHint.addEventListener("click", () => {

            fileInput.click();

        });

    });

}
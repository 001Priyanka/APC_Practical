// BlogHub Modern Client Scripts
document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5500);
    });

    // 2. Image upload preview for avatars and blog covers
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"], input[type="file"]#id_profile_image, input[type="file"]#id_cover_image');
    imageInputs.forEach(function (input) {
        input.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                // Check if preview element already exists
                let preview = input.parentElement.querySelector('.live-image-preview');
                if (!preview) {
                    preview = document.createElement('img');
                    preview.className = 'live-image-preview rounded img-thumbnail mt-2 shadow-sm d-block';
                    preview.style.maxHeight = '120px';
                    input.parentElement.appendChild(preview);
                }
                const reader = new FileReader();
                reader.onload = function (event) {
                    preview.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // 3. Form submit spinner prevention
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !form.checkValidity || (form.classList && form.classList.contains('was-validated'))) {
                // Let native validation proceed
                return;
            }
            if (submitBtn && !submitBtn.disabled) {
                // Add subtle opacity to show submission in progress
                submitBtn.classList.add('opacity-75');
            }
        });
    });
});

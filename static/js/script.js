// JavaScript for Patient Smart Card System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading spinner for file uploads
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                showLoading();
            }
        });
    });
});

function showLoading() {
    var loading = document.createElement('div');
    loading.className = 'loading';
    loading.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i></div>';
    document.body.appendChild(loading);
}

function hideLoading() {
    var loading = document.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
}

// Emergency access validation
function validateEmergencyAccess() {
    var patientId = document.getElementById('patient_id').value;
    var accessReason = document.getElementById('access_reason').value;
    
    if (!patientId.trim()) {
        alert('Please enter a valid Patient ID');
        return false;
    }
    
    if (!accessReason.trim() || accessReason.length < 10) {
        alert('Please provide a detailed reason for emergency access (minimum 10 characters)');
        return false;
    }
    
    showLoading();
    return true;
}

// Copy patient ID to clipboard
function copyPatientId(patientId) {
    navigator.clipboard.writeText(patientId).then(function() {
        showToast('Patient ID copied to clipboard!', 'success');
    }).catch(function() {
        showToast('Failed to copy Patient ID', 'error');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    var toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-' + (type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info') + ' border-0';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    var container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.appendChild(toast);
    document.body.appendChild(container);
    
    var bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    setTimeout(function() {
        container.remove();
    }, 5000);
}

// Confirm deletion
function confirmDelete(itemName) {
    return confirm('Are you sure you want to delete ' + itemName + '? This action cannot be undone.');
}

// Format date
function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Search functionality
function searchTable(tableId, searchInput) {
    var table = document.getElementById(tableId);
    var input = document.getElementById(searchInput);
    var filter = input.value.toUpperCase();
    var rows = table.getElementsByTagName('tr');
    
    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var found = false;
        
        for (var j = 0; j < cells.length; j++) {
            var cell = cells[j];
            if (cell) {
                var textValue = cell.textContent || cell.innerText;
                if (textValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        rows[i].style.display = found ? '' : 'none';
    }
}

// Print functionality
function printElement(elementId) {
    var element = document.getElementById(elementId);
    var printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <html>
            <head>
                <title>Print</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { padding: 20px; }
                    .no-print { display: none; }
                </style>
            </head>
            <body>
                ${element.innerHTML}
            </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

// File size validation
function validateFileSize(input, maxSizeMB = 10) {
    var maxSize = maxSizeMB * 1024 * 1024; // Convert MB to bytes
    
    if (input.files && input.files[0]) {
        var fileSize = input.files[0].size;
        
        if (fileSize > maxSize) {
            alert('File size must be less than ' + maxSizeMB + 'MB');
            input.value = '';
            return false;
        }
    }
    
    return true;
}

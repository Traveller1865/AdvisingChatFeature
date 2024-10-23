document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Error handling function
    function handleError(error, customMessage) {
        console.error('Error:', error);
        const errorMessage = customMessage || 'An unexpected error occurred. Please try again.';
        
        // Create and show error alert
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${errorMessage}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto dismiss after 5 seconds
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }, 5000);
        }
    }

    // FAQ Management
    window.editFaq = function(faqId) {
        const modal = document.getElementById('editFaqModal');
        if (!modal) return;

        fetch(`/admin/faq/${faqId}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch FAQ data');
                return response.json();
            })
            .then(data => {
                const form = document.getElementById('editFaqForm');
                if (!form) throw new Error('Edit form not found');

                form.querySelector('#editFaqId').value = data.id;
                form.querySelector('#editQuestion').value = data.question;
                form.querySelector('#editAnswer').value = data.answer;
                form.querySelector('#editCategory').value = data.category;
                form.action = `/admin/faq/${faqId}/edit`;

                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            })
            .catch(error => handleError(error, 'Failed to load FAQ details'));
    };

    window.deleteFaq = function(faqId) {
        if (confirm('Are you sure you want to delete this FAQ?')) {
            fetch(`/admin/faq/${faqId}/delete`, { 
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to delete FAQ');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    throw new Error(data.error || 'Failed to delete FAQ');
                }
            })
            .catch(error => handleError(error, 'Failed to delete FAQ'));
        }
    };

    // Advisor Management
    window.editAdvisor = function(advisorId) {
        const modal = document.getElementById('editAdvisorModal');
        if (!modal) return;

        fetch(`/admin/advisor/${advisorId}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch advisor data');
                return response.json();
            })
            .then(data => {
                const form = document.getElementById('editAdvisorForm');
                if (!form) throw new Error('Edit form not found');

                form.querySelector('#editAdvisorId').value = data.id;
                form.querySelector('#editName').value = data.name;
                form.querySelector('#editDepartment').value = data.department;
                form.querySelector('#editEmail').value = data.email;
                form.action = `/admin/advisor/${advisorId}/edit`;

                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            })
            .catch(error => handleError(error, 'Failed to load advisor details'));
    };

    window.deleteAdvisor = function(advisorId) {
        if (confirm('Are you sure you want to delete this advisor?')) {
            fetch(`/admin/advisor/${advisorId}/delete`, { 
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Failed to delete advisor');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    throw new Error(data.error || 'Failed to delete advisor');
                }
            })
            .catch(error => handleError(error, 'Failed to delete advisor'));
        }
    };

    // Form submission handlers
    const addFaqForm = document.getElementById('addFaqForm');
    const editFaqForm = document.getElementById('editFaqForm');
    const addAdvisorForm = document.getElementById('addAdvisorForm');
    const editAdvisorForm = document.getElementById('editAdvisorForm');

    [addFaqForm, editFaqForm, addAdvisorForm, editAdvisorForm].forEach(form => {
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);

                fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) throw new Error('Form submission failed');
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        throw new Error(data.error || 'Form submission failed');
                    }
                })
                .catch(error => handleError(error, 'Failed to submit form'));
            });
        }
    });
});

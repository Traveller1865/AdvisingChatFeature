document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on an admin page by looking for admin-specific elements
    const isAdminPage = document.querySelector('#addFaqModal') || document.querySelector('#addAdvisorModal');
    
    if (!isAdminPage) {
        return; // Exit if we're not on an admin page
    }

    // FAQ Management
    function editFaq(faqId) {
        if (!document.getElementById('editFaqModal')) return;
        
        fetch(`/admin/faq/${faqId}`)
            .then(response => response.json())
            .then(data => {
                const editForm = document.getElementById('editFaqForm');
                if (!editForm) return;

                document.getElementById('editFaqId').value = data.id;
                document.getElementById('editQuestion').value = data.question;
                document.getElementById('editAnswer').value = data.answer;
                document.getElementById('editCategory').value = data.category;
                editForm.action = `/admin/faq/${faqId}/edit`;
                const modal = new bootstrap.Modal(document.getElementById('editFaqModal'));
                modal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error fetching FAQ details');
            });
    }

    function deleteFaq(faqId) {
        if (confirm('Are you sure you want to delete this FAQ?')) {
            fetch(`/admin/faq/${faqId}/delete`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error deleting FAQ');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error deleting FAQ');
                });
        }
    }

    // Advisor Management
    function editAdvisor(advisorId) {
        if (!document.getElementById('editAdvisorModal')) return;

        fetch(`/admin/advisor/${advisorId}`)
            .then(response => response.json())
            .then(data => {
                const editForm = document.getElementById('editAdvisorForm');
                if (!editForm) return;

                document.getElementById('editAdvisorId').value = data.id;
                document.getElementById('editName').value = data.name;
                document.getElementById('editDepartment').value = data.department;
                document.getElementById('editEmail').value = data.email;
                editForm.action = `/admin/advisor/${advisorId}/edit`;
                const modal = new bootstrap.Modal(document.getElementById('editAdvisorModal'));
                modal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error fetching advisor details');
            });
    }

    function deleteAdvisor(advisorId) {
        if (confirm('Are you sure you want to delete this advisor?')) {
            fetch(`/admin/advisor/${advisorId}/delete`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error deleting advisor');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error deleting advisor');
                });
        }
    }

    // Make functions globally available
    window.editFaq = editFaq;
    window.deleteFaq = deleteFaq;
    window.editAdvisor = editAdvisor;
    window.deleteAdvisor = deleteAdvisor;

    // Form submission handlers
    const forms = document.querySelectorAll('#addFaqForm, #editFaqForm, #addAdvisorForm, #editAdvisorForm');
    forms.forEach(form => {
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);
                fetch(this.action, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert(data.error || 'An error occurred');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
                });
            });
        }
    });
});

// FAQ Management
function editFaq(faqId) {
    fetch(`/admin/faq/${faqId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editFaqId').value = data.id;
            document.getElementById('editQuestion').value = data.question;
            document.getElementById('editAnswer').value = data.answer;
            document.getElementById('editCategory').value = data.category;
            document.getElementById('editFaqForm').action = `/admin/faq/${faqId}/edit`;
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
    fetch(`/admin/advisor/${advisorId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('editAdvisorId').value = data.id;
            document.getElementById('editName').value = data.name;
            document.getElementById('editDepartment').value = data.department;
            document.getElementById('editEmail').value = data.email;
            document.getElementById('editAdvisorForm').action = `/admin/advisor/${advisorId}/edit`;
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

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
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

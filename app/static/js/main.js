// Form doğrulama ve diğer frontend işlevselliği

// DOM yüklendikten sonra çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    // Sepete ekleme formu varsa
    const sepetForm = document.getElementById('sepeteEkleForm');
    if (sepetForm) {
        sepetForm.addEventListener('submit', function(e) {
            const adet = document.getElementById('adet').value;
            if (adet <= 0) {
                e.preventDefault();
                alert('Adet en az 1 olmalıdır.');
            }
        });
    }

    // Kitap formu için ISBN kontrolü
    const isbnInput = document.getElementById('isbn');
    if (isbnInput) {
        isbnInput.addEventListener('blur', function() {
            const isbn = this.value;
            if (isbn && (isbn.length !== 10 && isbn.length !== 13)) {
                this.classList.add('is-invalid');
                
                // Zaten bir hata mesajı var mı kontrol et
                let feedback = this.nextElementSibling;
                if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                    feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    this.parentNode.appendChild(feedback);
                }
                
                feedback.textContent = 'ISBN 10 veya 13 karakter olmalıdır.';
            } else {
                this.classList.remove('is-invalid');
                const feedback = this.nextElementSibling;
                if (feedback && feedback.classList.contains('invalid-feedback')) {
                    feedback.remove();
                }
            }
        });
    }

    // Para birimini formatla (Fiyat alanları için)
    const formatCurrency = function(input) {
        if (!input) return;
        
        input.addEventListener('blur', function() {
            let value = this.value.replace(/[^\d.]/g, '');
            if (value) {
                value = parseFloat(value).toFixed(2);
                this.value = value;
            }
        });
    };

    const fiyatInput = document.getElementById('fiyat');
    if (fiyatInput) {
        formatCurrency(fiyatInput);
    }

    // Bootstrap tooltip'leri etkinleştir
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = Array.from(tooltipTriggerList).map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});
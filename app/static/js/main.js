// Form doğrulama ve diğer frontend işlevselliği

// DOM yüklendikten sonra çalışacak fonksiyonlar
document.addEventListener('DOMContentLoaded', function() {
    // Sayfa geçiş animasyonlarını yönet
    initPageTransitions();
    
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

    // Tablolar için satır animasyonları
    initTableRowAnimations();

    // Kart animasyonları
    initCardAnimations();
});

/**
 * Sayfa geçişlerini yönetir
 * Linklere tıklandığında sayfa geçişi animasyonu ekler
 */
function initPageTransitions() {
    // Tüm navigasyon bağlantılarını seç (navbar içindeki link ve dropdown itemlar)
    const navLinks = document.querySelectorAll('.navbar-nav a.nav-link:not(.dropdown-toggle), .dropdown-menu a.dropdown-item');
    
    // Ana içerik bölümü
    const contentContainer = document.querySelector('.page-transition');
    
    // Her link için event listener ekle
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Dropdown toggle linkleri ve PDF gibi dış bağlantıları atla
            if (link.classList.contains('dropdown-toggle') || link.getAttribute('target') === '_blank') {
                return;
            }
            
            // Mevcut sayfadaki linke tıklama durumunda animasyonu engelle
            const href = link.getAttribute('href');
            if (href === window.location.pathname) {
                return;
            }
            
            // Sayfa geçiş animasyonu için olayı engelle
            e.preventDefault();
            
            // Çıkış animasyonu
            contentContainer.style.animation = 'fadeOut 0.3s forwards';
            
            // Animasyon tamamlandıktan sonra sayfaya yönlendir
            setTimeout(() => {
                window.location.href = href;
            }, 300);
        });
    });
    
    // Sayfa yüklendiğinde giriş animasyonu
    if (contentContainer) {
        contentContainer.style.animation = 'pageTransition 0.5s forwards';
    }
}

/**
 * Tablo satırları için kademeli animasyon ekler
 */
function initTableRowAnimations() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        const tbody = table.querySelector('tbody');
        if (tbody) {
            const rows = tbody.querySelectorAll('tr');
            rows.forEach((row, index) => {
                row.style.opacity = '0';
                row.style.transform = 'translateY(10px)';
                row.style.animation = `fadeIn 0.3s ${index * 0.05}s forwards`;
            });
        }
    });
}

/**
 * Kartlar için kademeli animasyon ekler
 */
function initCardAnimations() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        if (!card.classList.contains('fade-in')) {
            card.classList.add('fade-in');
            card.style.animationDelay = `${index * 0.1}s`;
        }
    });
}
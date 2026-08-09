// Pequenas melhorias de UX para o site Observatório Socioambiental

document.addEventListener('DOMContentLoaded', () => {
    // Auto-fechar alertas após 6s
    document.querySelectorAll('.alert.alert-success, .alert.alert-info').forEach(el => {
        setTimeout(() => {
            try {
                const alert = bootstrap.Alert.getOrCreateInstance(el);
                alert.close();
            } catch (e) { /* bootstrap não disponível */ }
        }, 6000);
    });

    // Confirmação de envio de formulários de "excluir" no admin
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', e => {
            if (!confirm(form.dataset.confirm)) e.preventDefault();
        });
    });

    // Highlight do link ativo na navbar
    const path = window.location.pathname;
    document.querySelectorAll('.navbar .nav-link').forEach(link => {
        if (link.getAttribute('href') && path.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
            link.classList.add('active', 'fw-semibold');
        }
    });
});

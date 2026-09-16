// Progressive UX enhancements. The site remains usable if this file fails.
document.addEventListener('DOMContentLoaded', () => {
    const mainNav = document.getElementById('mainNav');
    if (mainNav && window.bootstrap) {
        mainNav.querySelectorAll('a:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992 && mainNav.classList.contains('show')) {
                    bootstrap.Collapse.getOrCreateInstance(mainNav).hide();
                }
            });
        });
    }

    document.querySelectorAll('.ux-quick-card, .gt-card, .news-card, .pub-card').forEach(card => {
        card.addEventListener('pointerdown', () => card.classList.add('is-pressed'));
        ['pointerup', 'pointerleave', 'pointercancel'].forEach(eventName => {
            card.addEventListener(eventName, () => card.classList.remove('is-pressed'));
        });
    });
});

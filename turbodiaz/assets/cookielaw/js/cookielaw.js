var Cookielaw = {
    createCookie: function (name, value, days) {
        var date = new Date(),
            expires = '';
        if (days) {
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    },

    getCookie: function (name) {
        var cookieName = name + "=";
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var c = cookies[i].trim();
            if (c.indexOf(cookieName) === 0) return c.substring(cookieName.length, c.length);
        }
        return null;
    },

    hideBanner: function () {
        var banner = document.getElementById('CookielawBanner');
        if (banner) {
            banner.style.display = 'none';
        }
    },

    handleConsent: function (action) {
        // Guardar la preferencia del usuario en una cookie
        this.createCookie('cookielaw_accepted', action, 365); // 365 días
        this.hideBanner();
    }
};

document.addEventListener("DOMContentLoaded", function () {
    // Verificar si la cookie ya existe
    if (!Cookielaw.getCookie('cookielaw_accepted')) {
        var banner = document.getElementById('CookielawBanner');
        if (banner) {
            banner.style.display = 'block';
        }

        // Configurar acciones de los botones
        var acceptButton = document.querySelector('.btn.accept');
        var rejectButton = document.querySelector('.btn.reject');

        if (acceptButton) {
            acceptButton.addEventListener('click', function (e) {
                e.preventDefault();
                Cookielaw.handleConsent('accepted');
            });
        }

        if (rejectButton) {
            rejectButton.addEventListener('click', function (e) {
                e.preventDefault();
                Cookielaw.handleConsent('rejected');
            });
        }
    } else {
        Cookielaw.hideBanner(); // Ocultar el banner si ya existe una cookie
    }
});

  
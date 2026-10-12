// Cookie lišta + Google Analytics (načte se až po souhlasu).
// ID měření předává build_site.py v atributu data-ga u <script>.
(function () {
  var GA_ID = document.currentScript.getAttribute('data-ga');
  var banner = document.getElementById('cookie-banner');

  function nactiGA() {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', GA_ID);
  }

  function cookieVolba(souhlas) {
    localStorage.setItem('cookie-souhlas', souhlas ? 'ano' : 'ne');
    banner.classList.remove('zobrazit');
    if (souhlas) nactiGA();
  }

  banner.querySelector('.prijmout').addEventListener('click', function () { cookieVolba(true); });
  banner.querySelector('.odmitnout').addEventListener('click', function () { cookieVolba(false); });

  var v = localStorage.getItem('cookie-souhlas');
  if (v === 'ano') { nactiGA(); }
  else if (v === null) { banner.classList.add('zobrazit'); }
})();

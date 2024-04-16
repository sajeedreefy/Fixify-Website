var animationDataUrl = "{% static 'images/Animation - 1709094674638.json' %}";

fetch(animationDataUrl)
    .then(response => response.json())
    .then(animationData => {
        var animationContainer = document.getElementById('lottie-container');
        var anim = lottie.loadAnimation({
            container: animationContainer,
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
        });
    })
    .catch(error => console.error('Error loading animation:', error));
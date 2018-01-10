$(document).ready(function () {

    $(".auth_buttons").click(function () {
        $(this).next().slideToggle();
    });
    $(".main_mnu_button").click(function () {
        $(".maian_mnu ul").slideToggle();
    });


    // туман эффект
    console.clear();

    canvasWidth = 1600;
    canvasHeight = 200;

    pCount = 0;


    pCollection = new Array();

    var puffs = 1;
    var particlesPerPuff = 2000;
    var img = 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/85280/smoke2.png';

    var smokeImage = new Image();
    smokeImage.src = img;

    for (var i1 = 0; i1 < puffs; i1++) {
        var puffDelay = i1 * 1500; //300 ms between puffs

        for (var i2 = 0; i2 < particlesPerPuff; i2++) {
            addNewParticle((i2 * 50) + puffDelay);
        }
    }


    draw(new Date().getTime(), 3000)


    function addNewParticle(delay) {

        var p = {};
        p.top = canvasHeight;
        p.left = randBetween(-200, 800);

        p.start = new Date().getTime() + delay;
        p.life = 8000;
        p.speedUp = 30;


        p.speedRight = randBetween(0, 20);

        p.rot = randBetween(-1, 1);
        p.red = Math.floor(randBetween(0, 255));
        p.blue = Math.floor(randBetween(0, 255));
        p.green = Math.floor(randBetween(0, 255));


        p.startOpacity = .3
        p.newTop = p.top;
        p.newLeft = p.left;
        p.size = 200;
        p.growth = 10;

        pCollection[pCount] = p;
        pCount++;


    }

    function draw(startT, totalT) {
        //Timing
        var timeDelta = new Date().getTime() - startT;
        var stillAlive = false;

        //Grab and clear the canvas
        var c = document.getElementById("myCanvas");
        var ctx = c.getContext("2d");
        ctx.clearRect(0, 0, c.width, c.height);
        c.width = c.width;

        //Loop through particles
        for (var i = 0; i < pCount; i++) {
            //Grab the particle
            var p = pCollection[i];

            //Timing
            var td = new Date().getTime() - p.start;
            var frac = td / p.life

            if (td > 0) {
                if (td <= p.life) {
                    stillAlive = true;
                }

                //attributes that change over time
                var newTop = p.top - (p.speedUp * (td / 1000));
                var newLeft = p.left + (p.speedRight * (td / 1000));
                var newOpacity = Math.max(p.startOpacity * (1 - frac), 0);

                var newSize = p.size + (p.growth * (td / 1000));
                p.newTop = newTop;
                p.newLeft = newLeft;

                //Draw!
                ctx.fillStyle = 'rgba(150,150,150,' + newOpacity + ')';
                ctx.globalAlpha = newOpacity;
                ctx.drawImage(smokeImage, newLeft, newTop, newSize, newSize);
            }
        }


        //Repeat if there's still a living particle
        if (stillAlive) {
            requestAnimationFrame(function () {
                draw(startT, totalT);
            });
        }
        else {
            clog(timeDelta + ": stopped");
        }
    }

    function randBetween(n1, n2) {
        var r = (Math.random() * (n2 - n1)) + n1;
        return r;
    }

    function randOffset(n, variance) {
        //e.g. variance could be 0.1 to go between 0.9 and 1.1
        var max = 1 + variance;
        var min = 1 - variance;
        var r = Math.random() * (max - min) + min;
        return n * r;
    }

    function clog(s) {
        console.log(s);
    }


    //Таймер обратного отсчета
    //Документация: http://keith-wood.name/countdown.html
    //<div class="countdown" date-time="2015-01-07"></div>
    var austDay = new Date($(".countdown").attr("date-time"));
    $(".countdown").countdown({until: austDay, format: 'yowdHMS'});

    //Попап менеджер FancyBox
    //Документация: http://fancybox.net/howto
    //<a class="fancybox"><img src="image.jpg" /></a>
    //<a class="fancybox" data-fancybox-group="group"><img src="image.jpg" /></a>
    $(".fancybox").fancybox();

    //Навигация по Landing Page
    //$(".top_mnu") - это верхняя панель со ссылками.
    //Ссылки вида <a href="#contacts">Контакты</a>
    $(".top_mnu").navigation();

    //Добавляет классы дочерним блокам .block для анимации
    //Документация: http://imakewebthings.com/jquery-waypoints/
    $(".block").waypoint(function (direction) {
        if (direction === "down") {
            $(".class").addClass("active");
        } else if (direction === "up") {
            $(".class").removeClass("deactive");
        }
        ;
    }, {offset: 100});

    //Плавный скролл до блока .div по клику на .scroll
    //Документация: https://github.com/flesler/jquery.scrollTo
    $("a.scroll").click(function () {
        $.scrollTo($(".div"), 800, {
            offset: -90
        });
    });

    //Каруселька
    //Документация: http://owlgraphic.com/owlcarousel/
    var owl = $(".carousel");
    owl.owlCarousel({
        items: 3,
        autoHeight: true
    });
    owl.on("mousewheel", ".owl-wrapper", function (e) {
        if (e.deltaY > 0) {
            owl.trigger("owl.prev");
        } else {
            owl.trigger("owl.next");
        }
        e.preventDefault();
    });
    $(".next_button").click(function () {
        owl.trigger("owl.next");
    });
    $(".prev_button").click(function () {
        owl.trigger("owl.prev");
    });

    //Кнопка "Наверх"
    //Документация:
    //http://api.jquery.com/scrolltop/
    //http://api.jquery.com/animate/
    $("#top").click(function () {
        $("body, html").animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    //Аякс отправка форм
    //Документация: http://api.jquery.com/jquery.ajax/
    $("#callback").submit(function () {
        $.ajax({
            type: "GET",
            url: "mail.php",
            data: $("#callback").serialize()
        }).done(function () {
            alert("Спасибо за заявку!");
            setTimeout(function () {
                $.fancybox.close();
            }, 1000);
        });
        return false;
    });

});
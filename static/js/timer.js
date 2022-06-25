var timer = new easytimer.Timer();
$('.buttons-wrapper .startButton').click(function () {
    timer.start();
});

$('.buttons-wrapper .pauseButton').click(function () {
    timer.pause();
});

$('.buttons-wrapper .resetButton').click(function () {
    timer.reset();
    timer.stop();
});

timer.addEventListener('secondsUpdated', function (e) {
    $('.time-values').html(timer.getTimeValues().toString());
});

timer.addEventListener('started', function (e) {
    $('.time-values').html(timer.getTimeValues().toString());
});

timer.addEventListener('reset', function (e) {
    $('.time-values').html(timer.getTimeValues().toString());
});
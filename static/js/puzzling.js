/* Indicates how many characters have been typed. */
function countChars(textarea) {
    var text = textarea.value;
    var len = text.length;
    var counter = document.getElementById('counter');
    if (len < 100) {
        counter.textContent = len + '/100';
    } else {
        var locale = getCurrentLocale();
        counter.innerHTML = DICTIONARIES[locale]['Above maximum'] + ' <span style="color: red;">' + len + '</span>' + '/2000';
    }
}


 function display() {
    window.print();
 }


















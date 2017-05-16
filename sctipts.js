
function toggle(target) {
    var x = document.getElementById(target);
    console.log(x.style.display);
    if (x.style.display === 'none') {
        x.style.display = 'initial';
    } else {
        x.style.display = 'none';
    }
}

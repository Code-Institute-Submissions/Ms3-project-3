  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    // datepicker, output format, show clear button, Internationalization options:
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
  });

// makes the navbar to disappear when scroll up and to apper when scroll down
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-70px";
  }
}
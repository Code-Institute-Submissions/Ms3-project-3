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


function sendMail(contactForm) {
    emailjs.send("service_fyyclkx","Linus", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.email.value,
        "message": contactForm.msg.value
    })
    .then(
        function(response) {
            console.log("success", response);
        },
        function(error) {
            console.log("error", error);
        })
    return false;
}
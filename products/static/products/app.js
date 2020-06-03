
$(document).ready(function() {
    /*
    handling live preview during create hunt
 */

    // funcs to preview photo after upload.
    var reader = new FileReader();
    reader.onload = function (e) {
        $('#preview-photo').attr('src', e.target.result);
    }

   function readURL(input) {
        if (input.files && input.files[0]) {
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_image_load").change(function(){
        readURL(this);
    });


    var arrival;
    var depart;
    var duration;

    // simple function return genetive forms for the amount of days or nights
    function genetiveForms(count){
        var dayForm = "";
        var nightForm = "";
        amount = count;
        if (amount === 0) {
            dayForm = "dni"
            nightForm = "nocy"
        }
        else if (amount === 1) {
            dayForm = "dzień";
            nightForm = "noc";

        }
        else if (amount < 5 && amount > 1) {
            dayForm = "dni";
            nightForm = "noce";
        }

        else if (amount > 21 && amount % 10 > 1 && amount % 10 < 5) {
            dayForm = "dni";
            nightForm = "noce";
        }
        else {
            dayForm = "dni";
            nightForm = "nocy";
        }
        return [dayForm, nightForm];
    }

    function callbackFunc(response) {
    // do something with the response. function to support ajax call in id_flight_url
    console.log(response);
}
    // changing preview snippet data
    $("#id_title, #id_body, .datepicker, #id_flight_url, #id_price_amount, #id_airline").change(function(){
        var new_text = $(this).val();

        console.log('second')

      switch(this.id) {
        case
            'id_title': $('#pTitle').text(new_text);
            break;
        case
            'id_body': $('#pBody').text(new_text);
            break;
        case
            'id_flight_url': $('#pPrice').attr("href", new_text);
            //  setting csrf (taken from here: https://docs.djangoproject.com/en/3.0/ref/csrf/)
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                       xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            // passing url tu django view. just for run scrapy in python
            $.ajax({
               type: "POST",
               url: "../scrap_flights/",
                // passing param to django views
               data: { param: new_text },
               success: callbackFunc
            });
            break;
        case
            'id_depart_on':
                $('#pDepartDate').text(new_text);
                //var n = new_text.replace(".", "");
                depart = moment(new_text, "DD-MM-YYYY");

                if (arrival >= depart) {
                    nights = arrival.diff(depart, "days");
                    duration = nights + 1

                    var dayForm = genetiveForms(duration)[0];
                    var nightForm = genetiveForms(nights)[1];

                     $('#pDuration').text(duration + " " + dayForm + " i " + nights + " " + nightForm);
                }
                break;
        case
            'id_arrive_on':
                // var l = new_text.replace(".", "");
                arrival = moment(new_text, "DD-MM-YYYY");

                if (depart <= arrival) {
                    nights = arrival.diff(depart, "days");
                    duration = nights + 1;

                    var dayForm = genetiveForms(duration)[0];
                    var nightForm = genetiveForms(nights)[1];

                     $('#pDuration').text(duration + " " + dayForm + " i " + nights + " " + nightForm);
                }
                break;
        case
            'id_price_amount': $('#pPrice').text(new_text+" PLN");
            break;
        case
            'id_airline': $('#pAirline').text(new_text);
            break;

      }
    });

    // add calendar widget to DateFields
    $.datepicker.regional['pl'] = {
                closeText: 'Zamknij',
              prevText: '&#x3c;Poprzedni',
                nextText: 'Następny&#x3e;',
                currentText: 'Dziś',
                monthNames: ['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec',
                'Lipiec','Sierpień','Wrzesień','Pażdziernik','Listopad','Grudzień'],
                monthNamesShort: ['Sty','Lu','Mar','Kw','Maj','Cze',
                'Lip','Sie','Wrz','Pa','Lis','Gru'],
                dayNames: ['Niedziela','Poniedziałek','Wtorek','Środa','Czwartek','Piątek','Sobota'],
                dayNamesShort: ['Nie','Pn','Wt','Śr','Czw','Pt','So'],
                dayNamesMin: ['N','Pn','Wt','Śr','Cz','Pt','So'],
                weekHeader: 'Tydz',
                dateFormat: 'dd.mm.yy',
                firstDay: 1,
                isRTL: false,
                showMonthAfterYear: false,
               yearSuffix: ''};

    $.datepicker.setDefaults($.datepicker.regional['pl']);

    // calendar widget
    $(".datepicker").datepicker({

               // minDate: 2,
               // maxDate: "+10D",
               // isRTL: true
    });
    console.log('foto7');

});

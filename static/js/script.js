$(document).ready(function(){
    var userId = $('#userId').attr('value');
    $.getJSON('/api/profiles/'+userId+'/', function(data){
        $('#numb_CAPS').text(data.profile_wallet.wallet);
    });
});
$(document).ready(function(){
    $("#soundcloudButton").click(function () {
        $('#itunes').hide();
        $('#youtube').hide();
        $('#soundcloud').show();
        switchButtonsOff();
        $('#soundcloudButton').removeClass('btn-secondary')
        $('#soundcloudButton').addClass('btn-primary')
        
    });
    $("#itunesButton").click(function () {
        $('#soundcloud').hide();
        $('#youtube').hide();
        $('#itunes').show();
        switchButtonsOff();
        $('#itunesButton').removeClass('btn-secondary')
        $('#itunesButton').addClass('btn-primary')
    });
    $("#youtubeButton").click(function () {
        $('#itunes').hide();
        $('#soundcloud').hide(); 
        $('#youtube').show(); 
        switchButtonsOff();
        $('#youtubeButton').removeClass('btn-secondary')
        $('#youtubeButton').addClass('btn-primary')
    });

    function switchButtonsOff(){
        $('#youtubeButton').removeClass('btn-primary')
        $('#itunesButton').removeClass('btn-primary')
        $('#soundcloudButton').removeClass('btn-primary')
        if($('#youtubebutton').hasClass('btn-secondary') ==  false){
            $('#youtubeButton').addClass('btn-secondary')
        }
        if($('#itunesButton').hasClass('btn-secondary') ==  false){
            $('#itunesButton').addClass('btn-secondary')
        }
        if($('#soundcloudButton').hasClass('btn-secondary') ==  false){
            $('#soundcloudButton').addClass('btn-secondary')
        }
    }
});

// Init All Components
function initAll(context) {

    $.ajaxSetup ({cache: false}); 

    initStars(context);
    initLightBox(context);
    initCarrousel(context);
    initTabs(context);
    initTags(context);
    initPaginators(context);
    initTooltips(context);
    initActions(context);
    // Other init components
    initDatepicker(context);
    initSearch(context);
    initAutoTranslate(context);
    initSlider(context);
}

function initSlider(context){
    $(".slider-range-years").slider({
        range: true,
        min: 1950,
        max: 2012,
        values: [ 1950, 2012 ],
        slide: function( event, ui ) {
            var label = language['range-from-to'];
            label = label.replace('{fromyear}', ui.values[0]);
            label = label.replace('{toyear}', ui.values[1]);

            $(this).siblings('.slider-range-years-label').html(label);
            $(this).siblings('.slider-range-years-from').val(ui.values[0]);
            $(this).siblings('.slider-range-years-to').val(ui.values[1]);
        }
    });
}

function initPaginators(context) {
    $(".expandpaginator").each(function(){
        var select = $(this);
        var option = $(this).children("option");
        var max = option.attr('value');
        var selected = option.html();

        option.html(max);

        for (i = max - 1; i > 0; i--) {
            var optionc = option.clone();
            optionc.attr('value', i);
            if (i == selected){
                optionc.attr('selected', 'selected');
            }
            optionc.html(i);
            select.prepend(optionc);
        }
    });
}

function initDatepicker(context) {
    $(".datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: '1910:2000',
        dateFormat: 'yy-mm-dd'
    });

}

function initSearch(context) {
    $("#search #submitimg").click(function (){
        $('#searchform').submit();
    });
    
    $("#search input").keypress(function(e){
        if(e.which == 13){
            $('#searchform').submit();
        }
    });

}

function initStars(context) {
    var ratehook = 'rateme'; 
    var rateform = 'rate'; 
    var ratestars = 10; // Numero de estrellas

    $("." + ratehook).each(function(){
            var $link = $(this).children("a");
            var rateurl = $link.attr('href');
            var params = getUrlVars(rateurl);
            var $caption = $('<span class="ratelabel"/>');

            // Creamos el formulario generico    
            var $genstars = $('<form method="post"><select name="vote" class="tooltify"></select></form>');
            $genstars.addClass(rateform);
            $genstars.addClass('tooltify');
            for (var value=1; value <= ratestars; value++) {
                var $row = $('<option value="' + value + '"' + (params['test']==value?' selected="selected"':'') +'>' + value + '</option>'); // select.val() doesnt work :(
                $row.appendTo($genstars.children());
            }

            var $genstarscloned = $genstars.clone();
            $genstarscloned.attr('action', rateurl);
            $($genstarscloned).appendTo(this);
            //$($caption).appendTo(this);

            // Creamos las estrellas mediante el formulario clonado anteriormente
            $(this).children("." + rateform ).stars({
                    inputType: "select",
                    showTitles: true,
		            cancelTitle: language['cancel-rating'],
                    //captionEl: $caption,
                    callback: function(ui, type, value) {
                        $.ajax({ type: 'GET', url: ui.$form.attr('action'), data: {'vote':value}});    

                        if (permissions['facebook_id']!=null && permissions['facebook_post_votes']=='1' && value > 0){

                            var img = '';
                            var title = '';
                            var url = 'http://www.likees.org';

                            var item = ui.element.parents('.rowitem').get(0);
                            
                            if (item != undefined){
                                img = $(item).find('.poster').attr('src');
                                title = $(item).find('.poster').attr('alt');
                                url = url + $(item).find('.title, .stitle').attr('href');
                            }
                            
                            var item = ui.element.parents('.main-item').get(0);
                            if (item != undefined){
                                img = $("meta[property='og:image']").attr('content');
                                title = $("meta[property='og:title']").attr('content');
                                url = url + $("meta[property='og:url']").attr('content').substring(21);
                            }

                            var message = language['facebook-voted'];
                            message = message.replace('{movie}', title);
                            message = message.replace('{value}', value);

                            check_status_and_publish_facebook(message, img, url);
                        }

                        // Escondemos el item correspondiente
                        ui.$form.parents(".fadewishitem").fadeOut(1500, function(){});
                    }
            });
    });

}

function initLightBox(context) {
    $('.trailerdetail').colorbox({opacity:0.8, width:640, height:390});
    $('.lightbox').colorbox({opacity:0.5});
}

function initCarrousel(context){
    $('.carousel').jcarousel({
        auto: 3,
        animation: 'slow',
        wrap: 'circular',
        easing: 'swing',
        initCallback: mycarousel_initCallback
    });
}

function mycarousel_initCallback(carousel)
{
        // Disable autoscrolling if the user clicks the prev or next button.
    carousel.buttonNext.bind('click', function() {
            carousel.startAuto(0);
            });

    carousel.buttonPrev.bind('click', function() {
            carousel.startAuto(0);
            });

    // Pause autoscrolling if the user moves with the cursor over the clip.
    carousel.clip.hover(function() {
            carousel.stopAuto();
            }, function() {
            carousel.startAuto();
            });
};


function initTabs(context){
    $('#tabs').tabs();
}

function initTooltips(context){
    $('.tooltify a, .tooltify img, a.tooltify', context).tipsy({gravity: 's', fade: true});
    $('.tooltify-user a, .tooltify-user img', context).tipsy({html: true, gravity: 's', fade: true});
}

function connectFacebook() {
        session = FB.getSession();
        
        if (session) {
            // user successfully logged in
            $.ajax({url: "/accounts/add_facebook_id/?id="+session.uid});
            FB.api('/me', function(response) {
                var birthdate_fb = response.birthday;
                var myDateParts = birthdate_fb.split("/");
                var birth = myDateParts[2] + "-" + myDateParts[0] +"-" + myDateParts[1];
                $.ajax({url: "/accounts/update_profile/?name="+response.first_name+"&surname="+response.middle_name + " " +response.last_name+"&gender="+response.gender+"&birthdate="+birth});
            });
        } else {
            $.ajax({url: "/accounts/del_facebook_id/"});
        }

}


function initActions(context){
   $('a.favs-action', context).click(function(){
        var ret = swapAction($(this), 'favs');
        
        if (!ret && permissions['facebook_id']!=null && permissions['facebook_post_faves']=='1'){

            var img = '';
            var title = '';
            var url = 'http://www.likees.org';

            var item = $(this).parents('.rowitem').get(0);

            if (item != undefined){
                img = $(item).find('.poster').attr('src');
                title = $(item).find('.poster').attr('alt');
                url = url + $(item).find('.title, .stitle').attr('href');
            }

            var item = $(this).parents('.main-item').get(0);
            if (item != undefined){
                img = $("meta[property='og:image']").attr('content');
                title = $("meta[property='og:title']").attr('content');
                url = url + $("meta[property='og:url']").attr('content').substring(21);
            }

            var message = language['facebook-faves'];
            message = message.replace('{movie}', title);

            check_status_and_publish_facebook(message, img, url);
        }

        return false;
    });
    $('a.wishlist-action', context).click(function(){
        var count = $('#iwhanttowatchcount').html();
        
        if (typeof(count) === 'undefined' || count.length == 0){
            count = 0;
        } 
        
        if(swapAction($(this), 'wishlist')){
            count = parseInt(count) - 1;
        } else {
            count = parseInt(count) + 1;
        }

        $('#iwhanttowatchcount').html(count);

        return false;
    });
    $('a.ignore-action', context).click(function(){
        swapAction($(this), 'ignore');
        return false;
    });
    $('a.ignore-fade-action', context).click(function(){
        swapAction($(this), 'ignore');
        
        // Escondemos el item correspondiente
        $(this).parents(".fadeignoreitem").fadeOut(1500, function(){});
        
        return false;
    });
    $('a.friend-action', context).click(function(){
        swapAction($(this), 'friend');
        return false;
    });
    $('a.list-fade-action', context).click(function(){
        swapAction($(this), 'tag');
        
        // Escondemos el item correspondiente
        $(this).parents(".fadelistitem").fadeOut(1500, function(){});
        
        return false;
    });
    $('a.rows-action', context).click(function(){
        $('div.thumbitem').addClass('rowitem');
        $('div.rowitem').removeClass('thumbitem');
        return false;
    });
    $('a.thumbs-action', context).click(function(){
        $('div.rowitem').addClass('thumbitem');
        $('div.thumbitem').removeClass('rowitem');
        return false;
    });
    $('a.options-action', context).click(function(){
       
        var bar = $('#options'); 

        if (bar.is('.opened')) {
            bar.slideUp("slow");
            bar.removeClass('opened');
        } else {
            bar.slideDown("slow");
            bar.addClass('opened');
        }

        return false;
    });
    $('.pagination .selpage', context).change(function(){
        $(this).submit();
        return false;
    });
    $('.item-lists a.create-tag-action', context).click(function(){
        var reply = prompt(language['create-tag-prompt'], "");
        
        if (typeof(reply) === 'undefined' || reply == null || reply.length == 0) {
            return false;
        }

        var url = $(this).attr('href');
        var pdata = {'value':reply};
            
        $(".item-lists .taglist").prepend('<li id="listid-' + reply + '"class="loading">' + reply + '</li>');            

        $.post(url, pdata, function(data) {
            $("#listid-" + reply).removeClass('loading');
            $("#listid-" + reply).addClass('checked');
        }); 
        
        return false;
    });
    $('.item-lists li', context).click(function(){

        var url = $('a.create-tag-action').attr('href');
        var tag = $(this).html();

        if ($(this).is('.checked')){
            url = url.replace('add','delete');
        }
        
        var pdata = {'value':tag};
        
        $.post(url, pdata, function(data) {
            $('.item-lists li#listid-' + tag).toggleClass('unchecked');
            $('.item-lists li#listid-' + tag).toggleClass('checked');
        }); 
    
        return false;
    });
}

function swapAction (obj, type){
    var url = obj.attr('href'); 
    var label = '';
    var ret = false;

    $.post(url, function(data) {
    }); 

    if (url.indexOf('add') > 0){
        url = url.replace('add','delete');
        label = language[type + '-del'];
        ret = false;
        obj.addClass('swapon');
    }else{
        url = url.replace('delete','add');
        label = language[type + '-add'];
        ret = true;
        obj.removeClass('swapon');
    }
   
    // No es del todo correcto hacer esto sin verificar que el post ha ido bien    
    obj.attr('href', url); 
    obj.children('span').html(label); 

    return ret;
}

function initTags(context){
    // Cargar las listas del usuario
    $('.tagit').tagit({
            availableTags: ["c++", "java", "php", "coldfusion", "javascript", "asp", "ruby", "python", "c", "scala", "groovy", "haskell", "perl"]
    });
}

function initAutoTranslate(context){

    var labelTranslator = ' (Google Translate)';

    $('.autotranslate').each(function(){
       
        var obj = $(this);
        var tolang = $('html').attr('lang');
        
        google.language.detect(obj.html(), function(result) {

            var fromlang = result['language'];

            if (fromlang != tolang){
                google.language.translate(obj.html(), fromlang, tolang, function(result) {
                    if (result.translation) {
                    obj.html(result.translation + labelTranslator);
                }
                });
            }
        });
    })


}


function getUrlVars(href)
{
    var vars = [], hash;
    var hashes = href.slice(href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function getUrl(href)
{
    return href.substr(0, href.indexOf('?'));
}

function check_status_and_publish_facebook(message, image, url) {
    FB.getLoginStatus(function(response) {
            if(response.session){
                // logged in and connected user, someone you know
                publish_facebook(message, image, url);
            } else {
                // no user sessiona vailable, someone you dont know
                FB.login(function(response) {
                    if(response.session){
                        // user successfully logged in
                        publish_facebook(message, image, url);
                    } else {
                        // user cancelled login
                        return false;
                    }});
            }
        });

}


function publish_facebook(message, image, url) {
    
    FB.api('/me/feed', 'POST',
               {
                    method: 'feed',
                    name: message,
                    link: url,
                    picture: image,
                    caption: '',
                    description: language['facebook-likees-desc'],
                    message: ''
                    },
                    function(response) {
                    }
         );
    
    //var attachment =  {'name':message,'href':'http://www.likees.org/','description':'Likees is a social network where you can vote movies, add them to faves and get recommendation from other users.','media':[{'type':'image','src':image,'href':url}]}
    //FB.streamPublish(null, attachment, null, null, null, null,autopublish, null);
}


function setupKudos( postId, kudos )
{
    $('.kudo').remove();
    $('.kudosDiv').append( '<figure class="kudo kudoable"><a class="kudobject"><div class="opening"><div class="circle">&nbsp;</div></div></a><a href="#kudo" class="count"><span class="num">0</span><span class="txt">Kudos</span></a></figure>');
    $('.kudo').data('id', postId );
    // initialize kudos
    $("figure.kudoable").kudoable();
    $(".kudo .num").html( kudos );
    
    // check to see if user has already kudod
    if($.cookie(postId) == 'true') {
        $(".kudo.kudoable").removeClass("animate").addClass("complete");
    }   

    // when kudoing
    $("figure.kudo").bind("kudo:active", function(e)
    {
    });

    // when not kudoing
    $("figure.kudo").bind("kudo:inactive", function(e)
    {
    });

    // after kudo'd
    $("figure.kudo").bind("kudo:added", function(e)
    {
        var element = $(this);
        // ajax'y stuff or whatever you want
        console.log("Kodo'd:", element.data('id'), ":)");
        $.fn.jaxify.sendStandardAjax( '/submitKudos', {'kudo': 1, 'id':postId }, function(){});

        // set cookie so user cannot kudo again for 7 days
        $.cookie(postId, 'true', { expires: 7 });
    });

    // after removing a kudo
    $("figure.kudo").bind("kudo:removed", function(e)
    {
        var element = $(this);
        // ajax'y stuff or whatever you want
        console.log("Un-Kudo'd:", element.data('id'), ":(");
        $.fn.jaxify.sendStandardAjax( '/submitKudos', {'unkudo': 1, 'id':postId }, function(){});
        // remove cookie
        console.log( postId );
        $.cookie(postId, null);
    });
};

$form = $( '.contactForm' ); 
shouldActuallySubmit = true;
lastError = {};

$form.click( function(){
    if( shouldActuallySubmit )
    {
            $( '.contactForm .input' ).each( function( index, element){
                this.setCustomValidity( '');
            });
    }
    else
        shouldActuallySubmit = true;

    return true;
});

$form.submit(function ( event ) {
    event.preventDefault();
    lastError = {};
        
    var dataArray = $form.serializeArray();
    var data = {};
    
    $( '.contactForm .input' ).attr( 'disabled', true ).addClass('disabled');
    //$('.contactForm .submitButton').attr( 'disabled', true );
    //$('.contactForm .input').addClass('disabled');
    $('.formBusy').css('display', 'inline' );
    
    for( i = 0; i < dataArray.length; i ++ )
        data[ dataArray[ i ].name ] = dataArray[ i ].value;
    
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $.extend( {}, data, {
                csrfmiddlewaretoken: $.cookie('csrftoken') 
               }),
        success: function (data) {            
            $('.formBusy').css('display', 'none' );
            
            if( data[ 'done'] == true )
            {
                $( '.formMessage' ).html( 'Thanks for sending me a wink! I will be in touch soon!' ).addClass( 'animated wobble');
                
            }
            else
            {
                $( '.contactForm .input' ).attr( 'disabled', false ).removeClass('disabled');
                var error = data[ 'error' ];
                for( key in error )
                {
                    var input = $('#id_' + key )[ 0 ];
                    var message = error[ key ][ 0 ];
                    console.log( message );
                    input.setCustomValidity( message );
                    shouldActuallySubmit = false;

                }
                
                lastError = error;
                $('.submitButton').click();
                
            }
            
            
        },
        error: function(data) {
            $('.contactForm .submitButton').removeClass('busy').attr( 'disabled', false );
            alert( 'Could not submit your contact form I am afraid');
            $('.formBusy').css('display', 'none' );
            console.log( data.error );
        },
    });
});
        
showAlert = function( type, message )
{
    var delay;
    //this should be a jquery thing!
    $('.AlertBox span').html( message );
    //type is danger or success
    $('.AlertBox').removeClass( 'alert-success' ).removeClass('alert-danger' ).addClass( 'alert-' + type ).fadeIn();
    if( type == 'success' )
        delay = 1;//seconds
    else
        delay = 5;//seconds
    
    $('.AlertBox').delay( delay * 1000 ).fadeOut();
}

closeAlertBox = function()
{
    $('.AlertBox').css('display', 'none');
}

function highlight( $div, endFunction, animationString, updateColor )
{
    if( typeof( animationString ) == 'undefined' || animationString == null )
        animationString = 'animated pulse';
        
    if( typeof( updateColor ) == 'undefined' )
        updateColor = true;
        
    $allElements = $div.find( '*' );
    if( updateColor )
        $allElements.addClass('highlightColor highlightBorder' );
    $div.addClass( animationString );
    $div.one('mozAnimationEnd webkitAnimationEnd oAnimationEnd animationend animationEnd', function(){
        $(this).removeClass( animationString );
        if( updateColor )
            $allElements.removeClass('highlightColor highlightBorder' );
        endFunction();
    });

}

$(document).ready(function(){
   $headerImage = $( '.headerImage' );
   $headerImageInnerWrapper = $( '.headerImageInnerWrapper' );
   $headerImageWrapper = $('.headerImageWrapper');
   hICHeight = $headerImageWrapper.height();
   gap = 0;
   isNoTouch = $('html').hasClass('no-touch');
    $( window ).scroll(function() {
        var yPos = $( this ).scrollTop();
        opacity = 1- Math.min( 1, Math.max( yPos / 200, 0 ) )  
        $headerImage.css('opacity', opacity );
        if( isNoTouch )
        {
        	newHeight = Math.max( 0, hICHeight - yPos + gap );
        	$headerImageInnerWrapper.css('height', newHeight );
        }
        
    });
    
    $('.contactButton').click( function(){
        $("html, body").animate({ scrollTop: $(document).height() }, "medium", null, function(){
            highlight( $('.contactFormDiv'), function(){
                highlight( $('.socialLinks'), function(){} )
            });
        });
        return false; 
    }); 
    
    $.fn.jaxify.jaxifyPage();
    
    var displaySecondNav = function( that )
    {
    	$ul = $( that ).find( 'ul');
    	if( $ul.css('display') == 'block' )
    		$ul.css('display', 'none');
    	else
    		$ul.css('display', 'block');
    }
    
	//because iOS sucks and doesnt quiet respect the CSS3 hover property:
    $('.touch .wideNav ul li.respectHover').click( function( e ){
    	e.preventDefault();
    	displaySecondNav( this );
    } );  
});
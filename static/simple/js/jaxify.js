;(function ( $, window, document, undefined ) {
	
	// Update the page content.
	var $title    	= $( '.pageTitle' );
	var $content  	= $( '.pageContent' );
	var spinner   	= null;
	var spinTarget 	= document.getElementsByTagName('header')[ 0 ];
	
    /**********************************************************
    ** Plugin
    ** definition of the plugin function
    ***********************************************************/
    function Plugin( element, userOptions ) {
        var options = $.extend( {}, $.fn.jaxify.defaults, userOptions );
        
        element.click( function( e ){
        	$.fn.jaxify.spin();
        	//ugly ugly hack to clear anything that may have been loaded
        	var maxId = setTimeout(function(){}, 0);
        	for(var i=0; i < maxId; i+=1) { 
        	    clearTimeout(i);
        	}
        	
            e.preventDefault();
            var url = this.attributes['href'].value;
            $.fn.jaxify.getPageData( url, false );        
            //hacky way to make sure the Hover disappears in the second level of navigations
            var $respectHover = $('.no-touch .respectHover'); 
            $respectHover.removeClass('respectHover');
            $respectHover.delay(500).fadeIn(500, null, function(){ $( this ).addClass('respectHover') });
            $("html, body").animate({ scrollTop: 0 }, "medium" ); 
        }).addClass('jaxified').removeClass('jaxify');   
    }
    
    /**********************************************************
     ** Actual attachment to jQuery
     ***********************************************************/    
    $.fn['jaxify'] = function ( options ) {
        return this.each(function () {
                Plugin( $( this ), options );
        } );
    };
    
    /**********************************************************
    ** Defaults
    ***********************************************************/    
    $.fn.jaxify.defaults = {
        };
    
    $.fn.jaxify.spin = function()
    {
    	if( spinner == null )
    	{
    		$.fn.jaxify.setupSpinner();
    	}
    	else
    		spinner.spin( spinTarget )
    },
    
    $.fn.jaxify.stopSpin = function()
    {
    	spinner.stop();
    },
    
    $.fn.jaxify.setupSpinner = function()
    {
		var opts = {
				  lines: 13, // The number of lines to draw
				  length: 20, // The length of each line
				  width: 10, // The line thickness
				  radius: 30, // The radius of the inner circle
				  corners: 1, // Corner roundness (0..1)
				  rotate: 0, // The rotation offset
				  direction: 1, // 1: clockwise, -1: counterclockwise
				  color: '#E3B74F', // #rgb or #rrggbb or array of colors
				  speed: 1, // Rounds per second
				  trail: 60, // Afterglow percentage
				  shadow: true, // Whether to render a shadow
				  hwaccel: false, // Whether to use hardware acceleration
				  className: 'spinner', // The CSS class to assign to the spinner
				  zIndex: 2e9, // The z-index (defaults to 2000000000)
				  top: 'auto', // Top position relative to parent in px
				  left: 'auto' // Left position relative to parent in px
				};

		spinner = new Spinner(opts).spin( spinTarget );	
    },

    $.fn.jaxify.jaxifyPage = function()
    {
        if (window.history && window.history.pushState)
        {
            var $links = $( '.jaxify' );
                
            // Attach click listeners for each of the nav links.
            $links.jaxify();
            // Update the page content when the popstate event is called.
            window.addEventListener('popstate', function(event) {
                $.fn.jaxify.updateContent( event.state );
            }); 
        };
    }
    
    $.fn.jaxify.sendStandardAjax = function( url, data, successFunction )
    {
        $.ajax({
            type: "POST",
            url:  url,
            data: $.extend( {}, data, {
                csrfmiddlewaretoken: $.cookie('csrftoken'),
            }),
            dataType: 'json',
            success: function( data ) {
                successFunction( data );
            },
            error: function(xhr, textStatus, errorThrown) {
                status = xhr.status;
                console.log( xhr, textStatus );
                successFunction( { 'error': status.toString() + ': Request Failed' } );
                console.log("Error ", errorThrown, textStatus, xhr );
            }
        });        
    };

    $.fn.jaxify.evaluateInlineScript = function( script )
    {
    	if( script.length > 0 )
    	{
    		$( '.inlinescript' ).html('').html(script);
    		eval( $( '.inlinescript' )[0].innerHTML );//ugly, but couldnt get it to work with append
    	}
    }
    
	$.fn.jaxify.updateContent = function( stateObj ) {
	    // Check to make sure that this state object is not null.
	    if (stateObj) {
	    	//$('.wideNav ul li > ul').css('display', 'none');
	        document.title = stateObj.longTitle;
	        $title.html( stateObj.title );
	        $('meta[property="twitter:title"]').attr('content', stateObj.title );
	        $content.html( stateObj.htmlContent );
	        $('meta[property="og:url"]').attr('content', window.location.href )
	        done = stateObj.scripts.length;
	        $('.pageSpecificElement').remove();
	        $('.shareWrapperWrapper').html('').append('<div class="shareWrapper"></div>');
	        $.each( stateObj.scripts, function( index, script){
	        	$.getScript( script, function( data, textStatus, jqxh ){
	        		done -= 1;
	        		if( done == 0 )
	        		{
	        			$.fn.jaxify.evaluateInlineScript( stateObj.inlinescript )
	        		}
	        	});
	        });
	        
	        if( stateObj.scripts.length == 0 )
	        {
	        	$.fn.jaxify.evaluateInlineScript( stateObj.inlinescript )
	        }
	        
	        $.each( stateObj.stylesheets, function( index, stylesheet ){
	        	$('<link>').attr('rel','stylesheet')
	        	  .attr('type','text/css')
	        	  .attr('href',stylesheet)
	        	  .addClass('pageSpecificElement')
	        	  .appendTo('head');
	        });
	        
	        $('.inlinestyle').html(stateObj.inlinestyle);
	        
	        $( '.jaxify').jaxify();
	        highlight( $('article' ), function(){}, null, false );
	        if( stateObj.showKudos )
	        {
	            var id = stateObj.id.toString(); 
	            //$('.kudo').data( 'id', id).removeClass('complete').fadeIn('fast');
	            //$('.kudo .count .num').html( 0 ); 
	            setupKudos( id, stateObj.kudos );
	        }
	        else
	        {
	            $('.kudo').fadeOut('fast');
	            //setupKudos( stateObj.id.toString(), 0 );
	        }
	        
	        $.fn.jaxify.stopSpin();
	    }
	};

	$.fn.jaxify.share = function(url,text)
	{
		$('.shareWrapper').sharrre({
			  share: {
			    facebook: true,
			    twitter: true
			  },
			  buttons: {
			    facebook: {layout: 'box_count'},
			    twitter: {count: 'vertical', via: 'oofaish'}
			  },
			  url: url,
			  text: text,
			  hover: function(api, options){
			    $(api.element).find('.buttons').show();
			  },
			  hide: function(api, options){
			    $(api.element).find('.buttons').hide();
			  },
			  enableTracking: true,
			  title: ' shares',
		});
	};
	
	$.fn.jaxify.getPageData = function( url, firstCall ) {
	    var data = {};
	    var internalurl =  url.replace( '/', '/int/' );
	    if( url == '/home/' )
	        url = '';
	    var pageData = $.fn.jaxify.sendStandardAjax( internalurl, data, function( data )
	        { 
	            if( typeof( data['error'] ) == "undefined" && data != 'Error' )
	            {
	                $.fn.jaxify.updateContent( data );
	                if( firstCall )
	                    history.replaceState( data, data.longTitle, '' );
	                else
	                {
	                    history.pushState(data, data.longTitle, url);
	                    //short url:
	                    var shortUrl = window.location.href;
	                    shortUrl = shortUrl.replace(/^[^\/]*(?:\/[^\/]*){2}/, "" );
	                    _gaq.push( [ '_trackPageview', shortUrl ] );
	                }
	                $('meta[property="og:url"]').attr('content', window.location.href )
	                $.data($('.shareWrapper')[0], 'plugin_sharrre', null);
	                
	                $.fn.jaxify.share(window.location.href, data.longTitle );
	            }
	            else
	            {                
	                //try and go to the url page to force a 404
	                //window.location = url;
	                console.log( data );
	            	console.log( window.location.href );
	                showAlert( 'danger', data['error'] );
	            } 
	        }
	    );
	}
})( jQuery, window, document );
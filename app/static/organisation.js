// BEGIN MODULE

/*
global
$

(function ($) {
    'use strict';

    $(document).ready(function () {

		$('.action').on('click', function() {
		    var action = this.id;
		    flash('inside organisation.js file');
		    console.log("action ",action);

		});

    });


});
// END MODULE - SCRAPING


*/
$('.action').on('click', function() {
		    var action = this.id;
		    flash('inside organisation.js file');
		    console.log("action ",action);
		    function submit_org(action) {
            $.ajax({
                type: 'POST',
                data: JSON.stringify(action),
                url: '/submit_organisation',
                success: 'true',
                error: 'false'
            });
        }

		});





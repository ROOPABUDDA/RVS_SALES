$('.action').on('click', function() {
		    var action = this.id;
		    flash('inside dashboard.js file');
		    console.log("action ",action);
		    
            $.ajax({
                type: 'POST',
                data: JSON.stringify(action),
                url: '/uploadtodb',
                success: 'true',
                error: 'false'
            });
        

		});

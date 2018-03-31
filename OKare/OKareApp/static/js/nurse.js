$(document).ready(function() {
    $('#nurse_table').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     true
    } );
    console.log("DataTables for list_nurse enabled!")
} );

$(document).ready(function() {
    $('#patient_table').DataTable( {
        "paging":   true,
        "ordering": true,
        "info":     true
    } );
    console.log("DataTables for list_patient enabled!")
} );

$(document).ready(function() {
    $('#prod_task_table').DataTable( {
        "paging":   false,
        "ordering": true,
        "info":     true
    } );
    console.log("DataTables for prod_task_table enabled!")
} );

$(document).ready(function(){
 setInterval(function(){
    check_assignment();
    poll_requests();
    check_requests();
 },3000);
});

function check_assignment()
{
    $.ajax({
        type: "POST",
        url: "/Nurse/check_assigned_help_request/",
        success:function(data, status, jqxhr)
        {
            console.log("HELP ME");
            console.log(data);
            if(data.length > 0)
            {
                for(var i = 0; i < data.length; i++)
                {
                    new PNotify({
                        title: "You have been assigned to help your teammate !",
                        text: data[i]['requester'] + " needs help!",
                        type: "info",
                        hide: false,
                        confirm: {
                            confirm: true,
                            buttons: [{
                                text: 'Ok',
                                addClass: 'btn-primary',
                                click: function(notice) {
                                    notice.remove();
                                }
                            },
                            null]
                        },
                    });
                }
            }
        },
        error: function(data, status, jqxhr)
        {
            console.log(data);
        }
    });
}


function poll_requests(){
    $.ajax({
        type: "POST",
        url:"/Nurse/unread_help_request",
        success:function(data, status, jqxhr)
        {
            //console.log("Checking unread help requests");
            //console.log(data);
            if(data.length > 0)
            {
                for(var i = 0; i < data.length; i++)
                {
                    new PNotify({
                        title: "There are new help requests !",
                        text: data[i]['requester'] + " needs help!",
                        type: "info",
                        confirm: {
                            confirm: true,
                            buttons: [{
                                text: 'Ok',
                                addClass: 'btn-primary',
                                click: function(notice) {
                                    notice.remove();
                                }
                            },
                            null]
                        },
                    });
                    console.log("deciding help request table on PNofity");
                    if(window.location == "/Nurse/list_help_request")
                    {
                        console.log("reloading help request table on PNofity");
                        reload_help_request_table();
                    }
                }
            }
        },
        error: function(data, status, jqxhr)
        {
            console.log(data);
        }
    });
}

function check_requests()
{
    $.ajax({
        type: "Post",
        url: "/Nurse/check_help_request",
        dataType: 'json',
        success:function(data, status, jqxhr)
        {
            if(data.length > 0)
            {
                for(var i = 0; i < data.length; i++)
                {
                    new PNotify({
                        title: "Your help request was accepted !",
                        text: data[i]['helper'] + " is on their way to help you!",
                        type: "",
                    });
                }
            }
        }
    });
}


function accept_request(request_id)
{
 $.ajax({
    type:"POST",
    url:"/Nurse/accept_help_request",
    data: {"id": request_id},
    success: function(data, status, jqxhr){
        console.log(data);
        console.log(status);
        new PNotify({
            title: 'Help Request Accepted',
            text: 'Thanks for helping!',
            type: 'success'
        });
        reload_help_request_table();
    },
    error: function(data, status, jqxhr)
    {
        console.log(data);
        console.log(status);
    }
});
}
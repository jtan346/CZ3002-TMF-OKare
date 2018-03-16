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
        "paging":   true,
        "ordering": true,
        "info":     true
    } );
    console.log("DataTables for prod_task_table enabled!")
} );
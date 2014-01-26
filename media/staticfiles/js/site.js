function eachRecursive(data, element)
{
    for (var data_key in data)
    {
        if (typeof data[data_key] == "object" && data[data_key] !== null) {
            // Create a new list group, and then an item that is another list group GROUP-CEPTION!
            // First display the title
            var new_id = element.attr('id') + "-" + data_key.replace(" ", "-");
            $("<a/>", {
                class: "list-group-item",
                text: data_key,
                onclick: 'javascript: $("#' + new_id + '").toggle(); $(this).toggleClass(\'active\');'
            }).appendTo(element);
            var new_group = $("<div/>", {
                class: "list-group",
                id: new_id,
                style: "display: none;"
            }).appendTo(element);
            var new_item = $("<div/>", {
                class: "list-group-item"
            }).appendTo(new_group);
            eachRecursive(data[data_key],
                $("<div/>", {
                    class: "list-group",
                    id: new_id + '-sub-'
                }).appendTo(new_item));
        }
        else {
            var end_element = $("<div/>", {
                class: "list-group-item",
                text: data[data_key]
            }).appendTo(element);
            // If this is a title, append the name to to parent.
            if ( data_key == 'title' ) {
                var parent_anchor = end_element.parent().parent().parent().prev("a.list-group-item");
                parent_anchor.text(parent_anchor.text() + " - " + data[data_key]);
            }
        }
    }
}

function load_media_callback(data) {
    $("#load_media").empty();
    $("<div/>", {
        class: "list-group",
        id: "sections-list-group"
    }).appendTo("#load_media");
    for (var section_key in data) {
        $("<a/>", {
            class: "list-group-item",
            id: section_key + "-list-anchor",
            text: section_key,
            onclick: 'javascript: $("#' + section_key + '-list-data-group").toggle(); $(this).toggleClass(\'active\');'
        }).appendTo("#sections-list-group");
        $("<div/>", {
            class: "list-group",
            id: section_key + "-list-data-group",
            style: "display: none;"
        }).appendTo("#sections-list-group");
        $("<div/>", {
            class: "list-group-item",
            id: section_key + "-list-data-group-item"
        }).appendTo("#" + section_key + "-list-data-group");
        $("<div/>", {
            class: "list-group",
            id: section_key + "-list-data-group-item-group"
        }).appendTo("#" + section_key + "-list-data-group-item");

        eachRecursive(data[section_key], $('#' + section_key + "-list-data-group-item-group"));
    }
}

function search_callback(data){
    if (data.status == 'success') {
        $('#data_loader').empty();
        // Check for empty results
        if ( Object.keys(data['data']).length == 0 ) {
            $('#data_loader').html("No matching media. :-(");
        }
        else {
            $.each(data['data'], function(key, value) {
            $( "<div>" ).appendTo( '#data_loader' ).addClass( "search_result").attr( "id", "r-" + value['media_id'] );
            $( "<h3>" ).appendTo( '#r-' + value['media_id'] ).html(value['title']).append( "</h3>" );
            $( "<div>" ).appendTo( '#r-' + value['media_id'] ).addClass( "sub_element").attr( "id", "s-" + value['media_id']);
            $( '#s-' + value['media_id'] ).html(value['summary']).append( "</div></div>" );
            });
        }
    }
    else {
        $('#data_loader').empty();
        $('#data_loader').append("<div style='color: red;'>" + data.status + "</div>");
    }
}
function torrent_callback(data){
    if (data.status == 'success'){
        $('#torrent_loader').html("");
        // Check for empty results
        if ( Object.keys(data['data']).length == 0 ){
            $('#torrent_loader').html("No search results. :-(");
        }
        else {
            $.each(data['data'], function(key, value) {
                $( "<div>" ).appendTo( '#torrent_loader' ).addClass( "search_result").attr( "id", "torrent-" + key );
                $( "<h3>" ).appendTo( '#torrent-' + key ).html(value['title']).append( "</h3>" );
                $( "<div>" ).appendTo( '#torrent-' + key ).addClass( "sub_element").attr( "id", "torrent-url-" + key);

                // Add a link here to call the ajax request for transmission rpc
                $( '<button class="btn btn-sm btn-info clicker" id="torrent-b-' + key + '">').appendTo( '#torrent-url-' + key ).html("Click to download").append( "</button></div></div>" );

                // Add the onclick event for transmission RPC
                $( '#torrent-b-' + key).click(function() {
                    $( '#torrent-b-' + key).html("Download posted, waiting...");
                    $( '#torrent-b-' + key).removeClass('btn-info');
                    $( '#torrent-b-' + key).addClass('btn-warning');
                    Dajaxice.media.transmission_torrent(transmission_callback, {'url': value['url'], 'id': 'torrent-b-' + key } );
                });

            });
        }
    }
    else
    {
        for (message in data.status){
            $('#torrent_loader').append("<p><b>" + message + ":</b>" + data.status["message"] + "</p>");
        }
    }
}
function transmission_callback(data){
    if (data.status == 'success') {
        $( '#' + data.id).removeClass('btn-warning');
        $( '#' + data.id).addClass('btn-success');
        $( '#' + data.id).html(data.data)
    }
    else {
        $( '#' + data.id).removeClass('btn-warning');
        $( '#' + data.id).addClass('btn-danger');
        $( '#' + data.id).html(data.data)
    }
}

function files_callback(data){
    if (data.status == 'success') {
        var downloadLink = "https://cereal.whatbox.ca/private/files/";
        $( '#files_loader' ).empty();
        $.each(data['data'], function(key, value) {
            // Find out if the current div exists, for this key
            if ( $('#torrent-container-' + key).length == 0 ) {
                $( '#files_loader').append('<div id="torrent-container-' + key + '"></div>');
                // Add onclick delete function here
                $( '#torrent-container-' + key).append('<h3>Torrent ' + key + ' - <button type="buttpn" class="btn btn-xs btn-danger" onclick="delete_torrent(' + key + '); return false;">Delete Torrent and Data</button></h3>');
            }
            // Append each list item to this div
            var length = value.length,
                element = null;
            for (var i = 0; i < length; i++) {
                var filesSplit = value[i].split("/");
                var fileName = filesSplit[filesSplit.length-1];
                $( '#torrent-container-' + key).append('<div><a id="torrent-' + key + '-' + i + '" href="' + downloadLink + value[i] + '">' + fileName + '</a></div>');
            }
        });
        $("#files_loader > div").tsort("",{attr:"id"});
    }
    else {
        alert(data.status);
    }
}

function delete_torrent(torrent_id) {
    Dajaxice.media.delete_torrent(delete_torrent_callback, { 'id': torrent_id } );
    $( '#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Deleting torrent ' + torrent_id + '...</p>');
}

function delete_torrent_callback(data) {
    var torrent_id = data['id'];
    if (data.status == 'success') {
        $( '#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Successfully deleted torrent ' + torrent_id + '.</p>');
    }
    else {
        var torrent_error = data['status']
        $( '#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Failed to delete. Error: ' + torrent_error + '.</p>');
    }
}
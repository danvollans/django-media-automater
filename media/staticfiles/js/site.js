/**
 * Created by djvol_000 on 9/27/13.
 */
$(document).ready(function () {
    $(".toggler").each(function() {
        $( this ).hide()
    });
    $(".clicker").each(function() {
        $( this ).click(function() {
            container = $( this ).closest('div').next('.toggler');
            // Toggle the container
            container.toggle( "slow" );
        });
    });
});

function search_callback(data){
  if (data.status == 'success'){
      $('#data_loader').html("");
      $.each(data['data'], function(key, value) {
          $( "<div>" ).appendTo( '#data_loader' ).addClass( "search_result").attr( "id", "r-" + value['media_id'] );
          $( "<h3>" ).appendTo( '#r-' + value['media_id'] ).html(value['title']).append( "</h3>" );
          $( "<div>" ).appendTo( '#r-' + value['media_id'] ).addClass( "sub_element").attr( "id", "s-" + value['media_id']);
          $( '#s-' + value['media_id'] ).html(value['summary']).append( "</div></div>" );
}     );

  }else{
    for (message in data.status){
      $('#data_loader').append("<p><b>" + message + ":</b>" + data.status["message"] + "</p>");
    }
  }
}
function torrent_callback(data){
  if (data.status == 'success'){
      $('#torrent_loader').html("");
      $.each(data['data'], function(key, value) {
          $( "<div>" ).appendTo( '#torrent_loader' ).addClass( "search_result").attr( "id", "torrent-" + key );
          $( "<h3>" ).appendTo( '#torrent-' + key ).html(value['title']).append( "</h3>" );
          $( "<div>" ).appendTo( '#torrent-' + key ).addClass( "sub_element").attr( "id", "torrent-url-" + key);

          // Add a link here to call the ajax request for transmission rpc
          $( '<a class="clicker" id="torrent-a-' + key + '">').appendTo( '#torrent-url-' + key ).html("Click to download").append( "</a></div></div>" );

          // Add the onclick event for transmission RPC
          $( '#torrent-a-' + key).click(function() {
              $( '#torrent-a-' + key).html("Download posted, waiting...");
              Dajaxice.media.transmission_torrent(transmission_callback, {'url': value['url'], 'id': 'torrent-a-' + key } );
          });

      } );
  }else{
    for (message in data.status){
      $('#torrent_loader').append("<p><b>" + message + ":</b>" + data.status["message"] + "</p>");
    }
  }
}
function transmission_callback(data){
    if (data.status == 'success') {
        $( '#' + data.id).html(data.data)
    }
    else {
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
                $( '#torrent-container-' + key).append('<h3>Torrent ' + key + ' - <a href="#torrent-container-' + key +'" onclick="delete_torrent(' + key + '); return false;">DELETE</a></h3>');
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
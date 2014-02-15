// AJAX For Downloader Services
function addDownload(download_url, location) {
    Dajaxice.media.transfer_file(download_file_callback, {'url': download_url, 'location': $('#' + location).val()});
}

function download_file_callback(data) {
    if (data['status'] === 'success') {
        refresh_downloads();
    }
}

function refresh_downloads() {
    Dajaxice.media.load_downloads(downloads_callback);
}

function refresh_files_ajax() {
    Dajaxice.media.refresh_files(files_callback);
}

function downloads_callback(data) {
    $('#active_panel_body').empty();
    var active_data = data['active'];
    for (var active_download in active_data) {
        for (var active_file in active_data[active_download]['files']) {
            var download_file = active_data[active_download]['files'][active_file]['path'];
            var total_length = active_data[active_download]['files'][active_file]['length'];
            var completed_length = active_data[active_download]['files'][active_file]['completedLength'];
            var percentage = Math.floor((parseInt(completed_length) / parseInt(total_length)) * 100).toString();
            var holder = $('<div/>', {
                class: "progress"
            }).appendTo('#active_panel_body');
            var holder_bar = $('<div/>', {
                class: "progress-bar progress-bar-info",
                role: "progressbar",
                "aria-valuenow": percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
                style: "width: " + percentage + "%"
            }).appendTo($(holder));
            $('<span/>', {
                class: "show",
                text: download_file.split("/").pop()
            }).appendTo($(holder_bar));
        }
    }

    $('#stopped_panel_body').empty();
    var stopped_data = data['stopped'];
    for (var stopped_download in stopped_data) {
        for (var stopped_file in stopped_data[stopped_download]['files']) {
            var download_file = stopped_data[stopped_download]['files'][stopped_file]['path'];
            var total_length = stopped_data[stopped_download]['files'][stopped_file]['length'];
            var completed_length = stopped_data[stopped_download]['files'][stopped_file]['completedLength'];
            var percentage = Math.floor((parseInt(completed_length) / parseInt(total_length)) * 100).toString();
            var holder = $('<div/>', {
                class: "progress"
            }).appendTo('#stopped_panel_body');
            var holder_bar = $('<div/>', {
                class: "progress-bar progress-bar-success",
                role: "progressbar",
                "aria-valuenow": percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
                style: "width: " + percentage + "%"
            }).appendTo($(holder));
            $('<span/>', {
                class: "show",
                text: download_file.split("/").pop()
            }).appendTo($(holder_bar));
        }
    }

    $('#waiting_panel_body').empty();
    var waiting_data = data['waiting'];
    for (var waiting_download in waiting_data) {
        for (var waiting_file in waiting_data[waiting_download]['files']) {
            var download_file = waiting_data[waiting_download]['files'][waiting_file]['path'];
            var total_length = waiting_data[waiting_download]['files'][waiting_file]['length'];
            var completed_length = waiting_data[waiting_download]['files'][waiting_file]['completedLength'];
            var percentage = Math.floor((parseInt(completed_length) / parseInt(total_length)) * 100).toString();
            var holder = $('<div/>', {
                class: "progress"
            }).appendTo('#waiting_panel_body');
            var holder_bar = $('<div/>', {
                class: "progress-bar progress-bar-info",
                role: "progressbar",
                "aria-valuenow": percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
                style: "width: " + percentage + "%"
            }).appendTo($(holder));
            $('<span/>', {
                class: "show",
                text: download_file.split("/").pop()
            }).appendTo($(holder_bar));
        }
    }
}

function guess_location(filename, textbox) {
    var show_reg = /(.*)[ .][sS](\d{1,2})[eE](\d{1,2})[ .a-zA-Z]*(\d{3,4}p)?/;
    var movie_reg = /(.+)?(\d{4})([ .a-zA-Z]*)?/
    //if not parsed:
    //    parsed = re.findall(r"""(.*?[ .]\d{4})[ .a-zA-Z]*(\d{3,4}p)?""", file_name, re.VERBOSE)
    //alert(filename.match(show_reg).splice(0, 1));

    // Check if torrent already exists
    var parsed_torrent = filename.match(show_reg);
    if (parsed_torrent) {
        var torrent_data = parsed_torrent.slice(1);
        var show_name = jQuery.trim(torrent_data[0].split('.').join(' '));
        var show_season = torrent_data[1];
        var show_episode = torrent_data[2];
        $('#' + textbox).val('TV Shows/' + show_name + '/Season ' + parseInt(show_season).toString() + '/');
    }
    else {
        var parsed_torrent = filename.match(movie_reg);
        if (parsed_torrent) {
            var torrent_data = parsed_torrent.slice(1);
            var movie_name = jQuery.trim(torrent_data[0].split('.').join(' ').replace(/\[|\)|\]|\(/g, ''));
            $('#' + textbox).val('Movies/' + movie_name + '/');
        }
    }
}

function parse_torrent(filename) {
    var show_reg = /(.*)[ .][sS](\d{1,2})[eE](\d{1,2})[ .a-zA-Z]*(\d{3,4}p)?/;
    var movie_reg = /(.+)?(\d{4})([ .a-zA-Z]*)?/
    //if not parsed:
    //    parsed = re.findall(r"""(.*?[ .]\d{4})[ .a-zA-Z]*(\d{3,4}p)?""", file_name, re.VERBOSE)
    //alert(filename.match(show_reg).splice(0, 1));

    // Check if torrent already exists
    var parsed_torrent = filename.match(show_reg);
    if (parsed_torrent) {
        var torrent_data = parsed_torrent.slice(1);
        $('input[type=radio][value=show]').prop('checked', true);
        $('#id_search_text').val(jQuery.trim(torrent_data[0].split('.').join(' ')));
        $('#id_optional_season').val(parseInt(torrent_data[1]));
        $('#id_optional_episode').val(parseInt(torrent_data[2]));

        Dajaxice.media.search_media(search_callback, $('#search_form').serializeObject());
    }
    else {
        var parsed_torrent = filename.match(movie_reg);
        if (parsed_torrent) {
            var torrent_data = parsed_torrent.slice(1);
            $('input[type=radio][value=movie]').prop('checked', true);
            $('#id_search_text').val(jQuery.trim(torrent_data[0].split('.').join(' ').replace(/\[|\)|\]|\(/g, '')));

            Dajaxice.media.search_media(search_callback, $('#search_form').serializeObject());
        }
    }
}

function eachRecursive(data, element) {
    for (var data_key in data) {
        if (typeof data[data_key] === "object" && data[data_key] !== null) {
            // Create a new list group, and then an item that is another list group GROUP-CEPTION!
            // First display the title
            var new_id = element.attr('id') + "-" + data_key.replace(/\s|\(|\)/g, "-");
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
            if (data_key === 'title') {
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

function search_callback(data) {
    if (data.status === 'success') {
        $('#data_loader').empty();
        // Check for empty results
        if (Object.keys(data['data']).length === 0) {
            $('#data_loader').html("No matching media. :-(");
        }
        else {
            $.each(data['data'], function (key, value) {
                $("<div>").appendTo('#data_loader').addClass("search_result").attr("id", "r-" + value['media_id']);
                $("<h3>").appendTo('#r-' + value['media_id']).html(value['title']).append("</h3>");
                $("<div>").appendTo('#r-' + value['media_id']).addClass("sub_element").attr("id", "s-" + value['media_id']);
                $('#s-' + value['media_id']).html(value['summary']).append("</div></div>");
            });
        }
    }
    else {
        $('#data_loader').empty();
        $('#data_loader').append("<div style='color: red;'>" + data.status + "</div>");
    }
}
function torrent_callback(data) {
    if (data.status === 'success') {
        $('#torrent_loader').html("");
        // Check for empty results
        if (Object.keys(data['data']).length === 0) {
            $('#torrent_loader').html("No search results. :-(");
        }
        else {
            $.each(data['data'], function (key, value) {
                $("<div/>", {
                    class: 'search_result panel panel-info',
                    id: "torrent-" + key
                }).appendTo('#torrent_loader');
                $("<div/>", {
                    class: 'panel-heading',
                    id: "torrent-" + key + '-heading'
                }).appendTo("#torrent-" + key);
                $("<h4/>", {
                    text: value['title']
                }).appendTo('#torrent-' + key + '-heading');
                $("<div/>", {
                    class: "sub_element panel-body",
                    id: "torrent-url-" + key
                }).appendTo('#torrent-' + key);

                // Add a link here to call the ajax request for transmission rpc
                $('<button class="btn btn-sm btn-info clicker" id="torrent-b-' + key + '">').appendTo('#torrent-url-' + key).html("Click to download").append("</button></div></div>");

                // Add a button to call the search to see if it exists
                $('<button class="btn btn-sm btn-warning clicker" id="torrent-c-' + key + '">').appendTo('#torrent-url-' + key).html("Check if it already exists").append("</button></div></div>");

                // Add the onclick event for transmission RPC
                $('#torrent-b-' + key).click(function () {
                    $('#torrent-b-' + key).html("Download posted, waiting...");
                    $('#torrent-b-' + key).removeClass('btn-info');
                    $('#torrent-b-' + key).addClass('btn-warning');
                    Dajaxice.media.transmission_torrent(transmission_callback, {'url': value['url'], 'id': 'torrent-b-' + key });
                });

                // Add the onclick event for the checking of file existence
                $('#torrent-c-' + key).click(function () {
                    parse_torrent(value['title'])
                })

            });
        }
    }
    else {
        for (message in data.status) {
            $('#torrent_loader').append("<p><b>" + message + ":</b>" + data.status["message"] + "</p>");
        }
    }
}
function transmission_callback(data) {
    if (data.status === 'success') {
        $('#' + data.id).removeClass('btn-warning');
        $('#' + data.id).addClass('btn-success');
        $('#' + data.id).html(data.data)
    }
    else {
        $('#' + data.id).removeClass('btn-warning');
        $('#' + data.id).addClass('btn-danger');
        $('#' + data.id).html(data.data)
    }
}

function files_callback(data) {
    if (data.status === 'success') {
        var downloadLink = "https://cereal.whatbox.ca/private/files/";

        /// If Div exists with a percentage bar already, just update the percentage
        var active_data = data['data']['active'];
        for (var active_torrent in active_data) {
            var percentage = active_data[active_torrent]['progress'].toString();
            var speed = parseInt(active_data[active_torrent]['speed']);
            if ($('#torrent-container-' + active_torrent + '-progress').length) {
                $('#torrent-container-' + active_torrent + '-progress').css('width', percentage + "%");
                $('#torrent-container-' + active_torrent + '-progress span').html('Downloading - speed: ' + Math.floor((speed / 1000) / 1000).toString() + ' MB/s')
                continue;
            }
            var active_files = active_data[active_torrent]['files'];
            var torrent_holder = $('<div/>', {
                id: 'torrent-container-' + active_torrent
            }).appendTo('#torrents_active_panel_body');
            $('<span/>', {
                text: 'Torrent ID: ' + active_torrent,
                style: "font-weight: bold; margin-right: 20px;"
            }).appendTo($(torrent_holder));
            $(torrent_holder).append('<button type="button" class="btn btn-xs btn-danger" onclick="javascript: delete_torrent(' + active_torrent + '); return false;">Delete Torrent and Data</button>');
            var holder = $('<div/>', {
                class: "progress"
            }).appendTo($(torrent_holder));
            var holder_bar = $('<div/>', {
                id: 'torrent-container-' + active_torrent + '-progress',
                class: "progress-bar progress-bar-info",
                role: "progressbar",
                "aria-valuenow": percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
                style: "width: " + percentage + "%"
            }).appendTo($(holder));
            $('<span/>', {
                class: "show",
                text: 'Downloading - speed: ' + Math.floor((speed / 1000) / 1000).toString() + ' MB/s'
            }).appendTo($(holder_bar));
            var files_holder = $('<div/>', {
                text: 'Files:'
            }).appendTo($(torrent_holder));
            var files_ul_holder = $('<ul/>').appendTo($(files_holder));
            for (var file in active_files) {
                var file_name = active_files[file]['name'].split('/');
                if (file_name.length > 1) {
                    file_name = file_name.pop();
                }
                var file_li = $('<li/>', {
                    text: file_name
                }).appendTo($(files_ul_holder));
            }
        }

        // First loop through all alements in the finished array.
        // If Div Exists, pass.
        // If Div does not Exist, add the stuffs.
        var stopped_data = data['data']['finished'];
        for (var stopped_torrent in stopped_data) {
            if ($('#torrents_active #torrent-container-' + stopped_torrent).length) {
                $('#torrents_active #torrent-container-' + stopped_torrent).remove();
            }
            if ($('#torrents_stopped #torrent-container-' + stopped_torrent).length) {
                continue;
            }
            var stopped_files = stopped_data[stopped_torrent]['files'];
            var percentage = stopped_data[stopped_torrent]['progress'].toString();
            var speed = stopped_data[stopped_torrent]['speed'];
            var torrent_holder = $('<div/>', {
                id: 'torrent-container-' + stopped_torrent
            }).appendTo('#torrents_stopped_panel_body');
            $('<span/>', {
                text: 'Torrent ID: ' + stopped_torrent,
                style: "font-weight: bold; margin-right: 20px;"
            }).appendTo($(torrent_holder));
            $(torrent_holder).append('<button type="button" class="btn btn-xs btn-danger" onclick="javascript: delete_torrent(' + stopped_torrent + '); return false;">Delete Torrent and Data</button>');
            var holder = $('<div/>', {
                class: "progress"
            }).appendTo($(torrent_holder));
            var holder_bar = $('<div/>', {
                class: "progress-bar progress-bar-success",
                role: "progressbar",
                "aria-valuenow": percentage,
                "aria-valuemin": "0",
                "aria-valuemax": "100",
                style: "width: " + percentage + "%"
            }).appendTo($(holder));
            $('<span/>', {
                class: "show",
                text: 'Finished - speed: ' + speed + ' MB/s'
            }).appendTo($(holder_bar));
            var files_holder = $('<div/>', {
                text: 'Files:'
            }).appendTo($(torrent_holder));
            var files_ul_holder = $('<ul/>').appendTo($(files_holder));
            var file_counter = 0;
            for (var file in stopped_files) {
                var file_li = $('<li/>').appendTo($(files_ul_holder));
                var file_name = stopped_files[file]['name'].split('/').pop();
                $('<a/>', {
                    text: file_name,
                    href:downloadLink + stopped_files[file]['name']
                }).appendTo($(file_li));
                var file_container = $('<div/>', {
                    class: 'file_holder',
                    style: 'width: 100%'
                }).appendTo($(file_li));
                $('<input/>', {
                    id: 'torrent-' + stopped_torrent + '-' + file_counter + '-input',
                    type: 'text',
                    class: 'textinput textInput form-control',
                    style: 'width: 70%'
                }).appendTo($(file_container));
                guess_location(file_name, 'torrent-' + stopped_torrent + '-' + file_counter + '-input');
                $(file_container).append('<button style="width: 20%" type="button" class="btn btn-xs btn-success" onclick="javascript: addDownload(\'' + downloadLink + stopped_files[file]['name'] + '\', \'torrent-' + stopped_torrent + '-' + file_counter + '-input\');">Download File</button>');
                file_counter++;
            }
        }

        return false;

        var downloadLink = "https://cereal.whatbox.ca/private/files/";
        $('#files_loader').empty();
        $.each(data['data'], function (key, value) {
            // Find out if the current div exists, for this key
            if ($('#torrent-container-' + key).length === 0) {
                $('#files_loader').append('<div id="torrent-container-' + key + '"></div>');
                // Add onclick delete function here
                $('#torrent-container-' + key).append('<h3>Torrent ' + key + ' - <button type="button" class="btn btn-xs btn-danger" onclick="delete_torrent(' + key + '); return false;">Delete Torrent and Data</button></h3>');
            }
            // Append each list item to this div
            var length = value.length,
                element = null;
            for (var i = 0; i < length; i++) {
                var filesSplit = value[i].split("/");
                var fileName = filesSplit[filesSplit.length - 1];
                $('#torrent-container-' + key).append('<div><button type="button" class="btn btn-xs btn-success" onclick="addDownload(\'' + downloadLink + value[i] + '\',\'torrent-' + key + '-' + i + '-location\');">Download File</button><a id="torrent-' + key + '-' + i + '" href="' + downloadLink + value[i] + '">' + fileName + '</a></div>');
                $('#torrent-container-' + key).append('<div><button type="button" class="btn btn-xs btn-info" onclick="guess_location(\'' + fileName + '\', \'torrent-' + key + '-' + i + '-location\');">Guess Location</button><input id="torrent-' + key + '-' + i + '-location" type="text" class="textinput textInput form-control"></input></div>');
            }
        });
        $("#files_loader > div").tsort("", {attr: "id"});
    }
    else {
        alert(data.status);
    }
}

function delete_torrent(torrent_id) {
    Dajaxice.media.delete_torrent(delete_torrent_callback, { 'id': torrent_id });
    $('#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Deleting torrent ' + torrent_id + '...</p>');
}

function delete_torrent_callback(data) {
    var torrent_id = data['id'];
    if (data.status === 'success') {
        $('#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Successfully deleted torrent ' + torrent_id + '.</p>');
    }
    else {
        var torrent_error = data['status']
        $('#torrent-container-' + torrent_id).html('<h3>Torrent ' + torrent_id + '</h3><p>Failed to delete. Error: ' + torrent_error + '.</p>');
    }
}

$(document).ready(function () {
    var timerId = setInterval(refresh_files_ajax, 20000);
    var downloadTimer = setInterval(refresh_downloads, 20000);
});
// commented by HC on Nov. 11, 2013
//    because this does not have a good compatibility with every browser
//    The related actions will be changed to save to db immediately after user click
// BEGIN comment
//$(window).bind("beforeunload", function() {
//        CallbackBeforeUnload();
//});
// END comment

// function declaration
// This function will be called after the accordion is created
function CallbackAfterAccordionCreated() {
    // The function MUST be override in html page
}

// function declaration
// This function will be called after a section of the accordion is clicked
function CallbackOnAccordionClicked(hid, bflag) {
    // The function MUST be override in html page
}


function SavePageStatusToMongoDB(flag_save) {
    if (flag_save) {
        $.ajax({
            type: "POST",
            url:  "/mesh/savepagestatus/",
            data: JSON.stringify(status_object),
            dataType: "json",
            contentType: 'application/json; charset=utf-8',
        });
    }
};

// params: surl and js_object MUST provided by user
function AjaxSaveObject(surl, js_object, flag_save) {
    flag_save = (typeof flag_save === 'undefined')? true : flag_save;
    if (flag_save) {
        $.ajax({
            type: "PUT",
            url:  surl,
            headers: {
                Accept: "application/json",
                contentType: "application/json; charset=utf-8",
            },
            dataType: "json",
            data: JSON.stringify(js_object),
        });
    }
};

function StopEventPropagation(e) {
    if (!e)
        e = window.event;

    //IE9 & Other Browsers
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    //IE8 and Lower
    else {
        e.cancelBubble = true;
    }
};

function PreventClickEventPropagate(helem) {
    $(helem).on(
        "mousedown", function(e) {
            StopEventPropagation(e);
        }
    ).on(
        "mouseup", function(e) {
            StopEventPropagation(e);
        }
    ).on(
        "click", function(e) {
            StopEventPropagation(e);
        }
    );
};


function CustomizeAccordionPlugin(aid, CallbackOnAccordionClicked, CallbackAfterAccordionCreated) {
    $(aid).accordion(
        {
            collapsible: true,
            heightStyle: "content",
            active: false,
            beforeActivate: function(event, ui) {
                if (ui.newHeader[0]) {    // The accordion believes a panel is being opened
                    var currHeader  = ui.newHeader;
                    var currContent = currHeader.next('.ui-accordion-content');
                } else {    // The accordion believes a panel is being closed
                    var currHeader  = ui.oldHeader;
                    var currContent = currHeader.next('.ui-accordion-content');
                }
                // Since we've changed the default behavior, this detects the actual status
                var isPanelSelected = currHeader.attr('selected-status') == 'true';
                // Toggle the panel's header
                currHeader.toggleClass('ui-corner-all',isPanelSelected).toggleClass('accordion-header-active ui-state-active ui-corner-top',!isPanelSelected).attr('selected-status',((!isPanelSelected).toString()));
                // Toggle the panel's icon
                currHeader.children('.ui-icon').toggleClass('ui-icon-triangle-1-e',isPanelSelected).toggleClass('ui-icon-triangle-1-s',!isPanelSelected);
                // Toggle the panel's content
                currContent.toggleClass('accordion-content-active',!isPanelSelected);
                if (isPanelSelected) {
                    currContent.slideUp();
                } else {
                    currContent.slideDown();
                }
                CallbackOnAccordionClicked(currHeader.attr("id"), !isPanelSelected);

                return false; // Cancel the default action
            },
            create: function( event, ui ) {
                CallbackAfterAccordionCreated();
            },
        });
};
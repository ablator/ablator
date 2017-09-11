$(document).ready(function () {
    reloadFunctionalityPage();
    window.setInterval(reloadFunctionalityPage, 1000);

    reloadFunctionalityLogWindow();
    window.setInterval(reloadFunctionalityLogWindow, 5000);
});

function reloadFunctionalityPage() {
    reloadFunctionalityEnabledUsersCount();
    reloadFunctionalityProgress();
    reloadFunctionalityFlavors();
}

function reloadFunctionalityEnabledUsersCount() {
    var enabledUsersDiv = $('#functionality-enabled-users');
    if (enabledUsersDiv.length) {
        console.log("Reloading... #functionality-enabled-users");
        $.get(enabledUsersDiv.attr("data-id"), function (data) {
            enabledUsersDiv.html(data);
        });
    }
}

function reloadFunctionalityProgress() {
    var progressSection = $('#functionality-progress');
    if (progressSection.length) {
        console.log("Reloading... #functionality-progress");
        $.get(progressSection.attr("data-id"), function (data) {
            progressSection.html(data);
        });
    }
}

function reloadFunctionalityFlavors() {
    var flavorsSection = $('#functionality-flavors');
    if (flavorsSection.length) {
        console.log("Reloading... #functionality-flavors");
        $.get(flavorsSection.attr("data-id"), function (data) {
            flavorsSection.html(data);
        });
    }
}

function reloadFunctionalityLogWindow() {
    var logWindow = $("#log-window");
    if (logWindow.length) {
        console.log("Reloading... #log-window");
        $.get(logWindow.attr("data-id"), function (data) {
            logWindow.html(data);
        });
    }
}
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
    if (enabledUsersDiv) {
        $.get(enabledUsersDiv.attr("data-id"), function (data) {
            enabledUsersDiv.html(data);
        });
    }
}

function reloadFunctionalityProgress() {
    var progressSection = $('#functionality-progress');
    if (progressSection) {
        $.get(progressSection.attr("data-id"), function (data) {
            progressSection.html(data);
        });
    }
}

function reloadFunctionalityFlavors() {
    var flavorsSection = $('#functionality-flavors');
    if (flavorsSection) {
        $.get(flavorsSection.attr("data-id"), function (data) {
            flavorsSection.html(data);
        });
    }
}

function reloadFunctionalityLogWindow() {
    var logWindow = $("#log-window");
    if (logWindow) {
        $.get(logWindow.attr("data-id"), function (data) {
            logWindow.html(data);
        });
    }
}
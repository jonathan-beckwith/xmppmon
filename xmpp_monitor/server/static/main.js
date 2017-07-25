google.load("visualization", "1", { packages:["corechart", 'timeline', 'bar'] });

google.setOnLoadCallback(function () {

    var timezone = "America/Toronto",
        today = moment(),
        event_filter = {
            startdate: today.tz(timezone).format("YYYY-MM-DD"),
            enddate: today.add(1, 'days').tz(timezone).format("YYYY-MM-DD"),
            jid: ''
        };

    console.log(event_filter);

    function load_user_list() {
        $.getJSON('users.json',  {}, function (data) {
            var user_list = $('#user_list tbody');
            user_list.empty();

            $.each(data.users, function(idx, user) {
                user_list.append([
                    "<tr><td>", user.jid, "</td><td>", user.name, "</td></tr>"
                ].join(''));
            });

        });
    }

    function load_event_list() {
        $.getJSON('events.json', event_filter, function (data) {
            var event_list = $('#event_list tbody');
            event_list.empty();

            $.each(data.events, function(idx, event) {
                event_list.append([
                    "<tr><td>",
                    event.jid, "</td><td>",
                    event.status, "</td><td>",
                    moment(event.start).clone().tz(timezone).format("YYYY-MM-DD hh:mm z"), "</td><td>",
                    moment.duration(moment(event.end) - moment(event.start)).humanize(), "</td></tr>"
                ].join(''));
            });

            console.log(data.events)

            drawTimeLine(data);
            drawPie(data);
        });
    }

    function add_user(event) {
        event.preventDefault();
        var data = $(this).serializeObject();
        $.postJSON("users.json", data, function (data) {
            load_user_list();
        });
    }

    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function drawPolar(data) {
        // Get the context of the canvas element we want to select
        var ctx = document.getElementById("radar").getContext("2d");

        var dataTable = [];

        var events = {};
        $.each(data.events, function (idx, event) {
            var duration = moment(event.end) - moment(event.start);
            events[event.status] = (events[event.status] || 0) + duration;
        });


        $.each(events, function(key, duration) {
            dataTable.push({
                label: key,
                color: getRandomColor(),
                highlight: getRandomColor(),
                value: duration
            })
        });

        return new Chart(ctx).PolarArea(dataTable);
    }

    function drawRadar(eventdata) {
        // Get the context of the canvas element we want to select
        var ctx = document.getElementById("radar").getContext("2d");

        var events = {},
            data = {
                labels: [],
                datasets: [{
                    data: []
                }]
            };

        $.each(eventdata.events, function (idx, event) {
            var duration = moment(event.end) - moment(event.start);
            events[event.status] = (events[event.status] || 0) + duration;

            if (data.labels.indexOf(event.status) === -1) {
                data.labels.push(event.status);
            }

            data.datasets[0].data === data.datasets[0].data || [];
            var indx = data.labels.indexOf(event.status)
            data.datasets[0].data[indx] = (data.datasets[0].data[indx] || 0)+ duration;
        });

        var myNewChart = new Chart(ctx).Radar(data);
    }

    function drawPie(data) {
        var chart = new google.visualization.PieChart(
                document.getElementById('bar')
            ),
            dataTable = new google.visualization.DataTable();

        dataTable.addColumn({type: 'string', id: 'status'});
        dataTable.addColumn({type: 'number', id: 'duration'});

        var events = {};
        $.each(data.events, function (idx, event) {
            var duration = moment(event.end) - moment(event.start);
            events[event.status] = (events[event.status] || 0) + duration;
        });


        $.each(events, function(key, duration) {
            dataTable.addRow([key, duration])
        });

        chart.draw(dataTable);
    }

    function drawTimeLine(data) {
        var chart = new google.visualization.Timeline(
                document.getElementById('timeline')
            ),
            dataTable = new google.visualization.DataTable()

        dataTable.addColumn({type: 'string', id: 'JID'});
        dataTable.addColumn({type: 'string', id: 'Status'});
        dataTable.addColumn({type: 'date', id: 'Start'});
        dataTable.addColumn({type: 'date', id: 'End'});

        jids = {};
        $.each(data.events, function (idx, event) {
            dataTable.addRow([
                event.jid,
                event.status,
                moment(event.start).tz(timezone).toDate(),
                moment(event.end).tz(timezone).toDate()
            ]);
            jids[event.jid] = true;
        });


        height = 128;
        console.log(jids);
        $.each(jids, function () {
            height += 48;
        });

        chart.draw(dataTable, { height: height });
    }

    function initialize() {
        load_user_list();
        load_event_list();
    }

    $('#add_user').submit(add_user);

    $('#update').click(function () {
        event_filter.jid = $('#jid').val();

        start = $('#startdate').val();
        if (start === '') {
            start = moment().hours(9);
        } else {
            start = moment(start);
        }

        end = $('#enddate').val();
        if (end === '') {
            end = moment().add(1, 'days').hours(17);
        } else {
            end = moment(end);
        }

        event_filter.startdate = start.format();
        event_filter.enddate = end.format();
        initialize();
    });


    $('#startdate').val(event_filter.startdate);
    $('#enddate').val(event_filter.enddate);
    moment.utc().format(); 
    initialize();
});
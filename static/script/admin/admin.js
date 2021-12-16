var $ = mdui.$;
//$("#cs-admin-user-table")
//$.ajax({
//    method: 'GET',
//    url: '/api/admin/getuser',
//    async: true,
//    headers: {},
//    success: function (data) {
//        data = JSON.parse(data)
//        //console.log(data);
//        id = 1
//        table_html = "";
//        for (each in data) {
//            //console.log(data[each])
//            table_html += "<tr>"
//            table_html += "<td>" + id + "</td>" //id
//            table_html += "<td>" + data[each].name + "</td>" //name
//            table_html += "<td>" + data[each].email + "</td>" //email
//            table_html += "<td>" + id + "</td>" //group
//            table_html += "<td>" + id + "</td>" //status
//            table_html += "<td>" + id + "</td>" //actions
//            table_html += "</tr>"
//            id += 1;
//        }
//        $("#cs-admin-user-table").html(table_html)
//        mdui.updateTables()
//    }
//});


var vlSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": "container",
    "height": 400,
    "description": "Stock prices of 5 Tech Companies over Time.",
    "data": {
        "url": "//vega.github.io/vega-lite/data/stocks.csv"
    },
    "mark": {
        "type": "line",
        "point": {
            "filled": false,
            "fill": "white"
        }
    },
    "encoding": {
        "x": {
            "timeUnit": "year",
            "field": "date"
        },
        "y": {
            "aggregate": "mean",
            "field": "price",
            "type": "quantitative"
        },
        "color": {
            "field": "symbol",
            "type": "nominal"
        }
    }
}



// Embed the visualization in the container with id `vis`
vegaEmbed('#vis', vlSpec);
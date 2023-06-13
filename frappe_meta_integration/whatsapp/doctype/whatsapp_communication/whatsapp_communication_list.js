// Copyright (c) 2022, efeone Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.listview_settings['WhatsApp Communication'] = {
    get_indicator: function(doc) {
        var indicator = [__(doc.status), frappe.utils.guess_colour(doc.status), "status,=," + doc.status];
        if(doc.status=="Delivered") {
          indicator[1] = "cyan";
        }
        if(doc.status=="Read") {
          indicator[1] = "green";
        }
        if(doc.status=="Received") {
          indicator[1] = "blue";
        }
        if(doc.status=="Sent"){
          indicator[1] = "orange";
        }
        if(doc.status=="Pending"){
          indicator[1] = "red";
        }
        return indicator;
    }
};

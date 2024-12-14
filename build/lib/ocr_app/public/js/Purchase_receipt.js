
console.log("Custom Purchase Receipt JS Loaded!");

frappe.ui.form.on('Purchase Receipt Item', {
    custom_extract_text_from_sticker: async function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
       
        
        if (!row.custom_attach_image) {
            frappe.msgprint(__('Please upload an image before extracting data.'));
            console.log("No image uploaded. Exiting process.");
            return;
        }
        console.log("Image exists. Making API call...");
        // await frm.save();
        // await frm.reload_doc();
         
         // Save the document to ensure the new row is committed
        //  if (frm.is_dirty()) {
        //     console.log("Document has unsaved changes. Saving document...");
        //     try {
        //         await frm.save(); // Use async/await to wait for save completion
        //         frappe.ui.form.refresh();
        //         await frm.reload_doc();
               
        //         console.log("Document saved successfully.");
        //     } catch (error) {
        //         console.error("Error saving document:", error);
        //         frappe.msgprint(__('Could not save the document. Please try again.'));
        //         return;
        //     }
        // }
       
        
     

// Now make the API call
        frappe.call({
            method: 'ocr_app.api.extract_item_level_data',
            args: {
                docname: frm.doc.name,
                item_idx: row.idx // Pass the correct item index
            },
            callback: function (r) {
                if (r.message.success) {
                    frappe.msgprint(__('Data extracted successfully!'));
                    frappe.model.set_value(cdt, cdn, 'custom_lot_no', r.message.lot_no);
                    frappe.model.set_value(cdt, cdn, 'custom_reel_no', r.message.reel_no);
                    frappe.model.set_value(cdt, cdn, 'qty', r.message.qty);

                    // Update dependent fields
                    frappe.model.set_value(cdt, cdn, 'accepted_qty', r.message.qty);
                    frappe.model.set_value(cdt, cdn, 'rejected_qty', 0);

                    console.log("Fields updated successfully.");
                    frm.reload_doc();
                } else {
                    frappe.msgprint(__('Error: ' + r.message.error));
                }
            }
        });
        await frm.reload_doc();
    }
   
     

});
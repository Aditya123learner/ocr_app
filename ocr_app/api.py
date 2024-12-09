import pytesseract
import re
import frappe
from frappe.utils.file_manager import get_file_path

@frappe.whitelist()
def extract_item_level_data(docname, item_idx):
    try:
        # Fetch the Purchase Receipt document
        doc = frappe.get_doc("Purchase Receipt", docname)
        item = next((i for i in doc.items if i.idx == int(item_idx)), None)
        
        if not item:
            return {"success": False, "error": "Item not found."}

        # Get the file URL for the image
        file_url = item.custom_sticker_copy
        if not file_url:
            return {"success": False, "error": "Please upload an image before extracting data."}

        # Get the file path
        file_path = get_file_path(file_url)
        
        # Extract text using …
frappe.ui.form.on('Purchase Receipt Item', {
    custom_extract_text_from_sticker: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        if (!row.custom_sticker_copy) {
            frappe.msgprint(__('Please upload an image before extracting data.'));
            return;
        }

        frappe.call({
            method: 'custom_ocr_app.api.extract_item_level_data',
            args: {
                docname: frm.doc.name,
                item_idx: row.idx
            },
            callback: function(r) {
                if (r.message.success) {
                    frappe.msgprint(__('Data extracted successfully!'));
                    frappe.model.set_value(cdt, cdn, 'custom_lot_no', r.message.lot_no);
                    frappe.model.set_value(cdt, cdn, 'custom_reel_size', r.message.reel_no);
                    frappe.model.set_value(cdt, cdn, 'qty', r.message.qty);


                    // Ensure UI reflects changes in dependent fields
                    frappe.model.set_value(cdt, cdn, 'accepted_qty', r.message.qty);
                    frappe.model.set_value(cdt, cdn, 'rejected_qty', 0);
                } else {
                    frappe.msgprint(__('Error: ' + r.message.error));
                }
            }
        });
    }
});
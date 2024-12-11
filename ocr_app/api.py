import pytesseract
import re
import frappe
from frappe.utils.file_manager import get_file_path

@frappe.whitelist()
def extract_item_level_data(docname, item_idx):
    try:
        # Fetch the Purchase Receipt document
        doc = frappe.get_doc("Purchase Receipt", docname)
        item_idx=int(item_idx)
        item = next((i for i in doc.items if i.idx == item_idx), None)
        
        if not item:
            return {"success": False, "error": "Item not found."}

         # Log the row being processed
        frappe.logger().info(f"Processing row: {item_idx} with image: {item.custom_attach_image}")

   
        # Get the file URL for the image
        file_url = item.custom_attach_image
        if not file_url:
            return {"success": False, "error": "Please upload an image before extracting data."}

        # Get the file path
        file_path = get_file_path(file_url)
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(file_path)
        raw_text = extracted_text

        # Extract Lot No. (either 4-digit or 6-digit)
        lot_no_match = re.search(r"Lot\s*No\.?\s*:\s*(\d{4,6})", extracted_text, re.IGNORECASE)
        lot_no = lot_no_match.group(1) if lot_no_match else None

        # Extract Reel No. (including spaces within numbers)
        reel_no_match = re.search(r"Reel\s*No\.?\s*:\s*([\d\s]+)", extracted_text, re.IGNORECASE)
        reel_no = reel_no_match.group(1).replace(" ", "") if reel_no_match else None
        

        # Extract Weight (Wt in Kgs)
        all_numbers = re.findall(r'\d+', extracted_text)  # Extract all numbers from the text
        if len(all_numbers) > 1:
            weight = all_numbers[-1]  # Last number as Weight

        doc = frappe.get_doc("Purchase Receipt", docname)
        item = next((i for i in doc.items if i.idx == item_idx), None)

        # Update the item fields
        item.custom_lot_no = lot_no
        item.custom_reel_no = reel_no
        item.qty = weight
        
          # Ensure Accepted + Rejected Qty matches Received Qty
        item.received_qty = weight  # Assume full acceptance, adjust as needed
        item.rejected_qty = 0  # No rejection, adjust as needed
        doc.save(ignore_version=True)
        
        return {
            "success": True,
            "lot_no": lot_no,
            "reel_no": reel_no,
            "qty": weight,
            "raw_text": raw_text,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
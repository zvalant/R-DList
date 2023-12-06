class EmailMessages:
    def __init__(self,file_name="Current",row=0):
        self.error_key_collision = f"Error found: Collision Error in sheet {file_name}. This ID is already in use, provide a unique ID for row {row + 2}, This row will be skipped until this issue is resolved."
        self.error_key_not_assigned = f"Error found: Missing ID in sheet {file_name}. Provide a Unique ID for row {row+2}, This row will be skipped until this issue is resolved."
        self.error_duplicate_part = f"Error found: Same part/date combination already exists for this project, change row {row+2}. This row will be skipped until this issue is resolved."
        self.error_reused_id = f"Error found: The ID in row {row} was reused please give this row a new Unique ID"
        self.report = "View attached pdf to see R&D demand changes from the previous day."
        self.locked_pdf_driving = f"PDF locked, please close {file_name}.pdf in driving folder"

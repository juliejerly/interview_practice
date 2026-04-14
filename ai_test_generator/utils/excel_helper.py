from openpyxl import Workbook
from openpyxl.styles import Alignment, Font


def export_test_cases_to_excel(test_cases, jira_id):
    file_name=f"AI_Generated_Test_Cases_{jira_id}.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Test Cases"

    # -----------------------------
    # HEADER
    # -----------------------------
    sheet.append([
        "Test Case ID",
        "Test Scenario",
        "Preconditions",
        "Test Steps",
        "Expected Result",
        "Test Type"
    ])

    # Make header bold
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Freeze header row
    sheet.freeze_panes = "A2"

    # Set column widths
    sheet.column_dimensions['B'].width = 35
    sheet.column_dimensions['C'].width = 30
    sheet.column_dimensions['D'].width = 60
    sheet.column_dimensions['E'].width = 35

    row_num = 2

    # -----------------------------
    # DATA ROWS
    # -----------------------------
    for tc in test_cases:

        # Auto generate Test Case ID
        tc_id = f"TC_{row_num-1:03}"

        # Format steps with new lines
        steps_text = "\n".join(
            f"{i+1}. {step}" for i, step in enumerate(tc["test_steps"])
        )

        sheet.append([
            tc_id,
            tc["test_scenario"],
            tc["preconditions"],
            steps_text,
            tc["expected_result"],
            tc["test_type"]
        ])

        # Wrap text for steps column
        cell = sheet.cell(row=row_num, column=4)
        cell.alignment = Alignment(wrap_text=True)

        # Adjust row height
        sheet.row_dimensions[row_num].height = 80

        row_num += 1

    workbook.save(file_name)

    print(f"✅ Excel file created: {file_name}")
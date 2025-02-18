from utils import *
from constants import *


def initiate_action_workflow() -> None:
    try:
        print("\nprocessing...\n")
        workflow_input = get_yaml_config(file_path=DATA_ENTRY_YAML)
        workflow_input.deadline = calculate_thirty_day_deadline(
            workflow_input.start_date
        )

        workflow_input.consultant, workflow_input.liaison = assign_hrc_hrl_reps(
            workflow_input.org
        )
        workflow_input.noa_description, workflow_input.plan_category = (
            get_action_details(workflow_input.noa_code_int)
        )

        if workflow_input.plan_category in TEMPORARY_POSITION_PLANS:
            validate_temporary_duration(
                workflow_input.start_date, workflow_input.end_date
            )

        notice_template = generate_notice_template(
            workflow_input.plan_category, workflow_input.deadline
        )
        formatted_notice_content = populate_notice_template(
            notice_template, workflow_input
        )

        save_notice_to_file(file_path=NOTICE_TXT_PATH, content=formatted_notice_content)
        archive_workflow(archive_path=ARCHIVE_YAML_PATH, workflow_input=workflow_input)

        print(f"\nprocessing complete: {workflow_input.employee_name}\n")
    except Exception as e:
        print(f"\nError: {e}\n")


MENU_ITEMS = {
    1: "Process Action",
    2: "Manual Entry",
    3: "Undo Most Recent",
    4: "Reset Action Files",
    5: "Match Org",
    6: "Validate Detail Duration",
    7: "Exit",
}


def display_menu() -> None:
    print("Make a selection:")
    [print(f"{k}: {v}") for k, v in MENU_ITEMS.items()]


def main() -> None:
    """Application entry point"""
    while True:
        try:
            display_menu()
            selection: int = int(input(">>> ").strip())
            if selection == 1:
                initiate_action_workflow()
            elif selection == 2:
                manual_entry()
                initiate_action_workflow()
            elif selection == 3:
                undo_most_recent()
            elif selection == 4:
                reset_action_files()
            elif selection == 5:
                org_string = input("Enter org string: ").strip()
                if not org_string:
                    print("Error: org string cannot be empty")
                else:
                    print(f"\norg: {match_org(org_string)}\n")
            elif selection == 6:
                validate_temporary_duration()
            elif selection == 7:
                exit()
            else:
                print("Error: Invalid selection. Please choose a valid option.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
        except Exception as e:
            print(f"\nError (Unexpected): {e}\n")
        finally:
            print(f"{'.'*100}\n")

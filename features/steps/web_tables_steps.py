from behave import given, when, then
from pages.web_tables_page import WebTablesPage
from fixtures.web_table_fixtures import WEB_TABLE_SAMPLE,WEB_TABLE_UPDATED

@given("I open the Web Tables page")
def step_open_web_tables(context):
    context.web_tables = WebTablesPage(context.page)
    context.web_tables.open()


@when("I add a new record")
def step_add_record(context):
    context.web_tables.click_add()
    data = WEB_TABLE_SAMPLE
    context.web_tables.fill_form(**data)
    context.web_tables.submit_form()
    context.expected_web_table_data = data


@then("I should see the new record in the table")
def step_check_record(context):
    email = WEB_TABLE_SAMPLE["email"]
    context.web_tables.assert_row_exists(email)

    row = context.web_tables.get_row_by_email(email)

    keys = ["first_name", "last_name", "age", "email", "salary", "department"]
    mismatches = []
    for i, key in enumerate(keys):
        expected = str(WEB_TABLE_SAMPLE[key])
        actual = row[i]
        if actual != expected:
            mismatches.append(f"{key}: expected '{expected}', got '{actual}'")
    
    assert not mismatches, f"Data mismatch for row with email {email}:\n" + "\n".join(mismatches)



@when("I search for the record by email")
def step_search_record(context):
    context.web_tables.search(WEB_TABLE_SAMPLE["email"])

@then("I should see the record in search results")
def step_check_search_result(context):
    context.web_tables.assert_row_exists(WEB_TABLE_SAMPLE["email"])

@when("I edit the first record")
def step_edit_first(context):
    context.web_tables.click_edit_row(0)
    context.web_tables.fill_form(**WEB_TABLE_UPDATED)
    context.web_tables.submit_form()
    context.expected_web_table_data = WEB_TABLE_UPDATED


@then("I should see the updated data in the table")
def step_check_updated(context):
    email = WEB_TABLE_UPDATED["email"]
    context.web_tables.assert_row_exists(email)
    row = context.web_tables.get_row_by_email(email)
    keys = ["first_name", "last_name", "age", "email", "salary", "department"]
    mismatches = []
    for i, key in enumerate(keys):
        expected = str(WEB_TABLE_UPDATED[key])
        actual = row[i]
        if actual != expected:
            mismatches.append(f"{key}: expected '{expected}', got '{actual}'")
    
    assert not mismatches, f"Data mismatch for row with email {email}:\n" + "\n".join(mismatches)


@when("I delete the first record")
def step_delete_first(context):
    context.web_tables.click_delete_row(0)

@then("the record should no longer be in the table")
def step_check_deleted(context):
    context.web_tables.assert_row_not_in_table(WEB_TABLE_UPDATED)
@when("I read all table rows")
def step_read_all_rows(context):
    context.expected_web_table_data = [
        {
            "first_name": "Cierra",
            "last_name": "Vega",
            "age": 39,
            "email": "cierra@example.com",
            "salary": 10000,
            "department": "Insurance"
        },
        {
            "first_name": "Alden",
            "last_name": "Cantrell",
            "age": 45,
            "email": "alden@example.com",
            "salary": 12000,
            "department": "Compliance"
        },
        {
            "first_name": "Kierra",
            "last_name": "Gentry",
            "age": 29,
            "email": "kierra@example.com",
            "salary": 2000,
            "department": "Legal"
        }
    ]

@then("I should see the expected data in the table")
def step_validate_table_data(context):
    if not hasattr(context, "expected_web_table_data"):
        raise AssertionError("No expected data defined in context. Did you forget to set it before reading?")

    expected_rows = context.expected_web_table_data
    actual_rows = context.web_tables.get_all_rows()

    keys = ["first_name", "last_name", "age", "email", "salary", "department"]

    for expected_row in expected_rows:
        found = any(all(str(expected_row[k]) == row[i] for i, k in enumerate(keys)) for row in actual_rows)
        assert found, f"Expected row {expected_row} not found in table"




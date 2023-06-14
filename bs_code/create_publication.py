import time
import timeit
import logging
from bs_code.utilities import logger_config
import bs_code.parameters as param
from bs_code.utilities import pre_processing, load, write, helpers
from bs_code.utilities import tables, charts, csvs, validations, dashboards
import bs_code.utilities.publication_files as publication
import xlwings as xw


def main():

    # Load frequently used parameters
    # Load reporting year
    year = param.YEAR
    # Load template/output file location parameters
    validations_kc63 = param.VALIDATIONS_OUTPUT_KC63
    validations_kc62 = param.VALIDATIONS_OUTPUT_KC62
    tables_template = param.TABLE_TEMPLATE
    charts_template = param.CHART_TEMPLATE
    report_tables_template = param.REPORT_TABLES_TEMPLATE
    csv_output_path = param.CSV_DIR
    dashboard_output_path = param.DASHBOARD_DIR
    # Load run parameters
    run_validations_kc63 = param.VALIDATIONS_KC63
    run_validations_kc62 = param.VALIDATIONS_KC62
    run_tables_kc63 = param.TABLES_KC63
    run_tables_kc62 = param.TABLES_KC62
    run_charts_kc63 = param.CHARTS_KC63
    run_charts_kc62 = param.CHARTS_KC62
    run_csvs_kc63 = param.CSVS_KC63
    run_csvs_kc62 = param.CSVS_KC62
    run_report_tables_kc62 = param.REPORT_TABLES_KC62
    run_dashboards = param.DASHBOARDS
    run_pub_outputs = param.RUN_PUBLICATION_OUTPUTS

    # Check which datasets need to be imported depending on the run flags
    if run_validations_kc63 | run_tables_kc63 | run_csvs_kc63 | run_charts_kc63 | run_dashboards:
        # Import the KC63 data (latest year and total no. of years as per parameters)
        year_range = helpers.get_year_range(year, param.TS_YEARS_KC63)
        df_kc63 = load.import_asset_data("KC63", year_range)
        # Apply pre-processing updates
        df_kc63 = pre_processing.update_kc63_data(df_kc63)

    if run_validations_kc62 | run_tables_kc62 | run_csvs_kc62 | run_charts_kc62 | run_report_tables_kc62 | run_dashboards:
        # Import the KC62 data (latest year and total no. of years as per parameters)
        year_range = helpers.get_year_range(year, param.TS_YEARS_KC62)
        df_kc62 = load.import_asset_data("KC62", year_range)
        # Apply pre-processing updates
        df_kc62 = pre_processing.update_kc62_data(df_kc62)

    # Run each part of the pipeline as per the run flags

    if run_validations_kc63:
        # Run the KC63 validation tables as defined by the items in get_validations_kc63
        all_validations = validations.get_validations_kc63()
        write.write_outputs(df_kc63, all_validations, validations_kc63)
        # Save the Excel validation file with the updated data and close Excel
        wb = xw.Book(validations_kc63)
        wb.save()
        xw.apps.active.api.Quit()

    if run_validations_kc62:
        # Run the KC63 validation tables as defined by the items in get_validations_kc63
        all_validations = validations.get_validations_kc62()
        write.write_outputs(df_kc62, all_validations, validations_kc62)
        # Save the Excel validation file with the updated data and close Excel
        wb = xw.Book(validations_kc62)
        wb.save()
        xw.apps.active.api.Quit()

    if run_tables_kc63:
        # Run the KC63 tables as defined by the items in get_tables_kc63
        all_tables = tables.get_tables_kc63()
        write.write_outputs(df_kc63, all_tables, tables_template)

        # Add the Table 11 LA footnote references.
        write.add_footnote_refs("Table 11",  "B21", "B")

    if run_tables_kc62:
        # Run the KC62 tables as defined by the items in get_tables_kc62
        all_tables = tables.get_tables_kc62()
        write.write_outputs(df_kc62, all_tables, tables_template)

        # Add the Table 12 BSU footnote references.
        write.add_footnote_refs("Table 12", "A23", "A", "B")

    # If any tables were updated
    if run_tables_kc63 | run_tables_kc62:
        # Save the Excel master tables with the updated data and close Excel
        wb = xw.Book(tables_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_csvs_kc63:
        # Run the KC63 tidy csv's as defined by the items in get_csvs_kc63
        all_csvs = csvs.get_csvs_kc63()
        write.write_outputs(df_kc63, all_csvs, csv_output_path,
                            param.CSV_NOT_INC)

    if run_csvs_kc62:
        # Run the KC62 tidy csv's as defined by the items in get_csvs_kc62
        all_csvs = csvs.get_csvs_kc62()
        write.write_outputs(df_kc62, all_csvs, csv_output_path,
                            param.CSV_NOT_INC)

    if run_charts_kc63:
        # Run the KC63 charts as defined by the items in get_charts_kc63
        all_charts = charts.get_charts_kc63()
        write.write_outputs(df_kc63, all_charts, charts_template)

    if run_charts_kc62:
        # Run the KC62 charts as defined by the items in get_charts_kc62
        all_charts = charts.get_charts_kc62()
        write.write_outputs(df_kc62, all_charts, charts_template)

    # If any charts were updated
    if run_charts_kc63 | run_charts_kc62:
        # Save the Excel master chart file with the updated data and close Excel
        wb = xw.Book(charts_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_report_tables_kc62:
        # Run the KC62 report tables as defined by the items in get_report_tables_kc62
        all_report_tables = tables.get_report_tables_kc62()
        write.write_outputs(df_kc62, all_report_tables, report_tables_template)

        # Save the Excel report tables with the updated data and close Excel
        wb = xw.Book(report_tables_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_dashboards:
        # Run the dashboard outputs

        # Run the KC63 dashboard outputs as defined by the items in get_dashboards_kc63
        all_dbs = dashboards.get_dashboards_kc63()
        write.write_outputs(df_kc63, all_dbs, dashboard_output_path)

        # Run the KC62 dashboard outputs as defined by the items in get_dashboards_kc62
        all_dbs = dashboards.get_dashboards_kc62()
        write.write_outputs(df_kc62, all_dbs, dashboard_output_path)

    # Save the cms ready tables and chart files to the publication area
    if run_pub_outputs:
        publication.save_tables(tables_template)
        publication.save_charts_as_image(charts_template)


if __name__ == "__main__":
    # Setup logging
    formatted_time = time.strftime("%Y%m%d-%H%M%S")
    logger = logger_config.setup_logger(
        # Setup file & path for log, as_posix returns the path as a string
        file_name=(
            param.OUTPUT_DIR / "Logs" / f"breast_screening_create_pub_{formatted_time}.log"
        ).as_posix())

    start_time = timeit.default_timer()
    main()
    total_time = timeit.default_timer() - start_time
    logging.info(
        f"Running time of create_publication: {int(total_time / 60)} minutes and {round(total_time%60)} seconds.")
    logger_config.clean_up_handlers(logger)

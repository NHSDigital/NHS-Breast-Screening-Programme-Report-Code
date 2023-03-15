import time
import timeit
import logging
from bs_code.utilities import logger_config
import bs_code.parameters as param
import bs_code.utilities.import_data as importdata
import bs_code.utilities.helpers as helpers
import bs_code.utilities.field_definitions as definitions
import bs_code.utilities.processing_steps as processing
import bs_code.utilities.tables as tables
import bs_code.utilities.charts as charts
import bs_code.utilities.csvs as csvs
import bs_code.utilities.dashboards as dashboards
import bs_code.utilities.publication_files as publication
import bs_code.utilities.write as write
import xlwings as xw


def main():

    # Load frequently used parameters
    # Load reporting year
    year = param.YEAR
    # Load template/master file location parameters
    tables_template = param.TABLE_TEMPLATE
    charts_template = param.CHART_TEMPLATE
    report_tables_template = param.REPORT_TABLES_TEMPLATE
    csv_output_path = param.CSV_DIR
    dashboard_output_path = param.DASHBOARD_DIR
    # Load run parameters
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

    if run_tables_kc63 | run_csvs_kc63 | run_charts_kc63 | run_dashboards:
        # Import the kc63 data (latest year and total no. of years as per parameters)
        year_range = helpers.get_year_range(year, param.TS_YEARS_KC63)
        df_kc63 = importdata.import_asset_data("KC63", year_range)

        # Import data for LA region updates
        df_la_updates = importdata.import_la_update_info()

        # Update kc63 org names based on dictionary in parameters file
        df_kc63.replace({"Org_Name": param.ORG_NAME_UPDATE_KC63},
                        inplace=True)

        # Update small LA org codes and names as per parameters input
        df_kc63 = processing.combine_small_las(df_kc63, param.ORG_UPDATE_KC63)

        # Update LA region info
        processing.update_la_regions(df_kc63, df_la_updates, year_range)

        # Add any additional measures (counts) required from field definitions
        df_kc63 = definitions.add_measures_counts(df_kc63, "KC63")

    if run_tables_kc62 | run_csvs_kc62 | run_charts_kc62 | run_report_tables_kc62 | run_dashboards:
        # Import the kc62 data (latest year and total no. of years as per parameters)
        year_range = helpers.get_year_range(year, param.TS_YEARS_KC62)
        df_kc62 = importdata.import_asset_data("KC62", year_range)
        # Update old KC62 Q region codes to their equivalent R region
        # codes based on the dictionary in the parameters file
        df_kc62.replace({"Parent_Org_Code": param.REGION_UPDATE_KC62},
                        inplace=True)

        # Update old KC62 region names to their new region names based on the
        # dictionary in the parameters file
        df_kc62.replace({"Parent_Org_Name": param.REGION_NAME_UPDATE_KC62},
                        inplace=True)

        # Update kc62 org names based on dictionary in parameters file
        df_kc62.replace({"Org_Name": param.ORG_NAME_UPDATE_KC62},
                        inplace=True)

        # Add a region order column based on the parameters input that determines
        # how BSU data is ordered.
        df_kc62 = helpers.new_column_from_lookup(df_kc62, "Parent_Org_Code",
                                                 param.REGION_ORDER_KC62,
                                                 "Parent_Org_Order")

        # Add any additional measures (counts) required from field definitions
        df_kc62 = definitions.add_measures_counts(df_kc62, "KC62")

    # Run each part of the pipeline as per the run flags

    if run_tables_kc63:
        # Run the kc63 tables as defined by the items in get_tables_kc63
        all_tables = tables.get_tables_kc63()
        write.write_outputs(df_kc63, all_tables, tables_template)

        # Add the table 11 LA footnote references.
        write.add_footnote_refs("Table 11",  "B21", "B")

    if run_tables_kc62:
        # Run the kc62 tables as defined by the items in get_tables_kc62
        all_tables = tables.get_tables_kc62()
        write.write_outputs(df_kc62, all_tables, tables_template)

        # Add the table 12 BSU footnote references.
        write.add_footnote_refs("Table 12", "A23", "A", "B")

    # If any tables were updated
    if run_tables_kc63 | run_tables_kc62:
        # Save the Excel master tables with the updated data and close Excel
        wb = xw.Book(tables_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_csvs_kc63:
        # Run the kc63 tidy csv's as defined by the items in get_csvs_kc63
        all_csvs = csvs.get_csvs_kc63()
        write.write_outputs(df_kc63, all_csvs, csv_output_path,
                            param.CSV_NOT_INC)

    if run_csvs_kc62:
        # Run the kc62 tidy csv's as defined by the items in get_csvs_kc62
        all_csvs = csvs.get_csvs_kc62()
        write.write_outputs(df_kc62, all_csvs, csv_output_path,
                            param.CSV_NOT_INC)

    if run_charts_kc63:
        # Run the kc63 charts as defined by the items in get_charts_kc63
        all_charts = charts.get_charts_kc63()
        write.write_outputs(df_kc63, all_charts, charts_template)

    if run_charts_kc62:
        # Run the kc62 charts as defined by the items in get_charts_kc62
        all_charts = charts.get_charts_kc62()
        write.write_outputs(df_kc62, all_charts, charts_template)

    # If any charts were updated
    if run_charts_kc63 | run_charts_kc62:
        # Save the Excel master chart file with the updated data and close Excel
        wb = xw.Book(charts_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_report_tables_kc62:
        # Run the kc62 report tables as defined by the items in get_report_tables_kc62
        all_report_tables = tables.get_report_tables_kc62()
        write.write_outputs(df_kc62, all_report_tables, report_tables_template)

        # Save the Excel report tables with the updated data and close Excel
        wb = xw.Book(report_tables_template)
        wb.save()
        xw.apps.active.api.Quit()

    if run_dashboards:
        # Run the dashboard outputs

        # Run the kc63 dashboard outputs as defined by the items in get_dashboards_kc63
        all_dbs = dashboards.get_dashboards_kc63()
        write.write_outputs(df_kc63, all_dbs, dashboard_output_path)

        # Run the kc62 dashboard outputs as defined by the items in get_dashboards_kc62
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

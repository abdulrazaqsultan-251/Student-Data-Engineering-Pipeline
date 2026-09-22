from app.output.csv_writer import (
    save_final_dataset,
    save_rejected_records,
)
from app.sources.api_source import extract_api
from app.sources.csv_source import extract_csv
from app.sources.database_source import extract_database
from app.transformation.cleaner import clean_student_data
from app.transformation.integration import (
    integrate_data,
    standardize_api,
    standardize_csv,
    standardize_database,
)
from app.transformation.transformer import (
    transform_student_data,
)
from app.utils.logger import logger
from app.validation.quality import (
    validate_final_data,
    validate_student_source,
)


def run_pipeline() -> None:
    """
    Run the complete student data ETL pipeline.
    """

    logger.info("Pipeline started.")

    try:
        # ==================================================
        # 1. Extract
        # ==================================================

        logger.info("Extracting CSV data.")
        csv_raw = extract_csv()

        logger.info(
            "CSV extraction completed: %d records.",
            len(csv_raw),
        )

        logger.info("Extracting API data.")
        api_raw = extract_api()

        logger.info(
            "API extraction completed: %d records.",
            len(api_raw),
        )

        logger.info("Extracting database data.")
        database_raw = extract_database()

        logger.info(
            "Database extraction completed: %d records.",
            len(database_raw),
        )

        # ==================================================
        # 2. Validate source data
        # ==================================================

        logger.info("Validating CSV source.")
        validate_student_source(csv_raw)

        logger.info("CSV source validation completed.")

        # ==================================================
        # 3. Standardize and Integrate
        # ==================================================

        logger.info("Standardizing CSV data.")
        csv_data = standardize_csv(csv_raw)

        logger.info("Standardizing API data.")
        api_data = standardize_api(api_raw)

        logger.info("Standardizing database data.")
        database_data = standardize_database(
            database_raw
        )

        logger.info("Integrating all data sources.")

        integrated_data = integrate_data(
            csv_data,
            api_data,
            database_data,
        )

        logger.info(
            "Integration completed: %d records.",
            len(integrated_data),
        )

        # ==================================================
        # 4. Clean
        # ==================================================

        logger.info("Cleaning integrated data.")

        clean_data, rejected_data = (
            clean_student_data(
                integrated_data
            )
        )

        logger.info(
            "Cleaning completed: %d clean records, "
            "%d rejected records.",
            len(clean_data),
            len(rejected_data),
        )

        # ==================================================
        # 5. Save rejected records
        # ==================================================

        logger.info("Saving rejected records.")

        save_rejected_records(
            rejected_data
        )

        logger.info(
            "Rejected records saved successfully."
        )

        # ==================================================
        # 6. Transform
        # ==================================================

        logger.info("Transforming clean data.")

        transformed_data = transform_student_data(
            clean_data
        )

        logger.info(
            "Transformation completed: %d records.",
            len(transformed_data),
        )

        # ==================================================
        # 7. Final Validation
        # ==================================================

        logger.info("Running final validation.")

        validate_final_data(
            transformed_data
        )

        logger.info(
            "Final validation completed successfully."
        )

        # ==================================================
        # 8. Load
        # ==================================================

        logger.info("Saving final dataset.")

        save_final_dataset(
            transformed_data
        )

        logger.info(
            "Final dataset saved successfully."
        )

        logger.info(
            "Pipeline completed successfully."
        )

        print()
        print("Pipeline completed successfully.")
        print("==============================")
        print(
            f"Final records    : "
            f"{len(transformed_data)}"
        )
        print(
            f"Rejected records : "
            f"{len(rejected_data)}"
        )

    except Exception:
        logger.exception(
            "Pipeline failed."
        )
        raise


if __name__ == "__main__":
    run_pipeline()
import os
import json
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, Tuple
from app.db.session import SessionLocal
from app.db.models import GovernmentDataSource, DatasetIngestionRun

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "reports")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

class DataPipelineService:
    @staticmethod
    def sync_manifest_to_db():
        manifest_path = os.path.join(RAW_DIR, "manifest.json")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest not found at {manifest_path}")
        
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        db = SessionLocal()
        try:
            for source_info in manifest.get("sources", []):
                existing = db.query(GovernmentDataSource).filter_by(dataset_id=source_info["dataset_id"]).first()
                if not existing:
                    ds = GovernmentDataSource(
                        dataset_id=source_info["dataset_id"],
                        name=source_info["name"],
                        official_url=source_info["official_url"],
                        catalog_url=source_info.get("catalog_url"),
                        local_file=source_info["local_file"],
                        reporting_period=source_info["reporting_period"],
                        granularity=source_info["granularity"],
                        units=source_info.get("units"),
                        is_synthetic_seed=source_info.get("is_synthetic_seed", False),
                        license=source_info.get("license", "GODL"),
                        limitations=source_info.get("limitations")
                    )
                    db.add(ds)
            db.commit()
        finally:
            db.close()

    @staticmethod
    def inspect_and_clean_dataset(dataset_id: str) -> Dict[str, Any]:
        """Loads raw dataset, validates schema, converts types, detects duplicates & missing values, saves processed copy."""
        db = SessionLocal()
        try:
            source = db.query(GovernmentDataSource).filter_by(dataset_id=dataset_id).first()
            if not source:
                raise ValueError(f"Unknown dataset_id: {dataset_id}")
            
            raw_path = os.path.join(RAW_DIR, source.local_file)
            if not os.path.exists(raw_path):
                raise FileNotFoundError(f"Raw data file not found at {raw_path}")
            
            df = pd.read_csv(raw_path)
            raw_count = len(df)
            columns = list(df.columns)
            missing = df.isnull().sum().to_dict()
            duplicates = int(df.duplicated().sum())

            # Normalization
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
            
            # Type conversions based on dataset
            quality_warnings = []
            if dataset_id == "udyam_msme":
                if "registered_units" in df.columns:
                    df["registered_units"] = pd.to_numeric(df["registered_units"], errors="coerce").fillna(0).astype(int)
                if duplicates > 0:
                    quality_warnings.append(f"Detected {duplicates} duplicate records; dropping exact duplicates.")
                    df = df.drop_duplicates()
            elif dataset_id == "commodity_export":
                if "export_value_usd_million" in df.columns:
                    df["export_value_usd_million"] = pd.to_numeric(df["export_value_usd_million"], errors="coerce").fillna(0.0)
                if "growth_rate_pct" in df.columns:
                    df["growth_rate_pct"] = pd.to_numeric(df["growth_rate_pct"], errors="coerce").fillna(0.0)

            processed_filename = f"processed_{source.local_file}"
            processed_path = os.path.join(PROCESSED_DIR, processed_filename)
            df.to_csv(processed_path, index=False)

            # Ingestion run record
            ingestion_run = DatasetIngestionRun(
                dataset_id=dataset_id,
                raw_file_path=raw_path,
                processed_file_path=processed_path,
                row_count=len(df),
                columns_detected=columns,
                missing_values_count=missing,
                validation_status="VALIDATED",
                quality_warnings=quality_warnings
            )
            db.add(ingestion_run)
            db.commit()

            return {
                "dataset_id": dataset_id,
                "name": source.name,
                "raw_records": raw_count,
                "processed_records": len(df),
                "columns": columns,
                "missing_values": missing,
                "duplicates_dropped": duplicates,
                "quality_warnings": quality_warnings,
                "processed_path": processed_path,
                "reporting_period": source.reporting_period,
                "granularity": source.granularity,
                "is_synthetic_seed": source.is_synthetic_seed
            }
        finally:
            db.close()

    @staticmethod
    def get_processed_dataframe(dataset_id: str) -> pd.DataFrame:
        db = SessionLocal()
        try:
            source = db.query(GovernmentDataSource).filter_by(dataset_id=dataset_id).first()
            if not source:
                raise ValueError(f"Unknown dataset_id: {dataset_id}")
            processed_filename = f"processed_{source.local_file}"
            processed_path = os.path.join(PROCESSED_DIR, processed_filename)
            if not os.path.exists(processed_path):
                # Clean first
                DataPipelineService.inspect_and_clean_dataset(dataset_id)
            return pd.read_csv(processed_path)
        finally:
            db.close()

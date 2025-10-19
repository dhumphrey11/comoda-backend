import os
from typing import Optional, List, Dict
from google.cloud import bigquery

class BigQueryClient:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.dataset = os.getenv("BQ_DATASET", "comoda_analytics")
        self.client = bigquery.Client(project=self.project_id)

    def insert_signals(self, rows: List[Dict]):
        table_id = f"{self.project_id}.{self.dataset}.signals"
        errors = self.client.insert_rows_json(table_id, rows)
        if errors:
            raise RuntimeError(f"BigQuery insert errors: {errors}")
        return {"inserted": len(rows)}

    def query_signals_analytics(self, ticker: Optional[str], lookback_days: int):
        table_id = f"{self.project_id}.{self.dataset}.signals"
        sql = f"""
        SELECT ticker, AVG(score) as avg_score, COUNT(*) as n
        FROM `{table_id}`
        WHERE (@ticker IS NULL OR ticker = @ticker)
          AND generated_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @lookback_days DAY)
        GROUP BY ticker
        ORDER BY n DESC
        """
        job = self.client.query(sql, job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("ticker", "STRING", ticker),
                bigquery.ScalarQueryParameter("lookback_days", "INT64", lookback_days),
            ]
        ))
        return [dict(row) for row in job]

    def query_portfolio_metrics(self):
        table_id = f"{self.project_id}.{self.dataset}.portfolio_metrics"
        sql = f"SELECT * FROM `{table_id}` ORDER BY ts DESC LIMIT 100"
        job = self.client.query(sql)
        return [dict(row) for row in job]

    def export_cloudsql_to_bq_example(self):
        """Example: batch export data from Cloud SQL to BigQuery (placeholder)."""
        # This would typically use Dataflow or manual ETL with pandas/pyarrow.
        return {"status": "not_implemented"}
from collections import namedtuple

# this file is used for Artifacts

# Data Ingestion artifacts
DataIngestionArtifact = namedtuple("DataIngestionArtifact", ["train_file_path", "test_file_path",
                                                             "is_ingested", "message"])